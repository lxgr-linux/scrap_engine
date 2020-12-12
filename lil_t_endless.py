#!/usr/bin/env python3
import scrap_engine as se
import time, os, threading, sys

os.system("")
width, height = os.get_terminal_size()
t=ev=v=0
g=0.015

class PanelItem(se.Object):
    def bump_left(self):
        self.remove()

    def bump(self, ob, x, y):
        ob.set(ob.x-1, ob.y)
        self.set(self.x-1, self.y)

map=se.Map(height-1, width+10, " ")
smap=se.Submap(map, 0, 0)

block=PanelItem("#")
panel=se.Square("#", 10, 1, ob_class=PanelItem)
ground=se.Square("#", map.width, 5)
player=se.Object("t")
h=se.Text("00 00")

block.add(map, map.width-12, map.height-6)
panel.add(map, map.width-12, map.height-10)
ground.add(map, 0, map.height-5)
player.add(map, round(smap.width/2), round(map.height/2))
h.add(smap, 0, 0)
moving=[panel, block]

def on_press(key):
    global ev
    ev=str(key)

if sys.platform == "linux":  # Use another (not on xserver relying) way to read keyboard input, to make this shit work in tty or via ssh, where no xserver is available
    def recogniser():
        global ev
        while True:
            a=os.popen('./reader.sh').read()
            if a == "\n":
                ev="Key.enter"
            else:
                ev="'"+a.rstrip()+"'"
else:
    from pynput.keyboard import Key, Listener
    def recogniser():
        global ev
        while True:
            with Listener(on_press=on_press) as listener:
                listener.join()

recognising=threading.Thread(target=recogniser)
recognising.daemon=True
recognising.start()

smap.remap()
smap.show(init=True)
time.sleep(0.5)
while True:
    for ob in map.obs:
        if player.y+1 == ob.y and player.x == ob.x:
            t=0
            v=0
    if ev == "Key.enter":
        v=-0.25
        ev=0
    if player.set(player.x, round(player.y-(v*(v/g)-1/2*g*(v/g)**2)-v*t+1/2*g*t**2)) != 0 and t != 0:
        player.set(player.x, player.y+1)
    t+=1
    for mov in moving:
        mov.set(mov.x-1, mov.y)
    if player.x < smap.x-1:
        exit()
    h.rechar((2-len(str(player.y)))*" "+str(player.y)+" "+str(map.height))
    time.sleep(0.05)
    smap.remap()
    smap.show()
