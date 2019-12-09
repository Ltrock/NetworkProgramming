import socket
import threading
import os

class ServerThreading():
    "run in terminal: python3 server.py"
    "communicate with more than one client at the same time in the same network"
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 12345
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #socket.setsockopt(level, optname, value)
#Set the value of the given socket option,SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, 
#without waiting for its natural timeout to expire.
        self.s.bind((self.host, self.port))                         

    def listen(self):
        self.s.listen(5) #queue of 5
        while True:
            c, addr = self.s.accept()
            c.settimeout(180)
            threading.Thread(target = self.listenToClient,args = (c,addr)).start() #create thread when there is a client connection 

    def listenToClient(self, c, addr):
        print("Connect with client", addr)
        data = c.recv(1024)
        if (data.decode() == "download"):
            #print("received download cmd")
            print(os.listdir("/home/pran/noninstantfile/server/"))
            FileName = c.recv(1024)
            for file in os.listdir("/home/pran/noninstantfile/server/"):
                if file == FileName.decode():
                    flag = 1 #found file
                    break
            if flag == 0:
                print(" File Not Found On Server")
            else:
                print("File Found")
                upfile = FileName.decode()
                UploadFile = open("/home/pran/noninstantfile/server/"+upfile,"rb")
                Read = UploadFile.read(1024)
                while Read:
                    print("Sending file...",upfile)
                    c.send(Read)
                    Read = UploadFile.read(1024)
                print("Done Sending")
                UploadFile.close()
                c.close()
        elif (data.decode() == "upload"):
            FileName = c.recv(1024) # a buffer size of 1024 bytes at a time
            downfile = FileName.decode()
            Data = c.recv(1024)
            DownloadFile = open(downfile,"wb")
            while Data:
                print('Recieving...',downfile)
                DownloadFile.write(Data)
                Data = c.recv(1024)
            print("Done Recieving")
            DownloadFile.close()
            c.close()      
                 
if __name__ == "__main__":
    ServerThreading().listen()
