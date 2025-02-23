import paramiko
import argparse
import sys
import utils
import base64

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Execute a remote command via SSH.")
parser.add_argument("command", help="Command to execute on the remote server")
parser.add_argument("--username", required=True, help="Username for SSH authentication")
parser.add_argument("--password", required=True, help="Password for SSH authentication")
parser.add_argument("-base64", action="store_true", help="Decode command from base64")
args = parser.parse_args()

# Connection parameters
hostname = "well.com"
username = args.username
password = args.password

# Build command array
command = args.command
if args.base64:
    command = base64.b64decode(command).decode("utf-8")

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

    
    print("Command to send to remote host:")
    print(command)
    # Execute command with proper quoting
    
    stdin, stdout, stderr = client.exec_command(command)
    stdin.close()
    
    # Capture output
    output = stdout.read().decode("utf-8", errors="replace")
    errors = stderr.read().decode("utf-8", errors="replace")

    # Print results, ensuring UTF-8 encoding
    if output:
        print("output from remote host:")
        sys.stdout.buffer.write(output.encode("utf-8", errors="replace"))
    if errors:
        print("error from remote host:")
        sys.stdout.buffer.write(errors.encode("utf-8", errors="replace"))

except paramiko.AuthenticationException:
    print("Authentication failed")
except paramiko.SSHException as e:
    print(f"Connection failed: {str(e)}")
finally:
    client.close()