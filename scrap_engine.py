#!/usr/bin/env python3
# This software is licensed under the GPL3

import time, os, threading

width, height = os.get_terminal_size()

class Map():
    def __init__(self, height=height-1, width=width, background="#", dynfps=True):
        self.height=height
        self.width=width
        self.dynfps=dynfps
        self.background=background
        self.map=[[self.background for j in range(width)] for i in range(height)]
        self.obmap=[[[] for j in range(width)] for i in range(height)]
        self.obs=[]

    def curse_init(): # This method uses curses to display the map in terminal, this may result in glitches
        import curses
        self.screen=curses.initscr()
        curses.start_color()

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
        self.out="\r\u001b["+str(self.height)+"A"
        for arr in self.map:
            self.out_line=""
            for i in arr:
                self.out_line+=i
            self.out+=self.out_line
        if self.out_old != self.out or self.dynfps == False or init == True:
            print(self.out+"\n\u001b[1000D", end="")
            self.out_old=self.out

    def cshow(self, init=False): # uses curses
        self.screen.erase()
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                self.screen.addstr(i, j, self.map[i][j])
        self.screen.refresh()

    def resize(self, height, width, background="#"):
        self.background=background
        self.map=[[self.background for j in range(width)] for i in range(height)]
        self.obmap=[[[] for j in range(width if width > self.width else self.width)] for i in range(height if height > self.height else self.height)]
        self.width=width
        self.height=height
        for ob in self.obs:
            try:
                self.obmap[ob.y][ob.x].append(ob)
                ob.redraw()
            except:
                pass


class Submap(Map):
    def __init__(self, bmap, x, y, height=height-1, width=width, dynfps=True):
        self.height=height
        self.width=width
        self.y=y
        self.x=x
        self.dynfps=dynfps
        self.bmap=bmap
        self.map=[[self.bmap.background for j in range(width)] for i in range(height)]
        self.obmap=[[[] for j in range(width)] for i in range(height)]
        self.obs=[]
        self.remap()

    def remap(self):
        for sy, y in zip(range(0, self.height), range(self.y, self.y+self.height)):
            for sx, x in zip(range(0, self.width), range(self.x, self.x+self.width)):
                try:
                    self.map[sy][sx] = self.bmap.map[y][x]
                except:
                    continue
        for ob in self.obs:
            ob.redraw()

    def set(self, x, y):
        if x<0 or y<0 or x+self.width>self.bmap.width or y+self.height>self.bmap.height:
            return 1
        self.x=x
        self.y=y
        self.remap()
        return 0


class Object():
    def __init__(self, char, state="solid"):
        self.char=char
        self.state=state
        self.added=False

    def add(self, map, x, y):
        for ob in map.obmap[y][x]:
            if ob.state == "solid":
                return 1
        self.backup=map.map[y][x]
        self.x=x
        self.y=y
        map.map[y][x]=self.char
        map.obmap[y][x].append(self)
        map.obs.append(self)
        self.map=map
        self.added=True
        return 0

    def set(self, x, y):
        if self.added == False:
            return 1
        if x > self.map.width-1:
            self.bump_right()
            return 1
        if x < 0:
            self.bump_left()
            return 1
        if y > self.map.height-1:
            self.bump_bottom()
            return 1
        if y < 0:
            self.bump_top()
            return 1
        for ob in self.map.obmap[y][x]:
            if ob.state == "solid":
                self.bump(ob, self.x-x, self.y-y)
                return 1
        try:
            if self.map.obmap[self.y][self.x][0] == self and len(self.map.obmap[self.y][self.x]) > 1:
                self.map.obmap[self.y][self.x][1].backup=self.backup
            else:
                self.map.map[self.y][self.x]=self.backup
        except:
            self.pull_ob()
            return 1
        del self.map.obmap[self.y][self.x][self.map.obmap[self.y][self.x].index(self)]
        self.map.obmap[y][x].append(self)
        self.backup=self.map.map[y][x]
        self.x=x
        self.y=y
        self.map.map[y][x]=self.char
        for ob in self.map.obmap[y][x]:
            if ob.state == "float":
                ob.action(self)
        return 0

    def redraw(self):
        if not self.added:
            return 1
        self.backup=self.map.map[self.y][self.x]
        self.map.map[self.y][self.x]=self.char
        return 0

    def action(self, ob):
        return

    def bump(self, ob, x, y):
        return

    def bump_right(self):
        return

    def bump_left(self):
        return

    def bump_top(self):
        return

    def bump_bottom(self):
        return

    def pull_ob(self):
        return

    def rechar(self, char):
        self.char=char
        if not self.added:
            return 1
        self.map.map[self.y][self.x]=self.backup
        self.redraw()

    def remove(self):
        if not self.added:
            return 1
        self.added=False
        if self.map.obmap[self.y][self.x][0] == self and len(self.map.obmap[self.y][self.x]) > 1:
            self.map.obmap[self.y][self.x][1].backup=self.backup
        else:
            self.map.map[self.y][self.x]=self.backup
        del self.map.obs[self.map.obs.index(self)]
        del self.map.obmap[self.y][self.x][self.map.obmap[self.y][self.x].index(self)]


