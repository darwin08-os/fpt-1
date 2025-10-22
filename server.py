import socket
import os
HOST = "127.0.0.1"
PORT = 9999
reading = 1024
last = 0
def actualrecive(c):
    filesize = int(c.recv(1024).decode('utf-8'))
    filename = c.recv(1024).decode('utf-8')
  
    with open("2"+filename,'wb') as f:
        if filesize < 1024:
            f.write(c.recv(int(str(filesize).encode('utf-8'))))
            f.close()
        else:
            iters = filesize//1024
            last = filesize - (1024*iters)
            for i in range(iters):
                f.write(c.recv(1024))
            f.write(c.recv(last))
            f.close()


def recivefile(c,sflag='SENDME'):
    c.send(sflag.encode('utf-8'))
    actualrecive(c)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))

s.listen(2)
print("waiting for connections...")
c , address = s.accept()
print(f"HOST : {HOST} , PORT : {PORT}")
while True:
    if c.recv(1024).decode('utf-8') == 'SEND' :
        # print("i got 'SEND' flag ")
        # print("i am sending you SENDME FLAG")
        recivefile(c)
        print("Done!!")
        break
    break