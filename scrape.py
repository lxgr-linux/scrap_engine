#!/usr/bin/env python3
# This is snake, but worse

import scrap_engine as se
import threading, time, random, os, sys
from pathlib import Path


class Start_master(se.Object):
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

    def pull_ob(self):
        dead()

class Start_easy(Start_master):
    def bump_action(self):
        if self.x == 0 and self.direction == 'l':
            self.set(self.map.width-1, self.y)
        elif self.x == self.map.width-1 and self.direction == 'r':
            self.set(0, self.y)
        elif self.y == 0 and self.direction == 't':
            self.set(self.x, self.map.height-1)
        elif self.y == self.map.height-1 and self.direction == 'b':
            self.set(self.x, 0)

    def bump(self, ob, x, y):
        dead()


class Apple(se.Object):
    def action(self, ob):
        exec("runner"+str(len(ob.group.obs))+"=Start(ob.group.symbol)")
        exec("runner"+str(len(ob.group.obs))+".add(map, ob.group.obs[-1].oldx, ob.group.obs[-1].oldy)")
        exec("ob.group.add_ob(runner"+str(len(ob.group.obs))+")")
        apples.rem_ob(self)
        self.remove()


class Berry(se.Object):
    def action(self, ob):
        global walkstep, walkframe
        ob.group.obs[-1].remove()
        del ob.group.obs[-1]
        if ob.group.walkstep > 1:
            ob.group.walkframe+=1
            ob.group.walkstep-=1
        berrys.rem_ob(self)
        self.remove()

def applegen():
    global inc
    x=random.randint(0, map.width-1)
    y=random.randint(0, map.height-1)
    if map.obmap[y][x] != []:
            return
    exec("apple"+str(inc)+"=Apple('\033[32;1ma\033[0m', state='float')")
    exec("apple"+str(inc)+".add(map, x, y)")
    exec("apples.add_ob(apple"+str(inc)+")")
    inc+=1

def berrygen():
    global inc
    x=random.randint(0, map.width-1)
    y=random.randint(0, map.height-1)
    if map.obmap[y][x] != []:
            return
    exec("berry"+str(inc)+"=Berry('\033[31;1ms\033[0m', state='float')")
    exec("berry"+str(inc)+".add(map, x, y)")
    exec("berrys.add_ob(berry"+str(inc)+")")
    inc+=1

def blockgen():
    global inc
    x=random.randint(0, map.width-1)
    y=random.randint(0, map.height-1)
    if map.obmap[y][x] != []:
            return
    exec("block"+str(inc)+"=se.Object('8', state='solid')")
    exec("block"+str(inc)+".add(map, x, y)")
    inc+=1

def exiter():
    global do_exit
    do_exit=True
    exit()

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


def level_normal():
    global genframe0, genframe1, framenum
    if genframe0+150 == framenum:
        applegen()
        genframe0+=150
    if genframe1+400 == framenum:
        berrygen()
        genframe1+=400

def level_single():
    if len(apples.obs) == 0:
        applegen()
    if len(berrys.obs) == 0:
        berrygen()

def level_easy():
    global genframe0, framenum
    if genframe0+150 == framenum:
        applegen()
        genframe0+=150

def level_hard():
    global genframe0, genframe1, framenum, genframe2
    if genframe0+200 == framenum:
        applegen()
        genframe0+=200
    if genframe1+200 == framenum:
        berrygen()
        genframe1+=200
    if genframe2+300 == framenum:
        blockgen()
        genframe2+=300

def level_multi():
    level_normal()

def level_normal_init():
    global Start
    Start=Start_master

def level_single_init():
    global Start
    Start=Start_master

def level_easy_init():
    global Start
    Start=Start_easy

def level_hard_init():
    global Start, genframe2, genframe1
    Start=Start_master
    genframe2=0
    genframe1=75

def level_multi_init():
    global Start
    class Start(Start_easy):
        def bump(self, ob, x, y):
            global suicide
            if self.group == ob.group:
                suicide=self.group
            dead()

    snake2=se.ObjectGroup([])
    snake2.symbol="\033[34m#\033[0m"
    start2=Start(snake2.symbol)
    start2.add(map, round(map.width/2-5), round(map.height/2))
    runner2_0=Start(snake2.symbol)
    runner2_1=Start(snake2.symbol)
    runner2_0.add(map, round(map.width/2-5), round(map.height/2)+1)
    runner2_1.add(map, round(map.width/2-5), round(map.height/2)+2)
    start2.direction="t"
    start2.key_t="'i'"
    start2.key_b="'k'"
    start2.key_l="'j'"
    start2.key_r="'l'"
    snake2.add_obs([start2, runner2_0, runner2_1])
    snake2.color="blue"
    snake2.walkframe=0
    snake2.walkstep=5
    snakes.append(snake2)

