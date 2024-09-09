from socket import *
import pickle
import sys
import random
import os

#connecting to udp socket

portSP = int(sys.argv[1])

serverSocket = socket(AF_INET,SOCK_DGRAM)

serverSocket.bind(("",portSP))

def fileExists(fileName):
    return os.path.exists(fileName)

def serverReply (msg, sock, address):
    # msg is a byte array ready to be sent
    # Generate random number in the range of 0 to 10
    message = pickle.dumps(msg)
    rand = random.randint(0, 10)
    # If rand is less is than 3, do not respond
    if rand >= 3:
        sock.sendto(message, address)
    return

while True:

    message, address = serverSocket.recvfrom(1024)
    request = pickle.loads(message)
    fileName = request[0]
    offset = request[1]
    noBytes = request[2]
    if(fileExists(fileName)):
        fileSize = os.path.getsize(fileName)
    print(f'file = {fileName} offset = {offset} noBytes = {noBytes}')


    try:

        f = open(fileName, 'rb')

        if(noBytes > fileSize):
            print("a")
            serverReply((2, 0, bytearray(1)), serverSocket, address)
            f.close()
        
        f.seek(offset)
        data = f.read(noBytes)
        f.close()

        msg = (0, len(data), data)
        serverReply(msg, serverSocket, address)


    except FileNotFoundError:
        print("Could not open file.")
        serverReply((1, 0, bytearray(1)), serverSocket, address)
        break
    



