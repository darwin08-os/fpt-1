#important libraris
import helper
import socket
import os
import subprocess

#variables
host = socket.gethostbyname(socket.gethostname())
#host = "127.0.0.1"
port = 41000

#socket
server = socket.socket(socket.AF_INET,socket.\
SOCK_STREAM)

#bind host and port
server.bind((host,port))

#start listening
server.listen(10)
print("server ip : ",host)
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
		if command.startswith("cd") or command in ('ls', 'pwd'):
			try:
				# Handle 'cd' with spaces correctly
				if command.startswith("cd") and len(command) > 2:
					path = command[3:].strip()
					# Change directory safely
					os.chdir(path)
					output = os.getcwd()
				else:
					# For 'pwd' or 'ls'
					if command == 'ls':
						command_to_run = 'dir'
					else:
						if command == "pwd":
							command = "cd"
						command_to_run = command
					# Execute the command safely
					run = subprocess.Popen(command_to_run, shell=True,
										stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
					output = run.stdout.read() + run.stderr.read()
			except Exception as e:
				output = f"ERROR: {e}"

			# Convert output to bytes for reliable sending
			output_bytes = output.encode(errors="replace")
			size = len(output_bytes)

			# First, send the size of output
			conn.send(str(size).encode())

			# Send the output in chunks
			chunk_size = 4096  # 4 KB per chunk
			sent = 0
			while sent < size:
				end = min(sent + chunk_size, size)
				conn.send(output_bytes[sent:end])
				sent = end

					
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