class ObjectGroup():
    def __init__(self, obs):
        self.obs=obs
        for ob in obs:
            ob.group=self

    def add_ob(self, ob):
        self.obs.append(ob)
        ob.group=self

    def add_obs(self, obs):
        for ob in obs:
            self.add_ob(ob)

    def rem_ob(self, ob):
        for i in range(len(self.obs)):
            if ob == self.obs[i]:
                self.obs[i].group=""
                del self.obs[i]
                return 0
        return 1

    def move(self, x=0, y=0):
        for ob in self.obs:
            ob.remove()
        for ob in self.obs:
            ob.add(self.map, ob.x+x, ob.y+y)

    def remove(self):
        for ob in self.obs:
            ob.remove()

    def set(self, x, y):
        self.move(x-self.x, y-self.y)
        self.x=x
        self.y=y


class Text(ObjectGroup):
    def __init__(self, text, state="solid", esccode="", ob_class=Object):
        self.obs=[]
        self.ob_class=ob_class
        self.added=False
        self.text=text
        self.esccode=esccode
        self.state=state
        self.texter(text)

    def texter(self, text):
        for text in text.split("\n"):
            for i, char in enumerate(text):
                if self.esccode != "":
                    char=self.esccode+char+"\033[0m"
                self.obs.append(self.ob_class(char, self.state))
        for ob in self.obs:
            ob.group=self

    def add(self, map, x, y):
        self.added=True
        self.map=map
        self.x=x
        self.y=y
        count=0
        for l, text in enumerate(self.text.split("\n")):
            for i, ob in enumerate(self.obs[count:count+len(text)]):
                ob.add(map, x+i, y+l)
            count+=len(text)

    def remove(self):
        self.added=False
        for ob in self.obs:
            ob.remove()

    def rechar(self, text, esccode=""):
        self.esccode=esccode
        if self.added:
            for ob in self.obs:
                ob.remove()
        self.obs=[]
        self.texter(text)
        self.text=text
        if self.added:
            self.add(self.map, self.x, self.y)


class Square(ObjectGroup):
    def __init__(self, char, width, height, state="solid", ob_class=Object, threads=False):
        self.obs=[]
        self.ob_class=ob_class
        self.width=width
        self.height=height
        self.char=char
        self.state=state
        self.exits=[]
        self.threads=threads
        for l in range(height):
            if threads:
                threading.Thread(target=self.one_line_create, args=(l,), daemon=True).start()
            else:
                self.one_line_create(l)
        for ob in self.obs:
            ob.group=self

    def one_line_create(self, l):
        for i in range(self.width):
            exec("self.ob_"+str(i)+str(l)+"=self.ob_class(self.char, self.state)")
            exec("self.obs.append(self.ob_"+str(i)+str(l)+")")

    def one_line_add(self, l):
        for i in range(self.width):
            exec("self.exits.append(self.ob_"+str(i)+str(l)+".add(self.map, self.x+i, self.y+l))")

    def add(self, map, x, y):
        self.x=x
        self.y=y
        self.map=map
        for l in range(self.height):
            if self.threads:
                threading.Thread(target=self.one_line_add, args=(l,), daemon=True).start()
            else:
                self.one_line_add(l)
        if 1 in self.exits:
            return 1
        return 0

    def rechar(self, char):
        for ob in self.obs:
            ob.rechar(char)


class Box(ObjectGroup):
    def __init__(self, height, width):
        self.height=height
        self.width=width
        self.obs=[]
        self.added=False

    def add(self, map, x, y):
        self.x=x
        self.y=y
        self.map=map
        for ob in self.obs:
            ob.add(self.map, ob.rx+self.x, ob.ry+self.y)
        self.added=True

    def add_ob(self, ob, rx, ry):
        self.obs.append(ob)
        ob.rx=rx
        ob.ry=ry
        if self.added:
            ob.add(self.map, ob.rx+self.x, ob.ry+self.y)

    def set_ob(self, ob, rx, ry):
        ob.rx=rx
        ob.ry=ry
        ob.set(ob.rx+self.x, ob.ry+self.y)

    def remove(self):
        for ob in self.ob:
            ob.remove()
        self.added=False
