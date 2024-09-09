import socket
import sys
import queue
import requests
import threading

baseURL = sys.argv[1]
movieName = sys.argv[2]
track = int(sys.argv[3])

player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():

    player_socket.connect(("localhost", 8000))

    #initialize queue
    q = queue.Queue()

    #create the producer thread
    producer_thread = threading.Thread(target=producer, args=(q,))
    #create the consumer thread
    consumer_thread = threading.Thread(target=consumer, args=(q,))

    #start the producer thread
    producer_thread.start()
    #start the consumer thread
    consumer_thread.start()

    #this guarantee that the consumer thread waits for the producer thread to finish
    producer_thread.join()
    consumer_thread.join()

    player_socket.close()


#method that returns the manifest already splited by lines
def get_manifest(baseURL, movieName):

    manifest_url = f"{baseURL}/{movieName}/manifest.txt"

    response = requests.get(manifest_url)

    return response.text.splitlines()


#method that returns the respective segment content
def download_segment(baseURL, movieName, track, start_offset, end_offset):

    segment_url = f"{baseURL}/{movieName}/{movieName}-{track}.mp4"

    #define the range of the segment to read
    headers = {"Range" : f"bytes={str(start_offset)}-{str(end_offset)}"}

    response = requests.get(segment_url, headers=headers)

    return response.content



def producer(q):

    manifest_lines = get_manifest(baseURL, movieName)

    #first 7 lines of the manifest (we just want the first line of the "Number of segments lines with 2 columns")
    i = 7
    j = 0 
    k = 0

    #to know how many lines in each track
    lines_in_track = int(manifest_lines[6])

    #responsible to get the first line of the respective offsets track
    while j < track - 1:
        i += 5 + lines_in_track
        j += 1

    #resposible for guarantee that all segment lines are readed
    while k < lines_in_track:
        offset = manifest_lines[i].split()

        start_offset = int(offset[0])
        #-1 to guarantee that next start_offset doesn't have the same offset value
        end_offset = start_offset + int(offset[1]) - 1

        segment = download_segment(baseURL, movieName, track, start_offset, end_offset)

        #Debugging prints
        print(start_offset)
        print(end_offset)
        
        #put the segment in queue
        q.put(segment)
        k += 1
        i += 1
        
    q.put(None)



def consumer(q):

    while True:

        #get the segment in queue
        segment = q.get()

        if segment is None:
            break
        
        #send the segment to the player
        player_socket.send(segment)


main()

