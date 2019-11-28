import socket
import threading
import os

class ServerThreading():
    "run in terminal: python3 server.py"
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 12345
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.s.bind((self.host, self.port))                         

    def listen(self):
        self.s.listen(5)
        while True:
            c, addr = self.s.accept()
            c.settimeout(180)
            threading.Thread(target = self.listenToClient,args = (c,addr)).start()

    def listenToClient(self, c, addr):
        print("Connect with client", addr)
        data = c.recv(1024)
        if (data.decode() == "download"):
            print("received download cmd")
            print(os.listdir("/home/pran/noninstantfile/server/"))
            FileName = c.recv(1024)
            for file in os.listdir("/home/pran/noninstantfile/server/"):
                if file == FileName.decode():
                    flag = 1 #found file
                    break
            if flag == 0:
                print(" Not Found On Server")
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
            FileName = c.recv(1024)
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