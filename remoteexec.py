import paramiko
import argparse
import sys
import utils


# Parse command-line arguments
parser = argparse.ArgumentParser(description="Execute a remote command via SSH.")
parser.add_argument("command", help="Command to execute on the remote server")
parser.add_argument("--username", required=True, help="Username for SSH authentication")
parser.add_argument("--password", required=True, help="Password for SSH authentication")
parser.add_argument("--input", help="Input string to pipe to the command")
args = parser.parse_args()

# Connection parameters
hostname = "well.com"
username = args.username
password = args.password
command = args.command

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
    
    # Execute command
    stdin, stdout, stderr = client.exec_command(command)
    
    # If input string is provided, write it to stdin and close it
    if args.input:
        stdin.write(args.input)
        stdin.flush()
    stdin.close()
    
    # Capture output
    output = stdout.read().decode("utf-8", errors="replace")
    errors = stderr.read().decode("utf-8", errors="replace")

    # Print results, ensuring UTF-8 encoding
    if output:
        sys.stdout.buffer.write(output.encode("utf-8", errors="replace"))
    if errors:
        sys.stdout.buffer.write(errors.encode("utf-8", errors="replace"))

except paramiko.AuthenticationException:
    print("Authentication failed")
except paramiko.SSHException as e:
    print(f"Connection failed: {str(e)}")
finally:
    client.close()