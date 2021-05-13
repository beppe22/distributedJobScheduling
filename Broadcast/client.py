import socket


PORT = 37020

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP

# Enable broadcasting mode
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # change `client` to `server` for server.py
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind(("", PORT))
while True:
    data, addr = client.recvfrom(1024)
    print("received message: %s"%data)
