#!/usr/bin/python3
# This software is licensed under the PGL v3 and comes with no warranty and so on....
# This software a proof of concept thingie for all features of the scrap_engine python module.
# It is also kind of an explaination for those, see the comments.
# Have fun!

import scrap_engine as se
from pynput.keyboard import Key, Listener
import threading, time, os

# Because of some wierd windows shit this is required to let colors work
os.system("")

# Some vars
luisframe=0
luisview="r"
framenum=0
bullet_num=0
bullets=[]
ev=ev2=0
obcount=0

# Adding Maps
map=se.Map(width=200, background=" ") # Maps are kind of the "playground" which you can add Objects and Groups to
smap=se.Submap(map, 0,0) # This one is just a small part of the real (map) Map
menumap=se.Map(background=" ")
howtomap=se.Map(background=" ")

# Defining the "action" function for the Pad class wich is a modified Object class, which is triggert, when another Object is in the same spot as the Object it self
class Pad(se.Object):
    def action(self, ob):
        ob.remove()

# Same as above, but the player is set to the middle of the map when he bumps into an solid Object
class Player(se.Object):
    def bump(self, ob, x, y):
        self.set(round(self.map.width/2), round(self.map.height/2))
        if self.char == "T":
            self.rechar("t")
        elif self.char == "t":
            self.rechar("T")
        elif self.char == "F":
            self.rechar("f")
        elif self.char == "f":
            self.rechar("F")

class Bullet(se.Object):
    def bump_action(self):
        for i in range(len(bullets)):
            if bullets[i] == self:
                del bullets[i]
                break
        self.remove()

    def bump(self, ob, x, y):
        ob.remove()
        self.bump_action()

    def bump_right(self):
        self.bump_action()

    def bump_left(self):
        self.bump_action()

    def bump_top(self):
        self.bump_action()

    def bump_bottom(self):
        self.bump_action()

def shoot(ob):
    exec("bullet"+str(bullet_num)+"=Bullet('*', state='float')")
    exec("bullet"+str(bullet_num)+".direction=ob.direction")
    if ob.direction == "t":
        exec("bullet"+str(bullet_num)+".add(map, ob.x, ob.y-1)")
    elif ob.direction == "l":
        exec("bullet"+str(bullet_num)+".add(map, ob.x-1, ob.y)")
    elif ob.direction == "b":
        exec("bullet"+str(bullet_num)+".add(map, ob.x, ob.y+1)")
    elif ob.direction == "r":
        exec("bullet"+str(bullet_num)+".add(map, ob.x+1, ob.y)")
    exec("bullets.append(bullet"+str(bullet_num)+")")

# Creating Objects
lui=se.Object(char="L") # Objects are just objects that can be added to a map
rock=se.Object(char="A")
menuind=se.Object("*")
player=Player(char="T")
player0=Player(char="F")
pad=Pad(char="i", state="float") # The state="float" means that other Objects can be placed over it, default is "solid"
testob=se.Object(char="t")
testob2=se.Object(char="t")
testtext=se.Text("Hey!")
box=se.Box(10, 10)
box.add_ob(testob, 5, 5)
box.add_ob(testob2, 6, 6)
box.add_ob(testtext, 7, 7)
box.add(map, 100, 10)

# Creating Groups
menutext1=se.Text("Resume", float) # The Text class creates a Group with the text in it
menutext2=se.Text("How to play", float)
menutext3=se.Text("Exit", float)
howtotext=se.Text("How to play this game ou ask?\nIf you haven't already understood,\nyou can move your character with w, a, s and d.\nTo open the menu press m", float)
text=se.Text("hello", float, esccode="\033[1m")
text2=se.Text("this\nis\nmultiline text!", float)
square1=se.Square("#", 2, 3, float)
square2=se.Square("#", 10, 5) # The Square class creates a square of a specific character

# Adding Objects and Groups to their Maps
player.add(map, 0, 0)
player0.add(map, 0, 1)
lui.add(map, 20, 10)
rock.add(map, 10, 10)
howtotext.add(howtomap, int(round(howtomap.width-47)/2), int(round(howtomap.height/2)-2))
menutext1.add(menumap, int(round(menumap.width/2)-2), int(round(menumap.height/2)-4))
menutext3.add(menumap, int(round(menumap.width/2)-2), int(round(menumap.height/2)+4))
menutext2.add(menumap, int(round(menumap.width/2)-2), int(round(menumap.height/2)))
menuind.add(menumap, int(round(menumap.width/2)-4), menutext1.y)
text.add(map, 11, 3)
text2.add(map, 11, 4)
square2.add(map, 60, 10)
square1.add(map, 20, 20)
pad.add(map, 10, 20)
player.direction="r"
player0.direction="r"

