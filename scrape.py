#!/usr/bin/python3

import scrap_engine as se
from pynput.keyboard import Key, Listener
import threading
import time
import random

ev=0

class Start(se.Object):
    def bump_action(self):
        # snake.remove()
        dead()

    def bump(self, x, y):
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
    def action(self):
        global runner_num
        exec("runner"+str(runner_num)+"=se.Object('#')")
        exec("runner"+str(runner_num)+".add(map, snake.obs[-1].oldx, snake.obs[-1].oldy)")
        exec("snake.add_ob(runner"+str(runner_num)+")")
        runner_num+=1
        self.remove()

def applegen():
    global apple_num, genframe
    x=random.randint(0, map.width-1)
    y=random.randint(0, map.height-1)
    for ob in map.obs:
        if ob.x == x and ob.y == y:
            return
    exec("apple"+str(apple_num)+"=Apple('a', state='float')")
    exec("apple"+str(apple_num)+".add(map, x, y)")
    apple_num+=1


def on_press(key):
    global ev
    ev=str(key)

def recogniser():
    global ev
    while True:
        with Listener(on_press=on_press) as listener:
            listener.join()

deadmap=se.Map(background=" ")

deadmenutext1=se.Text("Try again")
deadmenutext2=se.Text("Exit")
deadtext=se.Text("You dead!")
deadmenuind=se.Object("*")
deadmenutext1.add(deadmap, round(deadmap.width/2)-4, round(deadmap.height/2)+3)
deadmenutext2.add(deadmap, round(deadmap.width/2)-2, round(deadmap.height/2)+5)
deadtext.add(deadmap, round(deadmap.width/2)-4, round(deadmap.height/2-6))
deadmenuind.add(deadmap, deadmenutext1.x-2, deadmenutext1.y)
scoretext=se.Text("You scored 0 points")
scoretext.add(deadmap, round(deadmap.width/2-8-1), round(deadmap.height/2-4))

def dead():
    global ev, scoretext
    ev=0
    deadmenuind.index=1
    scoretext.remove()
    scoretext=se.Text("You scored "+str(len(snake.obs))+" points")
    scoretext.add(deadmap, round(deadmap.width/2-8-len(str(len(snake.obs)))/2), round(deadmap.height/2-4))
    deadmap.blur_in(map)
    deadmap.show(init=True)
    while True:
        if ev == "'m'":
            ev=0
            exit()
        elif ev == "'w'":
            if deadmenuind.index != 1:
                deadmenuind.index-=1
            exec("deadmenuind.set(deadmenutext"+str(deadmenuind.index)+".x-2, deadmenutext"+str(deadmenuind.index)+".y)")
            ev=0
        elif ev == "'s'":
            if deadmenuind.index != 2:
                deadmenuind.index+=1
            exec("deadmenuind.set(deadmenutext"+str(deadmenuind.index)+".x-2, deadmenutext"+str(deadmenuind.index)+".y)")
            ev=0
        elif ev == "Key.enter":
            if deadmenuind.y == deadmenutext1.y:
                main()
            elif deadmenuind.y == deadmenutext2.y:
                exit()
            ev=0
        else:
            time.sleep(0.05)
        deadmap.show()

menumap=se.Map(background=" ")

menutext=se.Text("Menu:")
menutext1=se.Text("Resume")
menutext2=se.Text("Restart")
menutext3=se.Text("Exit")
menuind=se.Object("*")
curscore=se.Text("Current score: 0 points")
curscore.add(menumap, round(menumap.width/2-11), round(menumap.height/2)-4)
menutext1.add(menumap, round(menumap.width/2)-3, round(menumap.height/2)+1)
menutext2.add(menumap, round(menumap.width/2)-3, round(menumap.height/2)+3)
menutext3.add(menumap, round(menumap.width/2)-2, round(menumap.height/2)+5)
menutext.add(menumap, round(menumap.width/2)-2, round(menumap.height/2)-6)
menuind.add(menumap, menutext1.x-2, menutext1.y)

def menu():
    global ev, curscore
    ev=0
    menuind.index=1
    curscore.remove()
    curscore=se.Text("Current score: "+str(len(snake.obs))+" points")
    curscore.add(menumap, round(menumap.width/2-10-len(str(len(snake.obs)))/2), round(menumap.height/2)-4)
    menumap.blur_in(map)
    menumap.show(init=True)
    while True:
        if ev == "'m'":
            ev=0
            break
        elif ev == "'w'":
            if menuind.index != 1:
                menuind.index-=1
            exec("menuind.set(menutext"+str(menuind.index)+".x-2, menutext"+str(menuind.index)+".y)")
            ev=0
        elif ev == "'s'":
            if menuind.index != 3:
                menuind.index+=1
            exec("menuind.set(menutext"+str(menuind.index)+".x-2, menutext"+str(menuind.index)+".y)")
            ev=0
        elif ev == "Key.enter":
            if menuind.y == menutext1.y:
                return
            elif menuind.y == menutext2.y:
                main()
            elif menuind.y == menutext3.y:
                exit()
            ev=0
        else:
            time.sleep(0.05)
        menumap.show() # Showing menumap

def main():
    global ev, apple_num, runner_num, snake, map
    walkframe=0
    genframe=0
    apple_num=0
    runner_num=2
    framenum=0

    map=se.Map(background=" ")

    start=Start("#")
    runner0=se.Object("#")
    runner1=se.Object("#")
    start.add(map, round(map.width/2), round(map.height/2))
    runner0.add(map, round(map.width/2), round(map.height/2)+1)
    runner1.add(map, round(map.width/2), round(map.height/2)+2)
    snake=se.ObjectGroup([start, runner0, runner1])

    start.direction="t"

    map.show()
    while True:
        if ev == "'w'":
            if start.direction != "b":
                start.direction="t"
            ev=0
        elif ev == "'a'":
            if start.direction != "r":
                start.direction="l"
            ev=0
        elif ev == "'s'":
            if start.direction != "t":
                start.direction="b"
            ev=0
        elif ev == "'d'":
            if start.direction != "l":
                start.direction="r"
            ev=0
        elif ev == "'m'":
            menu()
            map.show(init=True)
            ev=0
        else:
            time.sleep(0.01)
        if walkframe+5 == framenum:
            oldx=start.x
            oldy=start.y
            if start.direction == "t":
                start.set(start.x, start.y-1)
            if start.direction == "b":
                start.set(start.x, start.y+1)
            if start.direction == "l":
                start.set(start.x-1, start.y)
            if start.direction == "r":
                start.set(start.x+1, start.y)
            for ob in snake.obs[1:]:
                ob.oldx=ob.x
                ob.oldy=ob.y
                ob.set(oldx, oldy)
                oldx=ob.oldx
                oldy=ob.oldy
            walkframe+=5
        if genframe+100 == framenum:
            applegen()
            genframe+=100
        map.show()
        framenum+=1

recognising=threading.Thread(target=recogniser)
recognising.daemon=True
recognising.start()
main()
