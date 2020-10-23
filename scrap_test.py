#!/usr/bin/python3

import scrap_engine as se
from pynput import keyboard
import threading
import time
import os

luisframe=0
luisview="r"
framenum=0
ev=0
obcount=0


map=se.Map(background=" ")
lui=se.Object(char="L")
player=se.Object(char="T")
rock=se.Object(char="A")

player.add(map, 0,0)
lui.add(map, 20, 10)
rock.add(map, 10, 10)

class Pad(se.Object):
    def action(self):
        player.remove()

pad=Pad(char="i", state="float")
pad.add(map, 10, 20)

def recogniser():
    global ev
    while True:
        with keyboard.Events() as events:
        # Block for as much as possible
            event = events.get(1e6)
            if event.key == keyboard.KeyCode.from_char('w'):
                ev="w"
            elif event.key == keyboard.KeyCode.from_char('a'):
                ev="a"
            elif event.key == keyboard.KeyCode.from_char('s'):
                ev="s"
            elif event.key == keyboard.KeyCode.from_char('d'):
                ev="d"
            elif event.key == keyboard.KeyCode.from_char('q'):
                ev="q"

recognising=threading.Thread(target=recogniser)
recognising.start()

map.show()

while True:
    if ev == 'w':
        player.set(player.x, player.y-1)
        ev=0
    elif ev == 'a':
        player.set(player.x-1, player.y)
        ev=0
    elif ev == 's':
        player.set(player.x, player.y+1)
        ev=0
    elif ev == 'd':
        player.set(player.x+1, player.y)
        ev=0
    elif ev == 'q':
        exec("ob_"+str(obcount)+"=se.Object('A', state='solid')")
        exec("ob_"+str(obcount)+".add(map, player.x+1, player.y)")
        obcount+=1
        ev=0
    elif ev == 0:
        time.sleep(0.05)
    # lui
    if luisframe+20 == framenum:
        if lui.x == 20 and luisview == "l":
            lui.set(19, 10)
            luisview="r"
        elif lui.x == 20 and luisview == "r":
            lui.set(21, 10)
            luisview="l"
        elif lui.x == 19 or lui.x == 21:
            lui.set(20, 10)
        luisframe+=20

    map.show()
    framenum+=1
