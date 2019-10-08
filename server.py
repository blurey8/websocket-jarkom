from socket import *
import subprocess as sp
import ast
from datetime import datetime

# Check if server connected to internet
def is_connected():
    try:
        create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


logs = []
# Add new log to log list
def update_log(addr, is_success):
    timestamp = datetime.now()
    err_msg = "" if is_success else " [BAD REQUEST]"
    log = '[{}]{} IP Address: {}, Port: {}'.format(timestamp, err_msg, addr[0], addr[1])
    logs.append(log)
    print(log)

# Return list of log info as string
def get_log_info():
    return "\n".join(logs)

# Run bash command and return it's output
def run_command(command):
    return sp.run(command, shell=True, check=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE).stdout

# Return the information based on given command
def process_command(command):

    # Convert command string into dictionary
    args = ast.literal_eval(command)

    # Turn all flags to true if 'all' flags is true
    if (args['all']):
        for key in args.keys() - ['server', 'port']:
            args[key] = True

    # Retrieve all information based on given flag/argument
    sentence = ''
    if (args['hardware']):
        sentence += "=== HARDWARE INFO ===\n"
        sentence += run_command("lscpu | egrep 'Architecture|Model name|cache'")
        sentence += "\n"
        
    if (args['physical']):
        sentence += "=== PHYSICAL MEMORY CAPACITY ===\n"
        sentence += run_command("free | egrep 'Mem|total'")
        sentence += "\n"

    if (args['swap']):
        sentence += "=== SWAP MEMORY CAPACITY ===\n"
        sentence += run_command("free | egrep 'Swap|total'")
        sentence += "\n"

    if (args['storage']):
        sentence += "=== STORAGE MEMORY CAPACITY ===\n"
        sentence += run_command("df -h --total | egrep 'Filesystem|total'")
        sentence += "\n"

    if (args['status']):
        sentence += "=== INTERNET CONNECTIVITY STATUS ===\n"
        if is_connected():
            sentence += "Internet is connected!\n"
        else:
            sentence += "Internet is NOT connected.\n"
        sentence += "\n"

    if (args['log']):
        sentence += "=== LOG STATUS ===\n"
        sentence += get_log_info()
        sentence += "\n"

    return sentence

def main():
    serverPort = 12000
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print('The server is ready to receive')

    try:
        while 1:
            connectionSocket, addr = serverSocket.accept()
            command = connectionSocket.recv(1024).decode()
            
            try:
                output = process_command(command).encode('utf-8')
            except Exception as ex:
                is_success = False
                print(ex.__class__, ":", ex)
            else:
                is_success = True
                connectionSocket.send(output)
            finally:
                update_log(addr, is_success)
                
    finally:
        connectionSocket.close()

main()