#!/usr/bin/python3
# This software is licensed under the PGL v3 and comes with no license and so on....
# This software a proof of concept thingie for all features of the scrap_engine python module.
# It is also kind of an explaination for those, see the comments.
# Have fun!

import scrap_engine as se
from pynput.keyboard import Key, Listener
import threading
import time

# Some vars
luisframe=0
luisview="r"
framenum=0
ev=0
obcount=0

# Adding Maps
map=se.Map(background=" ") # Maps are kind of the "playground" which you can add Objects and Groups to
menumap=se.Map(background=" ")

# Creating Objects
lui=se.Object(char="L") # Objects are just objects that can be added to a map
player=se.Object(char="T")
rock=se.Object(char="A")
menuind=se.Object("*")

# Creating Groups
menutext1=se.Text("Resume", float) # The Text class creates a Group with the text in it
menutext2=se.Text("Exit", float)
text=se.Text("hello", float)
square1=se.Square("#", 2, 3, float)
square2=se.Square("#", 10, 5) # The Square class creates a square of a specific character

# Adding Objects and Groups to their Maps
menuind.add(menumap, int(round(menumap.width)/2-4), int(round(menumap.height)/2-3))
player.add(map, 0, 0)
lui.add(map, 20, 10)
rock.add(map, 10, 10)
menutext1.add(menumap, int(round(menumap.width)/2-2), int(round(menumap.height)/2-3))
menutext2.add(menumap, int(round(menumap.width)/2-2), int(round(menumap.height)/2+3))
text.add(map, 11, 3)
square2.add(map, 60, 10)
square1.add(map, 20, 20)

# Defining the "action" function for the Pad class wich is a modified Object class, which is triggert, when another Object is in the same spot as the Object it self
class Pad(se.Object):
    def action(self):
        player.remove()

# Defining and adding pad
pad=Pad(char="i", state="float") # The state="float" means that other Objects can be placed over it, default is "solid"
pad.add(map, 10, 20)

# Menu function
def menu():
    global ev
    ev=0
    menumap.blur_in(map) # Blurs in the map Map into the background of the menumap Map
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
        menumap.show() # Showing menumap

# Adding functions for capturing the keyboard and controling the game
def on_press(key):
    global ev
    ev=str(key)

def recogniser():
    global ev
    while True:
        with Listener(on_press=on_press) as listener:
            listener.join()

# Starting those in another thread
recognising=threading.Thread(target=recogniser)
recognising.daemon=True
recognising.start()

map.show() # showing map Map
while True:
    if ev == "'w'":
        player.set(player.x, player.y-1) # Doing something on keypress w
        ev=0
    elif ev == "'a'":
        player.set(player.x-1, player.y) # Doing something different on keypress a
        ev=0
    elif ev == "'s'":
        player.set(player.x, player.y+1) # Doing something more different on keypress s
        ev=0
    elif ev == "'d'":
        player.set(player.x+1, player.y) # Doing yet another different thing on keypress d
        ev=0
    elif ev == "'q'":
        # Creating and adding some Object on keypress q
        exec("ob_"+str(obcount)+"=se.Object('A', state='solid')")
        exec("ob_"+str(obcount)+".add(map, player.x+1, player.y)")
        obcount+=1
        ev=0
    elif ev == "'m'":
        menu() # Running the menu function on keypress q to open the menu
        map.show(init=True) # The init=True option ensures, the map Map is drawn after closing the menu, even if no changes accured in the map
        ev=0
    else:
        time.sleep(0.05) # Else just wait 0.05 seconds
    # Let lui run
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
    map.show() # Draw the frame
    framenum+=1
