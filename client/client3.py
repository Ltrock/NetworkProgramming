from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from PIL import Image, ImageTk
import socket, sys, os, time


def listfsend():
    root.filename =  filedialog.askopenfilename(initialdir = "/home/pran/noninstantfile/client/file/",title = "File on client")
def listfrecv():
    root.filename =  filedialog.askopenfilename(initialdir = "/home/pran/noninstantfile/server/",title = "File on server") 
def bar():
    progress['value']=25
    root.update_idletasks()
    time.sleep(1)
    progress['value']=50
    root.update_idletasks()
    time.sleep(1)
    progress['value']=75
    root.update_idletasks()
    time.sleep(1)
    progress['value']=100

root = Tk()
root.title("Client#3")
#window.geometry('500x500')
canvas = Canvas(root, width = 700, height = 500)
canvas.pack()
label1 = Label(root, text='Welcome to send/receive file program')
label1.config(font=('helvetica', 14))
canvas.create_window(350, 10, window=label1)
im = Image.open("/home/pran/noninstantfile/client/papa.png")
tk_im = ImageTk.PhotoImage(im)
canvas.create_image(350,140,image=tk_im)
label2 = Label(root, text='Select mode:')
label2.config(font=('helvetica', 10))
canvas.create_window(150, 320, window=label2)
# Option menu variable
optionVar = StringVar()
optionVar.set("upload")
# Create a option menu
option = OptionMenu(root, optionVar, "upload", "download")
#option.pack()
canvas.create_window(150, 360, window=option)

label3 = Label(root, text='Input filename:')
label3.config(font=('helvetica', 10))
canvas.create_window(400, 320, window=label3)
#var = StringVar(root)
#entry1 = Entry(root,textvariable = var)
en = StringVar()
en.set("ssh.txt")
# Create a option menu
entry1 = OptionMenu(root, en, "ssh.txt", "ddos.txt","csvssh.csv","sshbrute.pcap")
canvas.create_window(430, 360, window=entry1)
progress=Progressbar(root,orient=HORIZONTAL,length=300,mode='determinate')
#progress.pack()
canvas.create_window(350, 420, window=progress)
#List file that wanna send
btnShow = Button(root, text="List client file",command=listfsend)
#btnShow.pack()
canvas.create_window(250, 460, window=btnShow)
#List file that wanna receive  
btnShow2 = Button(root, text="List server file",command=listfrecv)
#btnShow2.pack()
canvas.create_window(450, 460, window=btnShow2)  
btnShow3 = Button(root, text="OK",command=lambda:[options(),bar()])
canvas.create_window(570, 360, window=btnShow3) 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
host = socket.gethostname() 
port = 12340         
s.bind((host, port))   

try:
    s.connect((host, 12345))
    print("Connected Successfully!")
except socket.error: 
    print("socket error")
def options():
    if optionVar.get().lower() == "download":
        op = "download"
        s.send(op.encode())
        #FileName = input("Enter Filename to Download from server : ")
        #print(en.get())
        FileName = en.get()
        Data = "xxx"
        while True:
            s.send(FileName.encode())
            Data = s.recv(1024)
            DownloadFile = open(FileName,"wb")
            while Data:
                print('Recieving...',FileName)
                DownloadFile.write(Data)
                Data = s.recv(1024)
            print("Done Recieving")
            DownloadFile.close()
            break
        
    elif optionVar.get().lower() == "upload":
        op = "upload"
        s.send(op.encode())
        print(os.listdir("/home/pran/noninstantfile/client/file/"))
        #FileName = input("Enter Filename : ")
        #FileName= "ssh.txt"  =>This worked
        #print(en.get())
        FileName = en.get()
        s.send(FileName.encode())
        UploadFile = open("/home/pran/noninstantfile/client/file/"+FileName,"rb")
        Read = UploadFile.read(1024)
        while Read:
            print("Sending...",FileName)
            s.send(Read) #sends 1KB 
            Read = UploadFile.read(1024)
        print("Done Sending")
        UploadFile.close()   
    s.close()
root.mainloop()

