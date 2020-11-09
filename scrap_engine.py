#!/usr/bin/env python3
import time, os

width, height = os.get_terminal_size()

class Map():
    def __init__(self, height=height-1, width=width, background="#", dynfps=True):
        a="["+width*("'"+background+"',")+"],"
        self.height=height
        self.width=width
        self.dynfps=dynfps
        self.background=background
        exec("self.map=["+height*a+"]")
        self.obs=[]

    def blur_in(self, blurmap, esccode="\033[37m"):
        for l in range(self.height):
            for i in range(self.width):
                if blurmap.map[l][i] != " ":
                    self.map[l][i]=esccode+blurmap.map[l][i].replace("\033[0m", "")[-1]+"\033[0m"
                else:
                    self.map[l][i]=" "
        for ob in self.obs:
            ob.redraw()

    def show(self, init=False):
        try:
            self.out_old
        except:
            self.out_old="test"
        self.out="\n"
        for arr in self.map:
            self.out_line=""
            for i in arr:
                self.out_line+=i
            if self.out_line == self.width*" ":
                self.out_line=" "
            self.out+=self.out_line+"\n"
        if self.out_old != self.out or self.dynfps == False or init == True:
            print(self.out, end="")
            self.out_old=self.out

class Submap(Map):
    def __init__(self, bmap, x, y, height=height-1, width=width, dynfps=True):
        self.height=height
        self.width=width
        self.y=y
        self.x=x
        self.dynfps=dynfps
        self.bmap=bmap
        self.map=[]
        self.obs=[]
        self.remap()

    def remap(self):
        self.map=[]
        for arr in self.bmap.map[self.y:self.y+self.height]:
            self.map.append(arr[self.x:self.x+self.width])
        for ob in self.obs:
            ob.redraw()

    def set(self, x, y):
        if x<0 or y<0 or x+self.width>self.bmap.width or y+self.height>self.bmap.height:
            return
        self.x=x
        self.y=y
        self.remap()


class Object():
    def __init__(self, char, state="solid"):
        self.char=char
        self.state=state
        self.added=False

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
        self.added=True

    def set(self, x, y):
        if self.added == False:
            return
        for ob in self.map.obs:
            if ob.x==x and ob.y==y and ob.state=="solid":
                self.bump(self.x-x, self.y-y)
                return
        if x > self.map.width-1:
            self.bump_right()
            return
        if x < 0:
            self.bump_left()
            return
        if y > self.map.height-1:
            self.bump_bottom()
            return
        if y < 0:
            self.bump_top()
            return
        self.map.map[self.y][self.x]=self.backup
        self.backup=self.map.map[y][x]
        self.x=x
        self.y=y
        self.map.map[y][x]=self.char
        for ob in self.map.obs:
            if ob.x==x and ob.y==y and ob.state=="float":
                ob.action(self)

    def redraw(self):
        if self.added == False:
            return
        self.backup=self.map.map[self.y][self.x]
        self.map.map[self.y][self.x]=self.char

    def action(self, ob):
        return

    def bump(self, x, y):
        return

    def bump_right(self):
        return

    def bump_left(self):
        return

    def bump_top(self):
        return

    def bump_bottom(self):
        return

    def rechar(self, char):
        self.map.map[self.y][self.x]=self.backup
        self.char=char
        self.redraw()

    def remove(self):

        self.map.map[self.y][self.x]=self.backup
        for i in range(len(self.map.obs)):
            if self.map.obs[i] == self:
                del self.map.obs[i]
                break
        self.added=False
        for ob in self.map.obs:
            if ob.x == self.x and ob.y == self.y:
                ob.backup=self.backup
                ob.redraw()

class ObjectGroup():
    def __init__(self, obs):
        self.obs=obs
        for ob in obs:
            ob.group=self

    def add_ob(self, ob):
        self.obs.append(ob)
        ob.group=self

    def move(self, x=0, y=0):
        for ob in self.obs:
            ob.set(ob.x+x, ob.y+y)

    def remove(self):
        for ob in self.obs:
            ob.remove()

class Text(ObjectGroup):
    def __init__(self, text, state="solid", esccode=""):
        self.obs=[]
        self.text=text
        for text in text.split("\n"):
            for i, char in enumerate(text):
                if i == 0:
                    char=esccode+char
                if i == len(text)-1 and esccode != "":
                    char+="\033[0m"
                exec("self.ob_"+str(i)+"=Object(char, state)")
                exec("self.obs.append(self.ob_"+str(i)+")")
        for ob in self.obs:
            ob.group=self

    def add(self, map, x, y):
        self.x=x
        self.y=y
        count=0
        for l, text in enumerate(self.text.split("\n")):
            for i, ob in enumerate(self.obs[count:count+len(text)]):
                ob.add(map, x+i, y+l)
            count+=len(text)

    def rechar(self, text):
        mtext=""
        for t in text.split("\n"):
            mtext+=t
        for ob, char in zip(self.obs, mtext):
            ob.rechar(char)

class Square(ObjectGroup):
    def __init__(self, char, width, height, state="solid"):
        self.obs=[]
        self.width=width
        self.height=height
        for l in range(height):
            for i in range(width):
                exec("self.ob_"+str(i)+str(l)+"=Object(char, state)")
                exec("self.obs.append(self.ob_"+str(i)+str(l)+")")
        for ob in self.obs:
            ob.group=self

    def add(self, map, x, y):
        self.x=x
        self.y=y
        for l in range(self.height):
            for i in range(self.width):
                exec("self.ob_"+str(i)+str(l)+".add(map, x+i, y+l)")

    def rechar(self, char):
        for ob in self.obs:
            ob.rechar(char)
