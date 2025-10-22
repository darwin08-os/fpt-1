import socket
import os

#end is indicated by this : \/ENDING\/

HOST = "127.0.0.1"
PORT = 9999
SEND = 'SEND'
reading = 1024
last = 0
def actualsend(c,filepath):
    sizeOfFile = str(os.path.getsize(filepath)).encode('utf-8')
    print(f"total bytes : {sizeOfFile}")
    filetype = str(os.path.basename(filepath)).encode('utf-8')
    c.send(sizeOfFile) # send file size
    c.send(filetype) #send file type
    sizeOfFile = int(sizeOfFile.decode('utf-8'))
    # print("i send you filesize")
    with open(filepath,'rb') as f:
        if sizeOfFile < 1024:
            file=f.read(sizeOfFile)
            c.send(file)
            f.close()
        else:
            iters = sizeOfFile//1024
            last = sizeOfFile - (1024*iters)
            for i in range(iters):
                chunk = f.read(1024)
                c.send(chunk)
            
            chunk = f.read(last)
            c.send(chunk)
            f.close()

def sendfile(c,filepath):
    c.send(SEND.encode('utf-8'))
    while True:
        if c.recv(1024).decode('utf-8') == 'SENDME':
            # print("i got 'SENDME' flag ")
            actualsend(c,filepath)
            break
        
        

c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

c.connect((HOST,PORT))

while True:
    option = input("do you wanna send the file? y/n : ")
    if option == 'y':
        filepath = input("file-path>")
        sendfile(c,filepath)
        break
    break