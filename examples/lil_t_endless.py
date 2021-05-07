#!/usr/bin/env python3
import scrap_engine as se
import time, os, threading, sys, random


class PanelItem(se.Object):
    def bump_left(self):
        global moving
        del moving[moving.index(self)]
        self.remove()

    def bump(self, ob, x, y):
        ob.set(ob.x-1, ob.y)
        self.set(self.x-1, self.y)


class Panel(se.Square):
    def init(self):
        for ob in self.obs:
            moving.append(ob)

def genpanel():
    global panelindex, test
    exec("panel_%s=Panel('#', 10, 1, ob_class=PanelItem)"%panelindex)
    exec("panel_%s.add(map, map.width-11, map.height-%i)"%(panelindex, random.randint(8,20)))
    exec("panel_%s.init()"%panelindex)
    panelindex+=1

def on_press(key):
    global ev
    ev=str(key)

if sys.platform == "linux":  # Use another (not on xserver relying) way to read keyboard input, to make this shit work in tty or via ssh, where no xserver is available
    def recogniser():
        import tty, sys, termios
        global ev, old_settings, termios, fd, do_exit

        do_exit=False
        fd=sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        while True:
            char=sys.stdin.read(1)
            if ord(char) == 13:
                ev="Key.enter"
            elif ord(char) == 32:
                ev="Key.space"
            else:
                ev="'"+char.rstrip()+"'"
            if ord(char) == 3 or do_exit:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                ev="exit"
else:
    from pynput.keyboard import Key, Listener
    def recogniser():
        global ev
        while True:
            with Listener(on_press=on_press) as listener:
                listener.join()


def main():
    global v, t, ev, g, framenum, genframe
    while True:
        nexty=lambda v,g,t : round(player.y-(v*(v/g)-1/2*g*(v/g)**2)-v*t+1/2*g*t**2)
        for ob in map.obs[1:]:
            if player.y+1 == ob.y and player.x == ob.x:
                t=0
                v=0
        for ob in map.obs[1:]:
            if player.y < ob.y < nexty(v,g,t) and ob.x == player.x+1:
                player.set(player.x, ob.y-1)
                t=0
                v=0
                break
            elif player.y > ob.y > nexty(v,g,t) and ob.x == player.x+1:
                player.set(player.x, ob.y+1)
                t=0
                v=0
                break
        if ev == "Key.space":
            v=-0.25
            ev=0
        elif ev == "exit":
            ev=0
            raise KeyboardInterrupt
        if player.set(player.x, nexty(v,g,t))!= 0 and t != 0:
            for ob in map.obs[1:]:
                if ob.x == player.x and ob.y == nexty(v,g,t):
                    v=0
            player.set(player.x, player.y+1)
        t+=1
        # exec("point_%s=PanelItem('*', 'float')"%panelindex)
        # exec("point_%s.add(map, player.x-1, player.y)"%panelindex)
        # exec("moving.append(point_%s)"%panelindex)
        # panelindex+=1
        for mov in moving:
            mov.set(mov.x-1, mov.y)
        if player.x < smap.x-1:
            exit()
        h.rechar((2-len(str(player.y)))*" "+str(player.y)+" "+str(map.height)+" "+str(player.y)+" "+str(nexty(v,g,t))+" "+str(player.y-nexty(v,g,t)))
        if genframe+15 == framenum:
            genpanel()
            genframe+=15
        time.sleep(0.05)
        smap.remap()
        smap.show()
        framenum+=1


os.system("")
width, height = os.get_terminal_size()
t=ev=v=0
g=0.015
panelindex=0
framenum=0
genframe=0

map=se.Map(height-1, width+12, " ")
smap=se.Submap(map, 0, 0)

player=se.Object("t")
block=PanelItem("#")
panel=Panel("#", 10, 1, ob_class=PanelItem)
ground=se.Square("#", map.width, 5)
h=se.Text("00 00")

player.add(map, round(smap.width/2), round(map.height/2))
block.add(map, map.width-11, map.height-6)
panel.add(map, map.width-11, map.height-10)
ground.add(map, 0, map.height-5)
h.add(smap, 0, 0)
moving=[ob for ob in panel.obs]+[block]

recognising=threading.Thread(target=recogniser)
recognising.daemon=True
recognising.start()

smap.remap()
smap.show(init=True)
main()
