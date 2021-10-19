import cv2
import PIL.Image,PIL.ImageTk
import tkinter
from functools import partial
import threading
import imutils
import time
import numpy as np
#from common import Sketchers
SET_WIDTH = 640
SET_HEIGHT = 360
stream = cv2.VideoCapture(r"I:\DRS system\mini_runout.mp4") #video path
stream2 = cv2.VideoCapture(r"I:\DRS system\mini_runout.mp4")
fgbg = cv2.createBackgroundSubtractorMOG2()
ROI=[(SET_WIDTH/2.5, SET_HEIGHT), (SET_WIDTH, SET_HEIGHT), (SET_WIDTH, 0), (SET_WIDTH/2.5, 0)]
def play(speed):
    print(f"You clicked on play. Speed is {speed}")

    # play video in reverse
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    frame2 = stream2.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    stream2.set(cv2.CAP_PROP_POS_FRAMES, frame2 + speed - 1)
    grabbedim, frameim = stream.read()
    grabbed2, frame2 = stream2.read()
    # fgmask = fgbg.apply(frame)
    subs=cv2.subtract(frameim, frame2)
    frameim1 = cv2.resize(subs, (SET_WIDTH, SET_HEIGHT))
    frameim1 = cv2.cvtColor(frameim1, cv2.COLOR_RGB2GRAY)
    mask = np.zeros_like(frameim1)
    cv2.fillPoly(mask, (np.array([ROI], np.int32)), 255)# filling the region with white
    frameim1 = cv2.bitwise_and(frameim1, mask)
    res = frameim1.astype(np.uint8)
    percentage = (np.count_nonzero(res)*100)/res.size
    print(percentage)
    frameim1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frameim1))
    canvas.image = frameim1
    canvas.create_image(0, 0, image=frameim1, anchor=tkinter.NW)
    frameim2 = imutils.resize(frameim, width=SET_WIDTH, height=SET_HEIGHT)
    frameim2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frameim2))
    canvas.image2 = frameim2
    canvas.create_image(642, 0, image=frameim2, anchor=tkinter.NW)


def pending(decision):
    # 1.Display decision pending image
    frame = cv2.cvtColor(cv2.imread(r"I:\DRS system\pending.png"), cv2.COLOR_BGR2RGB) # pending image path
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

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
    if decision == 'out':
        decision_img = r"I:\DRS system\out.jpg" #out decision image
    else:
        decision_img = r"I:\DRS system\not.jpg" #not out decision image
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

# width and height

window = tkinter.Tk()
window.title("Smart kheti DRS")
cv_img = cv2.cvtColor(cv2.imread(r"I:\DRS system\smartkheti(logo).png"), cv2.COLOR_BGR2RGB)
cv_img = cv2.resize(cv_img, (1000, 360))
canvas = tkinter.Canvas(window, width=SET_WIDTH*2, height=SET_HEIGHT)
photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(150, 0, ancho=tkinter.NW,image=photo)
canvas.pack()

# Buttons to control playback
btn = tkinter.Button(window, text="<< Previous(slow)", width=50, command=partial(play, -1))
btn.pack()

btn = tkinter.Button(window, text="Next(slow) >>", width=50, command=partial(play, 1))
btn.pack()

btn = tkinter.Button(window, text="<< Previous(fast)", width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="Next(fast) >>", width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Give out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give_not_out", width=50, command=not_out)
btn.pack()
window.mainloop()
'''
for index in np.ndindex(5,1,2):
    print(index)
'''