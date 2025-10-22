#important libraris
import helper
import socket
import os


#variables
host = socket.gethostbyname(socket.gethostname())
port = 41000

#socket
server = socket.socket(socket.AF_INET,socket.\
SOCK_STREAM)

#bind host and port
server.bind((host,port))

#start listening
server.listen(10)
print("started listening..")

#recive connection
conn,addr = server.accept()
print(f"Client : {addr} ")

#remember : byte => str => int
while conn:
	try:
		data = conn.recv(1024).decode()
		if not data :
			break
		command = str(data)
		if command.startswith("cd") or command == 'ls' or command == 'pwd':
			output = helper.ExecuteCommand(command)
			print(output)
			conn.send(output.encode())
		if command[0:4].lower() == 'send':
			conn.send("READY".encode())
			output = helper.ReciveData(conn)
			print(output)
		if command[0:3] == 'get':
			conn.send("send".encode())
			if conn.recv(1024).decode() == "READY":
				output = helper.SendData(conn,command[4:])
				print(output)
	except Exception as e :
		conn.close()
server.close()