def menuresize(map, box):
    width, height = os.get_terminal_size()
    if map.width != width or map.height != height-1:
        box.set(0, 0)
        map.resize(height-1, width, " ")
        box.set(round((map.width-box.width)/2), 1+round((map.height-box.height)/2))

def mapresize():
    width, height = os.get_terminal_size()
    if map.width != width or map.height != height-1:
        map.resize(height-1, width, " ")

def dead():
    global ev, scoretext, highscoretext, mode, modeindex, data, suicide
    ev=0
    deadmenuind.index=1
    menuresize(deadmap, deadbox)

    home=str(Path.home())
    Path(home+"/.cache/scrape").mkdir(parents=True, exist_ok=True)
    Path(home+"/.cache/scrape/scrape").touch(exist_ok=True)

    if mode == "multi":
        scores=sorted([len(group.obs) for group in snakes])
        score=scores[-1]
        if suicide != "":
            for group in snakes:
                if suicide != group:
                    score_text=group.color+" won with "+str(len(group.obs))+" points"
        elif scores[0] == scores[-1]:
            score_text="Both players scored "+str(score)+" -- tie"
        else:
            for group in snakes:
                if len(group.obs) == score:
                    score_text=group.color+" won with "+str(score)+" points"
        suicide=""
    else:
        score=len(snake.obs)
        score_text="You scored "+str(score)+" points"
    datas="{"
    for i in modes:
        datas+="'"+i+"' : 0,"
    datas+="}"
    exec("global data; data="+datas)
    with open(home+"/.cache/scrape/scrape", "r") as file:
        file_content=file.read()
        exec("global data; "+file_content)
        if file_content == "" or (mode not in data) or data[mode] < score:
            data[mode]=score
            with open(home+"/.cache/scrape/scrape", "w+") as file1:
                file1.write("data="+str(data))

    scoretext.rechar(score_text)
    highscoretext.rechar("Highscore: "+str(data[mode]))
    deadbox.set_ob(scoretext, round((deadbox.width-len(scoretext.text))/2), 2)
    deadbox.set_ob(highscoretext, round((deadbox.width-1-len(highscoretext.text))/2), 3)
    deadmap.blur_in(map, esccode="\033[31m")
    deadmap.show(init=True)
    while True:
        if ev == "'m'":
            ev=0
            exiter()
        elif ev == "exit":
            ev=0
            raise KeyboardInterrupt
        elif ev == "'w'":
            if deadmenuind.index != 0:
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
                exiter()
            elif deadmenuind.ry == deadmenutext0.ry:
                modeindex=modeindex+1 if modeindex < len(modes)-1 else 0
                mode=modes[modeindex]
                deadmenutext0.rechar("Mode: "+mode)
                deadbox.set_ob(deadmenuind, 0, 0)
                deadbox.set_ob(deadmenutext0, round((deadbox.width-len("Mode: "+mode))/2), 7)
                deadbox.set_ob(deadmenuind, deadmenutext0.rx-2, deadmenutext0.ry)
            ev=0
        else:
            time.sleep(0.05)
        menuresize(deadmap, deadbox)
        deadmap.show()

def menu():
    global ev, curscore
    ev=0
    menuind.index=1
    score=0
    for group in snakes:
        score+=len(group.obs)
    menuresize(menumap, menubox)
    curscore.rechar("Current score: "+str(score)+" points")
    menubox.set_ob(curscore, 1+round((menubox.width-22-len(str(score)))/2), 2)
    menumap.blur_in(map)
    menumap.show(init=True)
    while True:
        if ev == "'m'":
            ev=0
            break
        elif ev == "exit":
            ev=0
            raise KeyboardInterrupt
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
                exiter()
            ev=0
        else:
            time.sleep(0.05)
        menuresize(menumap, menubox)
        menumap.show()

