from socket import *
import pickle
import sys
import select
import random

senderHostName = sys.argv[1]
senderPort = int(sys.argv[2])
recieverHostName = sys.argv[3]
recieverPort = int(sys.argv[4])
fileName_receiver = sys.argv[5]
windowSizeInBlocks = int(sys.argv[6])

senderSocket = socket(AF_INET,SOCK_DGRAM)

timeOut = 10

recieverAddress = (recieverHostName, recieverPort)

def waitForReply( uSocket ):
    rx, tx, er = select.select( [uSocket], [], [], 10)
    # waits for data or timeout after 1 second
    if rx==[]:
        return False
    else:
        return True
    
def sendReply (msg, sock, address):
    # msg is a byte array ready to be sent
    # Generate random number in the range of 0 to 10
    message = pickle.dumps(msg)
    rand = random.randint(0, 10)
    # If rand is less is than 3, do not respond
    if rand >= 3:
        sock.sendto(message, address)
    return


def main():

    base = 1
    nextseqnum = 1
    offset = 0
    blockSize = 1024
    window = {}
    
    try:
        f = open(fileName_receiver, 'rb')

    except FileNotFoundError:
        print("Could not open file")


    for i in range(windowSizeInBlocks):
        f.seek(offset)
        data = f.read(blockSize)
        reply = (0, nextseqnum, data)
        window[i + 1] = reply
        nextseqnum += 1
        offset += len(data)
        sendReply(window[i + 1], senderSocket, recieverAddress)
        #print(len(window[i + 1]))

    while True:

        if waitForReply(senderSocket):
            pickledmsg, _ = senderSocket.recvfrom(2048)
            msg = pickle.loads(pickledmsg)
            cSeqNum = msg[1]

            if base == cSeqNum:
                for i in range(windowSizeInBlocks):
                    sendReply(window[base + i], senderSocket, recieverAddress)

            else:
                window[base] = None
                base += 1
                f.seek(offset)
                data = f.read(blockSize)
                reply = (0, nextseqnum, data)
                window[nextseqnum] = reply
                offset += len(data)
                print("sending: ", nextseqnum)
                sendReply(window[nextseqnum], senderSocket, recieverAddress)
                nextseqnum += 1


                if not data:
                    f.close()
                    senderSocket.close()
                    print("complete.")
                    break

    
main()

        

