from socket import *
import subprocess as sp
import ast
from datetime import datetime

# from cpuinfo import get_cpu_info
# from psutil import disk_usage, swap_memory, virtual_memory

# 2. Memori fisik
# a. Kapasitas total
# b. Kapasitas yang telah digunakan
# c. Kapasitas kosong yang tersedia

# 3. Memori swap
# a. Kapasitas total
# b. Kapasitas yang telah digunakan
# c. Kapasitas kosong yang tersedia

# 4. Storage
# a. Kapasitas total
# b. Kapasitas yang telah
# digunakan
# c. Kapasitas kosong yang
# tersedia

# 5. Status koneksi server ke internet
# (online atau offline)

# 6. Akses
# a. Daftar log akun yang sukses
# mengakses server
# b. Daftar log akun yang gagal
# mengakses server 


def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

logs = []

def update_log(addr):
    timestamp = datetime.now()    
    log = '[{}] IP Address: {}, Port: {}'.format(timestamp, addr[0], addr[1])
    logs.append(log)
    print(log)

def get_log_info():
    return "\n".join(logs)


def run_command(command):
    return sp.run(command, shell=True, check=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE).stdout

def process_command(command):
    args = ast.literal_eval(command)
    print(args)

    if (args['all']):
        for key in args.keys() - ['server', 'port']:
            args[key] = True


    sentence = ''
    if (args['hardware']):
        data = get_cpu_info()
        sentence += "=== HARDWARE INFO ===\n"
        sentence += run_command("lscpu | egrep 'Architecture|Model name|cache'")
        sentence += "\n"
        
    if (args['physical']):
        data = virtual_memory()
        sentence += "=== PHYSICAL MEMORY CAPACITY ===\n"
        sentence += run_command("free | egrep 'Mem|total'")
        sentence += "\n"

    if (args['swap']):
        data = swap_memory()
        sentence += "=== SWAP MEMORY CAPACITY ===\n"
        sentence += run_command("free | egrep 'Swap|total'")
        sentence += "\n"

    if (args['storage']):
        data = disk_usage('/')
        sentence += "=== STORAGE MEMORY CAPACITY ===\n"
        sentence += run_command("df -h --total | egrep 'Filesystem|total'")
        sentence += "\n"

    if (args['status']):
        sentence += "=== INTERNET CONNECTIVITY STATUS ===\n"
        if is_connected():
            sentence += "Internet is connected!"
        else:
            sentence += "Internet is NOT connected."

    if (args['log']):
        sentence += "=== LOG STATUS ===\n"
        sentence += get_log_info()

    return sentence

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

log = []

try:
    while 1:
        connectionSocket, addr = serverSocket.accept()
        # print(connectionSocket.args)
        update_log(addr)
        # print(addr)
        sentence = connectionSocket.recv(1024).decode()
        print(sentence)
        
        try:
            output = process_command(sentence).encode('utf-8')
        except Exception as ex:
            print(ex.__class__, ex)
        else:
            connectionSocket.send(output)
        finally:
            pass
finally:
    # process_command(sentence)    
    connectionSocket.close()
