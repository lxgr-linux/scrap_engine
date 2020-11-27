#!/usr/bin/python3
# This is snake, but worse

import scrap_engine as se
import threading, time, random, os, sys
from pathlib import Path


class Start(se.Object):
    def bump_action(self):
        dead()

    def bump(self, ob, x, y):
        self.bump_action()

    def bump_right(self):
        self.bump_action()

    def bump_left(self):
        self.bump_action()

    def bump_top(self):
        self.bump_action()

    def bump_bottom(self):
        self.bump_action()


class Apple(se.Object):
    def action(self, ob):
        exec("runner"+str(len(ob.group.obs))+"=se.Object('#')")
        exec("runner"+str(len(ob.group.obs))+".add(map, ob.group.obs[-1].oldx, ob.group.obs[-1].oldy)")
        exec("ob.group.add_ob(runner"+str(len(ob.group.obs))+")")
        self.remove()


class Berry(se.Object):
    def action(self, ob):
        global walkstep, walkframe
        ob.group.obs[-1].remove()
        del ob.group.obs[-1]
        if walkstep > 1:
            walkframe+=1
            walkstep-=1
        self.remove()

def applegen():
    global apple_num
    x=random.randint(0, map.width-1)
    y=random.randint(0, map.height-1)
    for ob in map.obs:
        if ob.x == x and ob.y == y:
            return
    exec("apple"+str(apple_num)+"=Apple('\033[32;1ma\033[0m', state='float')")
    exec("apple"+str(apple_num)+".add(map, x, y)")
    apple_num+=1

def berrygen():
    global berry_num
    x=random.randint(0, map.width-1)
    y=random.randint(0, map.height-1)
    for ob in map.obs:
        if ob.x == x and ob.y == y:
            return
    exec("berry"+str(berry_num)+"=Berry('\033[31;1ms\033[0m', state='float')")
    exec("berry"+str(berry_num)+".add(map, x, y)")
    berry_num+=1

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

def menuresize(map, box):
    width, height = os.get_terminal_size()
    if map.width != width or map.height != height-1:
        box.set(0, 0)
        map.resize(height-1, width, " ")
        box.set(round((map.width-box.width)/2), 1+round((map.height-box.height)/2))

def mapresize():
    width, height = os.get_terminal_size()
    if map.width != width or map.height != height-1:
        try:
            map.resize(height-1, width, " ")
        except:
            pass

def dead():
    global ev, scoretext, highscoretext
    ev=0
    deadmenuind.index=1
    menuresize(deadmap, deadbox)

    home=str(Path.home())
    Path(home+"/.cache/scrape").mkdir(parents=True, exist_ok=True)
    Path(home+"/.cache/scrape/scrape").touch(exist_ok=True)
    with open(home+"/.cache/scrape/scrape", "r") as file:
        file_content=file.read()
        if file_content == "" or int(file_content) < len(snake.obs):
            with open(home+"/.cache/scrape/scrape", "w+") as file1:
                file1.write(str(len(snake.obs)))
            file_content=str(len(snake.obs))

    deadbox.rem_ob(scoretext)
    deadbox.rem_ob(highscoretext)
    scoretext.remove()
    highscoretext.remove()
    scoretext=se.Text("You scored "+str(len(snake.obs))+" points")
    highscoretext=se.Text("Highscore: "+str(file_content))
    deadbox.add_ob(scoretext, round((deadbox.width-18-len(str(len(snake.obs))))/2), 2)
    deadbox.add_ob(highscoretext, round((deadbox.width-12-len(str(file_content)))/2), 3)
    deadmap.blur_in(map, esccode="\033[31m")
    deadmap.show(init=True)
    while True:
        if ev == "'m'":
            ev=0
            exit()
        elif ev == "'w'":
            if deadmenuind.index != 1:
                deadmenuind.index-=1
            exec("deadbox.set_ob(deadmenuind, deadmenutext"+str(deadmenuind.index)+".rx-2, deadmenutext"+str(deadmenuind.index)+".ry)")
            ev=0
        elif ev == "'s'":
            if deadmenuind.index != 2:
                deadmenuind.index+=1
            exec("deadbox.set_ob(deadmenuind, deadmenutext"+str(deadmenuind.index)+".rx-2, deadmenutext"+str(deadmenuind.index)+".ry)")
            ev=0
        elif ev == "Key.enter":
            if deadmenuind.ry == deadmenutext1.ry:
                main()
            elif deadmenuind.ry == deadmenutext2.ry:
                exit()
            ev=0
        else:
            time.sleep(0.05)
        menuresize(deadmap, deadbox)
        deadmap.show()

