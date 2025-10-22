#libs
import helper
import socket
import os

#vars
host = "127.0.0.1"
port = 41000


#socket
client = socket.socket(socket.AF_INET,socket.\
SOCK_STREAM)

#connect
client.connect((host,port))

while True:
	try:
		command = input(f"{os.getcwd()}>")
		if command.startswith("!"): #general commands
			output = helper.ExecuteCommand(command[1:])
			print(output)
		if command[0:4]!='send'\
and command[0:3]!='get' and (command.startswith("cd") \
or command.startswith("ls") or command.startswith("pwd")) :
			client.send(command.encode())
			output = client.recv(2048).decode()
			print(output)
		if command.startswith('send'):
			#three way handshake
			client.send("SEND".encode())
			if client.recv(1024).decode() == "READY":
				output = helper.SendData\
(client,command[5:])
			print(output)
		if command.startswith("get"):
			client.send(command.encode())
			if client.recv(1024).decode() == "send":
				client.send("READY".encode())
				output = helper.ReciveData(client)
				print(output)
	except KeyboardInterrupt:
		client.close()
		break
	except Exception as e:
		print("error :",e)

