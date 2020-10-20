#!/usr/bin/env python3
import time
import os

width, height = os.get_terminal_size()


class Map():
    def __init__(self, height=height-1, width=width, background="#"):
        a="["+width*("'"+background+"',")+"],"
        exec("self.map=["+height*a+"]")
        self.obs=[]

    def show(self):
        for arr in self.map:
            for i in arr:
                print(i, end="")
            print("")

class Object():
    def __init__(self, char, state="solid"):
        self.char=char
        self.state=state

    def add(self, map, x, y):
        for ob in map.obs:
            if ob.x==x and ob.y==y and ob.state=="solid":
                return
        self.backup=map.map[y][x]
        self.x=x
        self.y=y
        map.map[y][x]=self.char
        map.obs.append(self)
        self.map=map

    def set(self, x, y):
        for ob in map.obs:
            if ob.x==x and ob.y==y and ob.state=="solid":
                return
        self.remove()
        self.backup=map.map[y][x]
        self.x=x
        self.y=y
        map.map[y][x]=self.char

    def remove(self):
        self.map.map[self.y][self.x]=self.backup

class ObjectGroup():
    def __init__(self, obs):
        self.obs=obs

    def add(self, ob):
        self.obs.append(ob)

    def move(self, x=0, y=0):
        for ob in self.obs:
            ob.set(ob.x+x, ob.y+y)

    def remove(self):
        for ob in self.obs:
            ob.remove()

map=Map()
ob=Object("i")
ob2=Object("2")
ob3=Object("3")
ob4=Object("3")
ob5=Object("3")
ob6=Object("3")
ob7=Object("3")
group=ObjectGroup([ob3, ob4, ob5, ob6, ob7])
ob3.add(map, 2, 2)
ob4.add(map, 3, 2)
ob5.add(map, 4, 2)
ob6.add(map, 5, 2)
ob7.add(map, 6, 2)
ob.add(map, 1, 2)
ob.set(1,2)
ob2.add(map, 1, 2)
map.show()
for i in range(3):
    time.sleep(1)
    ob.set(ob.x, ob.y+1)
    map.show()
group.move(2,3)
map.show()
group.remove()
map.show()