# Menu function
def menu():
    global ev
    ev=0
    menuind.index=1
    menumap.blur_in(smap) # Blurs in the map Map into the background of the menumap Map
    menumap.show(init=True)
    while True:
        if ev == "'m'":
            ev=0
            break
        elif ev == "'w'":
            if menuind.index != 1:
                menuind.index-=1
            exec("menuind.set(menuind.x, menutext"+str(menuind.index)+".y)")
            ev=0
        elif ev == "'s'":
            if menuind.index != 3:
                menuind.index+=1
            exec("menuind.set(menuind.x, menutext"+str(menuind.index)+".y)")
            ev=0
        elif ev == "Key.enter":
            if menuind.y == menutext1.y:
                return
            elif menuind.y == menutext2.y:
                howtoplay()
                menumap.show(init=True)
            elif menuind.y == menutext3.y:
                exit()
            ev=0
        else:
            time.sleep(0.05)
        menumap.show() # Showing menumap

# How to play menuentry function
def howtoplay():
    global ev
    ev=0
    #howtomap.blur_in(menumap) # Blurs in the menumap Map into the background of the howtomap Map
    howtomap.show(init=True)
    while True:
        if ev == "'m'":
            ev=0
            break
        else:
            time.sleep(0.05)
        howtomap.show() # Showing howtomap

# Adding functions for capturing the keyboard and controling the game, you may recicle this in your applications
def on_press(key):
    global ev, ev2
    if str(key) in ["'w'", "'a'", "'s'", "'d'", "'e'", "'q'", "Key.space"]:
        ev=str(key)
    elif str(key) in ["Key.up", "Key.left", "Key.down", "Key.right", "'#'"]:
        ev2=str(key)

def recogniser():
    global ev, ev2
    while True:
        with Listener(on_press=on_press) as listener:
            listener.join()

# Starting those in another thread
recognising=threading.Thread(target=recogniser)
recognising.daemon=True
recognising.start()

smap.remap()
smap.show() # showing smap Map
while True:
    if ev == "'w'":
        player.direction="t"
        player.set(player.x, player.y-1) # Doing something on keypress w
        ev=0
    elif ev == "'a'":
        player.direction="l"
        player.set(player.x-1, player.y) # Doing something different on keypress a
        ev=0
    elif ev == "'s'":
        player.direction="b"
        player.set(player.x, player.y+1) # Doing something more different on keypress s
        ev=0
    elif ev == "'d'":
        player.direction="r"
        player.set(player.x+1, player.y) # Doing yet another different thing on keypress d
        ev=0
    elif ev2 == "Key.up":
        player0.direction="t"
        player0.set(player0.x, player0.y-1) # Doing something on keypress w
        ev2=0
    elif ev2 == "Key.left":
        player0.direction="l"
        player0.set(player0.x-1, player0.y) # Doing something different on keypress a
        ev2=0
    elif ev2 == "Key.down":
        player0.direction="b"
        player0.set(player0.x, player0.y+1) # Doing something more different on keypress s
        ev2=0
    elif ev2 == "Key.right":
        player0.direction="r"
        player0.set(player0.x+1, player0.y) # Doing yet another different thing on keypress d
        ev2=0
    elif ev == "'e'":
        text2.rechar("thus\nus\nmultiline mext!")
        square2.rechar("A") # Doing some weird shit on keypress e
        ev=0
    elif ev == "'q'":
        # Creating and adding some Object on keypress q
        exec("ob_"+str(obcount)+"=se.Object('A', state='solid')")
        exec("ob_"+str(obcount)+".add(map, player.x+1, player.y)")
        obcount+=1
        ev=0
    elif ev == "'m'":
        menu() # Running the menu function on keypress q to open the menu
        smap.show(init=True) # The init=True option ensures, the map Map is drawn after closing the menu, even if no changes accured in the map
        smap.remap()
        ev=0
    elif ev == "Key.space":
        shoot(player)
        ev=0
    elif ev2 == "'#'":
        shoot(player0)
        ev2=0
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
    for ob in [player, player0]:
        if ob.x+5 > smap.x+smap.width:
            smap.set(smap.x+1 ,smap.y)
        if ob.x < smap.x+5:
            smap.set(smap.x-1 ,smap.y)
    for ob in bullets:
        if ob.direction == "t":
            ob.set(ob.x, ob.y-1)
        elif ob.direction == "l":
            ob.set(ob.x-1, ob.y)
        elif ob.direction == "b":
            ob.set(ob.x, ob.y+1)
        elif ob.direction == "r":
            ob.set(ob.x+1, ob.y)
    smap.remap()
    smap.show() # Draw the frame
    framenum+=1
