from tkinter import *
from PIL import Image, ImageTk
import subprocess

def run():
	subprocess.run(["sudo","snort","-g","snort","-A","console","-i","enp0s3","-c","/etc/snort/snort.conf"])

root = Tk()
canvas = Canvas(root, width = 600, height = 300)
canvas.pack()

im = Image.open("snort.jpeg")
tk_im = ImageTk.PhotoImage(im)
canvas.create_image(300,150,image=tk_im)
T = Text(root, height =4, width =40)
T.pack()
T.insert(END,"Snort Intrusion Detection System\nDetect SSH bruteforce and DoS attack\n")
Button(root,text="Activate Snort",command = run).pack()
root.mainloop()
