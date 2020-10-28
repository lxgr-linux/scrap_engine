#!/usr/bin/python3

import scrap_engine as se
from pynput.keyboard import Key, Listener
import threading
import time

framenum=0
ev=0
walkframe=0

map=se.Map(background=" ")
start=se.Object("#")
start.add(map, round(map.width/2), round(map.height/2))
start.direction="t"

def on_press(key):
    global ev
    ev=str(key)

def recogniser():
    global ev
    while True:
        with Listener(on_press=on_press) as listener:
            listener.join()

recognising=threading.Thread(target=recogniser)
recognising.daemon=True
recognising.start()

map.show()
while True:
    if ev == "'w'":
        start.direction="t"
        ev=0
    elif ev == "'a'":
        start.direction="l"
        ev=0
    elif ev == "'s'":
        start.direction="b"
        ev=0
    elif ev == "'d'":
        start.direction="r"
        ev=0
    else:
        time.sleep(0.01)
    if walkframe+5 == framenum:
        if start.direction == "t":
            start.set(start.x, start.y-1)
        if start.direction == "b":
            start.set(start.x, start.y+1)
        if start.direction == "l":
            start.set(start.x-1, start.y)
        if start.direction == "r":
            start.set(start.x+1, start.y)
        walkframe+=5
    map.show()
    framenum+=1
