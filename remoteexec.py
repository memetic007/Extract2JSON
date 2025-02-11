import paramiko
import argparse
import sys

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Execute a remote command via SSH.")
parser.add_argument("command", help="Command to execute on the remote server")
parser.add_argument("--username", required=True, help="Username for SSH authentication")
parser.add_argument("--password", required=True, help="Password for SSH authentication")
args = parser.parse_args()

# Connection parameters
hostname = "well.com"
username = args.username  # Use command-line argument for username
password = args.password  # Use command-line argument for password
command = args.command  # Use command-line argument for command

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