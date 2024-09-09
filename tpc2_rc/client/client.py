from socket import *
import pickle
import sys
import select


host_of_server = sys.argv[1]
portSP = int(sys.argv[2])
fileName = sys.argv[3]
chunkSize = int(sys.argv[4])

offset = 0

clientSocket = socket(AF_INET,SOCK_DGRAM)

f = open(fileName, 'wb')

def waitForReply( uSocket ):
    rx, tx, er = select.select( [uSocket], [], [], 1)
    # waits for data or timeout after 1 second
    if rx==[]:
        return False
    else:
        return True

while True:
    request = (fileName, offset, chunkSize)
    req = pickle.dumps(request)
    clientSocket.sendto(req, (host_of_server, portSP))
    if not (waitForReply(clientSocket)):
        continue

    datapick, address = clientSocket.recvfrom(40000) #para chunksize de 32Kb
    status, size, data = pickle.loads(datapick)

    if(status == 1):
        print('Could not find file in server')
        break

    if (status == 0):
        f.write(data)
        if (size < chunkSize):
             break
        
        offset += size

            
    elif(status == 2):
        print("invalid chunksize")
        break