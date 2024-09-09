from socket import *
import pickle
import sys
import select
import random


receiverIP = sys.argv[1]
receiverPort = int(sys.argv[2])
fileName = sys.argv[3]

recieverSocket = socket(AF_INET,SOCK_DGRAM)

recieverAddr = (receiverIP, receiverPort)

recieverSocket.bind(recieverAddr)


def waitForReply( uSocket ):
    rx, tx, er = select.select( [uSocket], [], [], 1)
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
    
    f = open(fileName, 'wb')
    offset = 0 
    expectedseqnum = 1

    while True:

        if waitForReply(recieverSocket):
            
            pickledmsg, address = recieverSocket.recvfrom(2048)
            msg = pickle.loads(pickledmsg)
            
            seqN = msg[1]
            data = msg[2]

            if not data:
                print("complete.")
                break
            
            if seqN == expectedseqnum:
               
                f.seek(offset)
                f.write(data)
                offset += len(data)
                replymesg = (1, expectedseqnum) 
                expectedseqnum += 1
                print("recieved: ", seqN)
                sendReply(replymesg, recieverSocket, address)

            else: 

                replymesg = (1, expectedseqnum)
                sendReply(replymesg, recieverSocket, address)

    recieverSocket.close()
    f.close()
        

main()



                

            

