import paramiko
import argparse
import sys
import base64
import time
import re

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Execute commands via SSH with specific timing.")
    parser.add_argument("command", help="Base64 encoded command to execute")
    parser.add_argument("--username", required=True, help="Username for SSH authentication")
    parser.add_argument("--password", required=True, help="Password for SSH authentication")
    parser.add_argument("--conf", required=True, help="Conference name")
    parser.add_argument("--topic", required=True, help="Topic name")
    parser.add_argument("-debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    # Hard-coded host
    hostname = "well.com"
    username = args.username
    password = args.password
    conf = args.conf
    topic = args.topic
    debug_mode = args.debug

    # Decode command from base64
    try:
        decoded_command = base64.b64decode(args.command).decode("utf-8")
        lines = decoded_command.strip().split('\n')
    except Exception as e:
        print(f"Error decoding command: {str(e)}")
        sys.exit(1)

    # Initialize SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Establish connection
        client.connect(
            hostname=hostname,
            username=username,
            password=password
        )
        
        # Open channel for interactive shell
        channel = client.invoke_shell()
        
        # Buffer for received data
        output_buffer = ""
        
        # Flag to track if we've seen the "ok (" pattern
        ok_pattern_seen = False
        
        # Wait for initial response
        while True:
            if channel.recv_ready():
                data = channel.recv(4096).decode("utf-8", errors="replace")
                output_buffer += data
                
                # Only print debug output if debug mode is enabled
                if debug_mode:
                    print(data, end="", flush=True)
                
                # Check for "ok (" pattern (case insensitive)
                if not ok_pattern_seen and re.search(r"ok \(", data, re.IGNORECASE):
                    ok_pattern_seen = True
                    
                    # Wait 300ms
                    time.sleep(0.3)
                    
                    # Send "post conf topic" with newline
                    channel.send(f"!post {conf} {topic}\n")
                    
                    # Wait 300ms
                    time.sleep(0.3)
                    
                    # Send each line with newline, wait 50ms after each
                    for line in lines:
                        channel.send(f"{line}\n")
                        time.sleep(0.05)
                    
                    # Send single dot with newline
                    channel.send(".\n")
                    
                    # Wait 100ms to collect final output, then close
                    time.sleep(0.1)
                    break
            
            # Prevent CPU hogging
            time.sleep(0.1)
        
        # Collect any remaining output for 100ms
        time.sleep(0.1)
        while channel.recv_ready():
            data = channel.recv(4096).decode("utf-8", errors="replace")
            output_buffer += data
            
            # Only print debug output if debug mode is enabled
            if debug_mode:
                print(data, end="", flush=True)
            
    except paramiko.AuthenticationException:
        print("Authentication failed")
    except paramiko.SSHException as e:
        print(f"Connection failed: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    main()