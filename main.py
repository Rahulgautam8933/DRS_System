import tkinter
from tkinter import ttk,filedialog
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time
from ttkthemes import themed_tk as tk

stream = None
file_path = ''
def open_file():
    global stream
    global file_path
    file_path = filedialog.askopenfilename()
    stream = cv2.VideoCapture(file_path)
def play_video(self):
    global stream
    global file_path
    file_path = filedialog.askopenfilename()
    stream = cv2.VideoCapture(file_path)
def pause_video(self):
        self.pause = True

def play(speed):
    global flag
    print(f"You clicked on play. Speed is{speed}")
    
    # play the video in reverse
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES,frame1 + speed)

    grabbed,frame = stream.read()
    if not grabbed:
        exit()

    frame = imutils.resize(frame,width=set_width,height=set_height)
    frame = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame, anchor=tkinter.NW)
    canvas.create_text(134,26,fill="yellow",font="Times 26 bold",text="Decision Pending")

def pending(decision):
    # display decision pending image
    
    frame = cv2.cvtColor(cv2.imread("pending.png"),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=set_width,height=set_height)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)

    # display wait for 1 second
    
    time.sleep(1)

    # display sponser image
    
    frame = cv2.cvtColor(cv2.imread("sponsor.png"),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=set_width,height=set_height)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)

    # display wait for 1.5 second
    time.sleep(2.5)

    # display out/not out image
    
    if decision == 'Out':
        decisionImg = "out.png"
    else:
        decisionImg = "not_out.png"

    frame = cv2.cvtColor(cv2.imread(decisionImg),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=set_width,height=set_height)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)

    
def out():
    thread = threading.Thread(target=pending,args=("Out",))
    thread.daemon = 1
    thread.start()
    print("Player is Out")

def not_out():
    thread = threading.Thread(target=pending,args=("Not Out",))
    thread.daemon = 1
    thread.start()
    print("Player is Not Out")

# width and height of a main screen
set_width = 820
set_height = 510

# Gui

# Window

    # window theme
window = tk.ThemedTk()
window.get_themes()
window.set_theme("radiance")

# window configure
window.configure(bg='white')
window.resizable(width=False,height=False)
window.title("Third Empire Decision System made by Rahul Gautam")

# canvas
cv_img = cv2.cvtColor(cv2.imread("welcome.png"),cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window,width=set_width,height=set_height)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0,0,anchor=tkinter.NW,image=photo)
canvas.grid(row = 0,column=1,rowspan=4)


# Buttons to control playback
    # frame1
frame1 = tkinter.LabelFrame(window,text='Controls',bg='white',fg='red')

btn = ttk.Button(frame1,text="<< Previous (fast)",width=30,command=partial(play, -25))
btn.grid(row=0,column=0,padx=5,pady=2)

btn = ttk.Button(frame1,text="<< Previous (slow)",width=30,command=partial(play, -2))
btn.grid(row=1,column=0,padx=5,pady=2)

btn = ttk.Button(frame1,text="Next (slow) >>",width=30,command=partial(play, 2))
btn.grid(row=2,column=0,padx=5,pady=2)

btn = ttk.Button(frame1,text="Next (fast) >>",width=30,command=partial(play, 25))
btn.grid(row=3,column=0,padx=5,pady=2)

frame1.grid(row=0,column=0)

# Buttons to decison
    # frame2
frame2 = tkinter.LabelFrame(window,text="Decision",bg='white',fg='red')

btn = ttk.Button(frame2,text="Give Out",width=30,command=out)
btn.grid(row=1,column=2,padx=5,pady=2)

btn = ttk.Button(frame2,text="Give Not Out",width=30,command=not_out)
btn.grid(row=2,column=2,padx=5,pady=2)

frame2.grid(row=1,column=0)

# Button to open file
# frame3
frame3 = tkinter.LabelFrame(window,text="Open Video",bg='white',fg='red')

btn = ttk.Button(frame3,text="Open",width=30,command=open_file)
btn.grid(row=1,column=2,padx=5,pady=2)

btn = ttk.Button(frame3,text="play",width=30,command=play_video)
btn.grid(row=2,column=2,padx=5,pady=2)

btn = ttk.Button(frame3,text="pause",width=30,command=pause_video)
btn.grid(row=3,column=2,padx=5,pady=2)


frame3.grid(row=3,column=0)

window.mainloop()