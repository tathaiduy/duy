from scapy.all import *
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
localIP = s.getsockname()[0]
destination_IP = "192.168.1.47"
#destination_port = int(port)
destination_port = 80
i = 1
while True:
    send(IP(src=localIP, dst=destination_IP) / TCP(sport=80, dport=destination_port), loop=0,inter=0.0000001)
    print("Packet sent: ", i)
    i = i + 1