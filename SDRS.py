import cv2
import PIL.Image,PIL.ImageTk
import tkinter
from functools import partial
import threading
import imutils
import time

stream= cv2.VideoCapture(r"I:\DRS system\mini_runout.mp4")
def play(speed):
    print(f"You clicked on play. Speed is {speed}")

    #play video in reverse
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    grabbed,frame = stream.read()
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image =frame
    canvas.create_image(0,0, image=frame,anchor=tkinter.NW)

def pending(decision):
    # 1.Display decision pending image
    frame = cv2.cvtColor(cv2.imread(r"I:\DRS system\pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)

    # 2. Wait for 1 second
    time.sleep(1)

    # 3.display sponsor
    frame = cv2.cvtColor(cv2.imread(r"I:\DRS system\smartkheti(logo).png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    # 4.wait for second
    time.sleep(1.5)

    # 5.display out/not_out
    if decision=='out':
        decision_img=r"I:\DRS system\out.jpg"
    else:
        decision_img=r"I:\DRS system\not.jpg"
    frame = cv2.cvtColor(cv2.imread(decision_img), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("player is out")

def not_out():
    thread = threading.Thread(target=pending, args=("not_out",))
    thread.daemon = 1
    thread.start()
    print("player is not out")



#width and height
SET_WIDTH=640
SET_HEIGHT=360
window=tkinter.Tk()
window.title("Smart kheti DRS")
cv_img = cv2.cvtColor(cv2.imread(r"I:\DRS system\smartkheti(logo).png"),cv2.COLOR_BGR2RGB)
cv_img = imutils.resize(cv_img,width=SET_WIDTH,height=SET_HEIGHT)
canvas = tkinter.Canvas(window,width=SET_WIDTH,height=SET_HEIGHT)
photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0,0, ancho=tkinter.NW,image=photo)
canvas.pack()

# Buttons to control playback
btn = tkinter.Button(window, text="<< Previous(slow)",width=50,command=partial(play,-2))
btn.pack()

btn = tkinter.Button(window, text="Next(slow) >>",width=50,command=partial(play,2))
btn.pack()

btn = tkinter.Button(window, text="<< Previous(fast)",width=50,command=partial(play,-25))
btn.pack()

btn = tkinter.Button(window, text="Next(fast) >>",width=50,command=partial(play,25))
btn.pack()

btn = tkinter.Button(window, text="Give out",width=50,command=out)
btn.pack()

btn = tkinter.Button(window, text="Give_not_out",width=50,command=not_out)
btn.pack()
window.mainloop()