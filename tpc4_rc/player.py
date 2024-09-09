
import socket
import subprocess
# Start a socket listening for connections on 0.0.0.0:8000
#(0.0.0.0 means all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
# Run a viewer with an appropriate command line. Uncomment the mplayer
# version if you would prefer to use mplayer instead of VLC
# For Mac: alias vlc='/Applications/VLC.app/Contents/MacOS/VLC'
# cmdline = '/Applications/VLC.app/Contents/MacOS/VLC --demux h264 -'
    cmdline = r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe -'
    player = subprocess.Popen(cmdline.split(), stdin=subprocess.PIPE)
    while True:
# Repeatedly read 1k of data from the connection and write it to
# the media player's stdin
        data = connection.read(1024)
        # Removing this code allows user to be able to stream whole video, but player does
        # not terminate when video stream is finished
        if not data:
            break
        player.stdin.write(data)
finally:
        connection.close()
        server_socket.close()
        player.terminate()