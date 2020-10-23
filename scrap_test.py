#!/usr/bin/python3

import scrap_engine as se
from pynput import keyboard
import threading
import time
import os

ev=0
obcount=0

map=se.Map(background=" ")
player=se.Object(char="T")
rock=se.Object(char="A")

player.add(map, 0,0)

class Pad(se.Object):
    def action(self):
        player.remove()

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

pad=Pad(char="i", state="float")

rock.add(map, 10, 10)

pad.add(map, 10, 20)

t=threading.Thread(target=recogniser)
t.start()

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
    map.show()
