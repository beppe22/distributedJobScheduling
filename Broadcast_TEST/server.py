import socket
import time

PORT = 37020

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #serve per runnare più istanze sullo stesso dispositivo
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
message = b"your very important message"
server.bind(("", PORT))
while True:
    server.sendto(message, ('<broadcast>', PORT))
    print("message sent!")

    #ovviamente pure io ricevo la comunicazion broadcast!
    data, addr = server.recvfrom(1024)
    print("received message: %s from %s" % (data , addr))
    time.sleep(1)