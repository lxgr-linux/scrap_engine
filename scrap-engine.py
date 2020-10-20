#!/usr/bin/env python3
import time

class Map():
    def __init__(self, height, width):
        a="["+width*"'#',"+"],"
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


map=Map(15,40)
ob=Object("i")
ob2=Object("2")
ob.add(map, 1, 2)
ob.set(1,2)
ob2.add(map, 1, 2)
map.show()
for i in range(3):
    time.sleep(1)
    ob.set(ob.x, ob.y+1)
    map.show()
