#libs
import subprocess
import os
from tqdm import tqdm
def ExecuteCommand(command):
        if command == "cd":
                return os.getcwd()
        if command.startswith("cd") and len(command)>3:
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
                        pbar = tqdm(total=max(filesize,4096),\
unit='B',unit_scale=True,desc="Uploading the file")
                        while True:
                                data = f.read(4096)
                                if not data:
                                        break
                                c.sendall(data)
                                pbar.update(len(data))
                        pbar.close()
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
                remain = filesize
                with open(filename,"wb") as f :
                        pbar = tqdm(total=max(filesize,4096),\
unit='B',unit_scale=True,desc="Uploading the file")
                        while remain > 0:
                                if filesize >= 4096:
                                        chunk = 4096
                                else:
                                        chunk = remain
                                data = c.recv(chunk)
                                if not data:
                                        break
                                f.write(data)
                                remain = remain - len(data)
                                pbar.update(len(data))
                        pbar.close()
                return "recieved"
        except Exception as e :
                return e