def main():
    global ev, inc, map, walkstep, walkframe, snake, genframe0, genframe1, framenum, apples, berrys, start, snakes
    genframe0=genframe1=inc=framenum=0

    snakes=[]
    width, height = os.get_terminal_size()
    map=se.Map(height-1, width, " ")
    exec("level_"+mode+"_init()")

    snake=se.ObjectGroup([])
    snake.symbol="#"
    start=Start(snake.symbol)
    runner0=Start(snake.symbol)
    runner1=Start(snake.symbol)
    runner0.add(map, round(map.width/2), round(map.height/2)+1)
    runner1.add(map, round(map.width/2), round(map.height/2)+2)
    start.add(map, round(map.width/2), round(map.height/2))
    snake.add_obs([start, runner0, runner1])
    start.key_t="'w'"
    start.key_b="'s'"
    start.key_l="'a'"
    start.key_r="'d'"
    start.is_set=False
    snake.color="white"
    snake.walkframe=0
    snake.walkstep=5
    snakes.append(snake)
    apples=se.ObjectGroup([])
    berrys=se.ObjectGroup([])

    start.direction="t"
    map.show()
    while True:
        for group in snakes:
            for arr in [[group.obs[0].key_t, "b", "t"], [group.obs[0].key_l, "r", "l"], [group.obs[0].key_b, "t", "b"], [group.obs[0].key_r, "l", "r"]]:
                if ev == arr[0]:
                    if group.obs[0].direction != arr[1] and not group.obs[0].is_set:
                        group.obs[0].direction=arr[2]
                        group.obs[0].is_set=True
                    ev=0
        if ev == "'m'":
            menu()
            mapresize()
            map.show(init=True)
            ev=0
        elif ev == "exit":
            ev=0
            raise KeyboardInterrupt
        elif ev == "'e'":
            ev=0
            dead()
        else:
            time.sleep(0.01)
        start.oldx=start.oldy=0
        for group in snakes:
            if group.walkframe+group.walkstep == framenum:
                oldx=group.obs[0].x
                oldy=group.obs[0].y
                if group.obs[0].direction == "t":
                    group.obs[0].set(group.obs[0].x, group.obs[0].y-1)
                elif group.obs[0].direction == "b":
                    group.obs[0].set(group.obs[0].x, group.obs[0].y+1)
                elif group.obs[0].direction == "l":
                    group.obs[0].set(group.obs[0].x-1, group.obs[0].y)
                elif group.obs[0].direction == "r":
                    group.obs[0].set(group.obs[0].x+1, group.obs[0].y)
                if len(group.obs) == 0:
                    dead()
                group.obs[0].oldx=oldx
                group.obs[0].oldy=oldy
                for ob in group.obs[1:]:
                    ob.oldx=ob.x
                    ob.oldy=ob.y
                    ob.set(oldx, oldy)
                    oldx=ob.oldx
                    oldy=ob.oldy
                group.walkframe+=group.walkstep
                group.obs[0].is_set=False
        exec("level_"+mode+"()")
        mapresize()
        map.show()
        framenum+=1

modeindex=0
mode="normal"
modes=["normal", "single", "easy", "hard", "multi"]
# objects for dead
deadmap=se.Map(background=" ")
deadbox=se.Box(13, 28)
deadtext=se.Text("You dead!")
scoretext=se.Text("You scored 0 points")
highscoretext=se.Text("Highscore: 0")
deadmenutext0=se.Text("Mode: "+mode)
deadmenutext1=se.Text("Try again")
deadmenutext2=se.Text("Exit")
deadmenuind=se.Object("*")
deadbox.add_ob(deadtext, 9, 0)
deadbox.add_ob(scoretext, round((deadbox.width-len(scoretext.text))/2), 2)
deadbox.add_ob(highscoretext, round((deadbox.width-1-len(highscoretext.text))/2), 3)
deadbox.add_ob(deadmenutext0, round((deadbox.width-len("Mode: "+mode))/2), 7)
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
menubox.add_ob(curscore, 3, 2)
menubox.add_ob(menutext1, 11, 7)
menubox.add_ob(menutext2, 11, 9)
menubox.add_ob(menutext3, 12, 11)
menubox.add_ob(menuind, 9, 7)
menubox.add(menumap, round((menumap.width-menubox.width)/2), 1+round((menumap.height-menubox.height)/2))

suicide=""
ev=0
os.system("")
recognising=threading.Thread(target=recogniser)
recognising.daemon=True
recognising.start()
try:
    main()
except KeyboardInterrupt:
    print("Exited by user")
