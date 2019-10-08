#!/usr/bin/python3

from socket import *
import argparse, time

parser = None
# Create parser if it doesn't exist
def get_parser():
    global parser
    if parser == None:
        parser = argparse.ArgumentParser("Client argument")
        parser.add_argument("-s", "--server", help="Specify the (s)erver IP", required=True)
        parser.add_argument("-p", "--port", help="Specify the server (p)ort", type=int, required=True)
        parser.add_argument("-a", "--all", help="Information about (a)ll things below", action='store_true')
        parser.add_argument("-w", "--hardware", help="Information about hard(w)are", action='store_true')
        parser.add_argument("-y", "--physical", help="Information about ph(y)sical memory", action='store_true')
        parser.add_argument("-m", "--swap", help="Information about swap (m)emory", action='store_true')
        parser.add_argument("-t", "--storage", help="Information about s(t)orage capacity", action='store_true')
        parser.add_argument("-c", "--status", help="Information about internet (c)onnection status", action='store_true')
        parser.add_argument("-l", "--log", help="Information about (a)ccess log info", action='store_true')
    return parser

# Return argument as Namespace object
def get_args():
    return get_parser().parse_args()

def main():
    # Retrieve argument
    args = get_args()

    # Setup server address
    serverName = args.server #'localhost'
    serverPort = args.port #12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    # Send command
    sentence = str(vars(args))
    clientSocket.send(sentence.encode('utf-8'))

    # Receive information
    output = clientSocket.recv(1024).decode()
    print(output)

    clientSocket.close()

main()