def menu():
    global ev, curscore
    ev=0
    menuind.index=1
    menuresize(menumap, menubox)
    menubox.rem_ob(curscore)
    curscore.remove()
    curscore=se.Text("Current score: "+str(len(snake.obs))+" points")
    menubox.add_ob(curscore, 1+round((menubox.width-22-len(str(len(snake.obs))))/2), 2)
    menumap.blur_in(map)
    menumap.show(init=True)
    while True:
        if ev == "'m'":
            ev=0
            break
        elif ev == "'w'":
            if menuind.index != 1:
                menuind.index-=1
            exec("menubox.set_ob(menuind, menutext"+str(menuind.index)+".rx-2, menutext"+str(menuind.index)+".ry)")
            ev=0
        elif ev == "'s'":
            if menuind.index != 3:
                menuind.index+=1
            exec("menubox.set_ob(menuind, menutext"+str(menuind.index)+".rx-2, menutext"+str(menuind.index)+".ry)")
            ev=0
        elif ev == "Key.enter":
            if menuind.ry == menutext1.ry:
                return
            elif menuind.ry == menutext2.ry:
                main()
            elif menuind.ry == menutext3.ry:
                exit()
            ev=0
        else:
            time.sleep(0.05)
        menuresize(menumap, menubox)
        menumap.show()

def main():
    global ev, apple_num, berry_num, map, walkstep, walkframe, snake
    walkframe=genframe0=genframe1=apple_num=berry_num=framenum=0
    walkstep=5

    width, height = os.get_terminal_size()
    map=se.Map(height-1, width, " ")

    start=Start("#")
    runner0=se.Object("#")
    runner1=se.Object("#")
    start.add(map, round(map.width/2), round(map.height/2))
    runner0.add(map, round(map.width/2), round(map.height/2)+1)
    runner1.add(map, round(map.width/2), round(map.height/2)+2)
    snake=se.ObjectGroup([start, runner0, runner1])

    start.direction="t"

    map.show()
    set=False
    while True:
        for arr in [["'w'", "b", "t"], ["'a'", "r", "l"], ["'s'", "t", "b"], ["'d'", "l", "r"]]:
            if ev == arr[0]:
                if start.direction != arr[1] and not set:
                    start.direction=arr[2]
                    set=True
                ev=0
        if ev == "'m'":
            menu()
            mapresize()
            map.show(init=True)
            ev=0
        else:
            time.sleep(0.01)
        if walkframe+walkstep == framenum:
            start.oldx=oldx=start.x
            start.oldy=oldy=start.y
            if start.direction == "t":
                start.set(start.x, start.y-1)
            elif start.direction == "b":
                start.set(start.x, start.y+1)
            elif start.direction == "l":
                start.set(start.x-1, start.y)
            elif start.direction == "r":
                start.set(start.x+1, start.y)
            for ob in snake.obs[1:]:
                ob.oldx=ob.x
                ob.oldy=ob.y
                ob.set(oldx, oldy)
                oldx=ob.oldx
                oldy=ob.oldy
            if len(snake.obs) == 0:
                dead()
            set=False
            walkframe+=walkstep
        if genframe0+150 == framenum:
            applegen()
            genframe0+=150
        if genframe1+400 == framenum:
            berrygen()
            genframe1+=400
        mapresize()
        map.show()
        framenum+=1

# objects for dead
deadmap=se.Map(background=" ")
deadbox=se.Box(13, 28)
deadtext=se.Text("You dead!")
scoretext=se.Text("You scored 0 points")
highscoretext=se.Text("Highscore: 0")
deadmenutext1=se.Text("Try again")
deadmenutext2=se.Text("Exit")
deadmenuind=se.Object("*")
deadbox.add_ob(deadtext, 9, 0)
deadbox.add_ob(scoretext, 3, 2)
deadbox.add_ob(highscoretext, 7, 3)
deadbox.add_ob(deadmenutext1, 9, 9)
deadbox.add_ob(deadmenutext2, 11, 11)
deadbox.add_ob(deadmenuind, 7, 9)
deadbox.add(deadmap, round((deadmap.width-deadbox.width)/2), 1+round((deadmap.height-deadbox.height)/2))

# Objects for menu
menumap=se.Map(background=" ")
menubox=se.Box(13, 28)
menutext=se.Text("Menu:")
curscore=se.Text("Current score: 0 points")
menutext1=se.Text("Resume")
menutext2=se.Text("Restart")
menutext3=se.Text("Exit")
menuind=se.Object("*")
menubox.add_ob(menutext, 12, 0)
menubox.add_ob(curscore, 2, 2)
menubox.add_ob(menutext1, 11, 7)
menubox.add_ob(menutext2, 11, 9)
menubox.add_ob(menutext3, 12, 11)
menubox.add_ob(menuind, 9, 7)
menubox.add(menumap, round((menumap.width-menubox.width)/2), 1+round((menumap.height-menubox.height)/2))

ev=0
os.system("")
recognising=threading.Thread(target=recogniser)
recognising.daemon=True
recognising.start()
main()
