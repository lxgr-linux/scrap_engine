#!/usr/bin/python3

import scrap_engine as se
from pynput import keyboard
from pynput.keyboard import Key, Listener
import threading
import time

luisframe=0
luisview="r"
framenum=0
ev=0
obcount=0


map=se.Map(background=" ")
menumap=se.Map(background=" ")
lui=se.Object(char="L")
player=se.Object(char="T")
rock=se.Object(char="A")
menutext1=se.Text("Resume", menumap, int(round(menumap.width)/2-2), int(round(menumap.height)/2-3), float)
menutext2=se.Text("Exit", menumap, int(round(menumap.width)/2-2), int(round(menumap.height)/2+3), float)
menuind=se.Object("*")
menuind.add(menumap, int(round(menumap.width)/2-4), int(round(menumap.height)/2-3))

player.add(map, 0, 0)
lui.add(map, 20, 10)
rock.add(map, 10, 10)

class Pad(se.Object):
    def action(self):
        player.remove()

pad=Pad(char="i", state="float")
pad.add(map, 10, 20)

def menu():
    global ev
    ev=0
    menumap.blur_in(map)
    menumap.show(init=True)
    while True:
        if ev == "'m'":
            ev=0
            break
        elif ev == "'w'":
            menuind.set(menuind.x, menutext1.y)
            ev=0
        elif ev == "'s'":
            menuind.set(menuind.x, menutext2.y)
            ev=0
        elif ev == "Key.enter":
            if menuind.y == menutext1.y:
                return
            elif menuind.y == menutext2.y:
                exit()
            ev=0
        else:
            time.sleep(0.05)
        menumap.show()

def recogniser():
    global ev
    def on_press(key):
        global ev
        ev=str(key)

    while True:
        with Listener(on_press=on_press) as listener:
            listener.join()

recognising=threading.Thread(target=recogniser)
recognising.daemon = True
recognising.start()

text=se.Text("hello", map, 11, 3, float)

map.show()
while True:
    if ev == "'w'":
        print(1)
        player.set(player.x, player.y-1)
        ev=0
    elif ev == "'a'":
        player.set(player.x-1, player.y)
        ev=0
    elif ev == "'s'":
        player.set(player.x, player.y+1)
        ev=0
    elif ev == "'d'":
        player.set(player.x+1, player.y)
        ev=0
    elif ev == "'q'":
        exec("ob_"+str(obcount)+"=se.Object('A', state='solid')")
        exec("ob_"+str(obcount)+".add(map, player.x+1, player.y)")
        obcount+=1
        ev=0
    elif ev == "'m'":
        print(ev)
        menu()
        map.show(init=True)
        ev=0
    else:
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
