#!/usr/bin/env python3
# This software is licensed under the GPL3

import time, os, threading

width, height = os.get_terminal_size()


class CoordinateError(Exception):
    def __init__(self, ob, map, x, y):
        self.ob = ob
        self.x = x
        self.y = y
        self.map = map
        super().__init__(f"The {ob}s coordinate ({x}|{y}) is \
not in {map.width-1}x{map.height-1}")


class Map():
    def __init__(self, height=height-1, width=width, background="#", dynfps=True):
        self.height=height
        self.width=width
        self.dynfps=dynfps
        self.background=background
        self.obmap=[[[Object(self.background, state="float")] 
            for j in range(width)] for i in range(height)]
        self.obs=[]
        self.out_old = ""

    def blur_in(self, blurmap, esccode="\033[37m"):
        for l in range(self.height):
            for i in range(self.width):
                self.map[l][i]=esccode+(blurmap.map[l][i].replace("\033[0m", "")[-1] if blurmap.obmap[l][i] == [] else blurmap.obmap[l][i][-1].char.replace("\033[0m", "")[-1])+"\033[0m"

    def show(self, init=False):
        self.out = (f"\r\u001b[{self.height}A"
                +"".join("".join(i[-1].char for i in j) for j in self.obmap)
                +"\n\u001b[1000D")
        if self.out_old != self.out or self.dynfps == False or init == True:
            print(self.out, end="")
            self.out_old = self.out


    def resize(self, height, width, background="#"):
        self.background=background
        self.obmap=[[[Object(self.background, state="float")] 
            for j in range(width)] for i in range(height)]
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
        self.obmap=[[[Object(" ", state="float")] 
                for j in range(width)] for i in range(height)]        
        self.obs=[]
        self.out_old = ""
        self.remap()

    def remap(self):
        for h in range(self.height):
            for w in range(self.width):
                # print(h+self.y, self.bmap.height, w+self.x, self.bmap.width)
                if h+self.y < self.bmap.height and w+self.x < self.bmap.width:
                    char = self.bmap.obmap[h+self.y][w+self.x][-1].char
                else:
                    char = " "
                self.obmap[h][w][0].rechar(char)

    def set(self, x, y):
        if x<0 or y<0:
            return 1
        self.x=x
        self.y=y
        self.remap()
        return 0

    def full_show(self, init=False):
        self.remap()
        self.show(init)


class Object():
    def __init__(self, char, state="solid", arg_proto={}):
        self.char = char
        self.state = state
        self.added = False
        self.arg_proto = arg_proto

    def add(self, map, x, y):
        if not (0 <= x < map.width) or not (0 <= y < map.height):
            raise CoordinateError(self, map, x, y)
        if "solid" == map.obmap[y][x][-1].state:
            return 1
        self.x=x
        self.y=y
        map.obmap[y][x].append(self)
        map.obs.append(self)
        self.map=map
        self.added=True
        return 0

    def set(self, x, y):
        if not self.added:
            return 1
        elif x > self.map.width-1:
            self.bump_right()
            return 1
        elif x < 0:
            self.bump_left()
            return 1
        elif y > self.map.height-1:
            self.bump_bottom()
            return 1
        elif y < 0:
            self.bump_top()
            return 1
        elif self.x > self.map.width-1 or self.y > self.map.height-1:
            self.pull_ob()
            return 1
        elif (ob := self.map.obmap[y][x][-1]).state == "solid":
            self.bump(ob, self.x-x, self.y-y)
            return 1
        del self.map.obmap[self.y][self.x][self.map.obmap[self.y][self.x].index(self)]
        self.map.obmap[y][x].append(self)
        self.x=x
        self.y=y
        if ob.state == "float":
            ob.action(self)
        return 0

    def redraw(self):
        return

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

    def remove(self):
        if not self.added:
            return 1
        self.added=False
        del self.map.obs[self.map.obs.index(self)]
        del self.map.obmap[self.y][self.x][self.map.obmap[self.y][self.x].index(self)]


class ObjectGroup():
    def __init__(self, obs):
        self.obs = obs
        for ob in obs:
            ob.group = self

    def add_ob(self, ob):
        self.obs.append(ob)
        ob.group = self

    def add_obs(self, obs):
        for ob in obs:
            self.add_ob(ob)

    def rem_ob(self, ob):
        for i in range(len(self.obs)):
            if ob == self.obs[i]:
                self.obs[i].group = ""
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
        self.x = x
        self.y = y

    def set_state(self, state):
        self.state = state
        for i in self.obs:
            i.set_state(state)


class Text(ObjectGroup):
    def __init__(self, text, state="solid", esccode="", ob_class=Object,
            ob_args={}, ignore=""):
        self.obs = []
        self.ob_class = ob_class
        self.added = False
        self.map = None
        self.x = None
        self.y = None
        self.text = text
        self.esccode = esccode
        self.state = state
        self.ignore = ignore
        self.ob_args = ob_args
        self.__texter(text)

    def __add__(self, other):
        self.text += other.text
        self.obs += other.obs
        if self.added:
            self.remove()
            self.add(self.map, self.x, self.y)
        return self

    def __texter(self, text):
        for text in text.split("\n"):
            for i, char in enumerate(text):
                if self.esccode != "":
                    char = self.esccode+char+"\033[0m"
                self.obs.append(self.ob_class(char, self.state,
                                            arg_proto=self.ob_args))
        for ob in self.obs:
            ob.group = self

    def add(self, map, x, y):
        self.added = True
        self.map = map
        self.x = x
        self.y = y
        count = 0
        for l, text in enumerate(self.text.split("\n")):
            for i, ob in enumerate(self.obs[count:count+len(text)]):
                if ob.char != self.ignore:
                    ob.add(map, x+i, y+l)
            count += len(text)

    def remove(self):
        self.added = False
        for ob in self.obs:
            ob.remove()

    def rechar(self, text, esccode=""):
        self.esccode = esccode
        if self.added:
            for ob in self.obs:
                ob.remove()
        self.obs = []
        self.__texter(text)
        self.text = text
        if self.added:
            self.add(self.map, self.x, self.y)


class Square(ObjectGroup):
    def __init__(self, char, width, height, state="solid", ob_class=Object,
            ob_args={}, threads=False):
        self.obs = []
        self.ob_class = ob_class
        self.width = width
        self.height = height
        self.added = False
        self.char = char
        self.state = state
        self.exits = []
        self.ob_args = ob_args
        self.threads = threads
        self.__create()
        for ob in self.obs:
            ob.group = self

    def __create(self):
        for l in range(self.height):
            if self.threads:
                threading.Thread(target=self.__one_line_create,
                        args=(l,), daemon=True).start()
            else:
                self.__one_line_create(l)

    def __one_line_create(self, l):
        for i in range(self.width):
            exec(f"self.ob_{i}_{l} = self.ob_class(self.char, self.state,\
arg_proto=self.ob_args)")
            exec(f"self.obs.append(self.ob_{i}_{l})")

    def __one_line_add(self, l):
        for i in range(self.width):
            exec(f"self.exits.append(self.ob_{i}_{l}.add(self.map, self.x+i,\
self.y+l))")

    def add(self, map, x, y):
        self.x = x
        self.y = y
        self.map = map
        for l in range(self.height):
            if self.threads:
                threading.Thread(target=self.__one_line_add, args=(l,),
                        daemon=True).start()
            else:
                self.__one_line_add(l)
        self.added = True
        if 1 in self.exits:
            return 1
        return 0

    def remove(self):
        self.added = False
        for ob in self.obs:
            ob.remove()

    def rechar(self, char):
        for ob in self.obs:
            ob.rechar(char)

    def resize(self, width, height):
        self.width = width
        self.height = height
        if self.added:
            self.remove()
            self.obs = []
            self.__create()
            self.add(self.map, self.x, self.y)
        else:
            self.obs = []
            self.__create()


class Frame(ObjectGroup):
    def __init__(self, height, width, corner_chars=["+", "+", "+", "+"],
            horizontal_chars=["-", "-"], vertical_chars=["|", "|"],
            state="solid", ob_class=Object, ob_args={}):
        self.height = height
        self.width = width
        self.ob_class = ob_class
        self.ob_args = ob_args
        self.added = False
        self.state = state
        self.corner_chars = corner_chars
        self.horizontal_chars = horizontal_chars
        self.vertical_chars = vertical_chars
        self.corners = [self.ob_class(i, arg_proto=self.ob_args,
                            state=self.state)
                        for i, j in zip(corner_chars, range(4))]
        self.horizontals = [Square(char=i, width=self.width-2, height=1,
                                state=self.state, ob_class=Object, ob_args={})
                            for i, j in zip(horizontal_chars, range(2))]
        self.verticals = [Square(char=i, width=1, height=self.height-2,
                            state=self.state, ob_class=Object, ob_args={})
                        for i, j in zip(vertical_chars, range(2))]

    def __add_obs(self):
        for ob, rx, ry in zip(self.corners, [0, self.width-1, 0, self.width-1],
                [0, 0, self.height-1, self.height-1]):
            ob.add(self.map, self.x+rx, self.y+ry)
        for ob, rx, ry in zip(self.horizontals, [1, 1], [0, self.height-1]):
            ob.add(self.map, self.x+rx, self.y+ry)
        for ob, rx, ry in zip(self.verticals, [0, self.width-1], [1, 1]):
            ob.add(self.map, self.x+rx, self.y+ry)

    def add(self, map, x, y):
        self.x = x
        self.y = y
        self.map = map
        self.__add_obs()
        self.added = True

    def set(self, x, y):
        self.x = x
        self.y = y
        for ob in self.corners+self.horizontals+self.verticals:
            ob.remove()
        self.__add_obs()

    def rechar(self, corner_chars=["+", "+", "+", "+"], horizontal_char="-",
            vertical_char="|"):
        for ob, c in zip(self.corners, corner_chars):
            ob.rechar(c)
        for ob in self.horizontals:
            ob.rechar(horizontal_char)
        for ob in self.verticals:
            ob.rechar(vertical_char)

    def remove(self):
        for ob in self.corners + self.horizontals + self.verticals:
            ob.remove()
        self.added = False

    def resize(self, height, width):
        added = self.added
        if added:
            self.remove()
        self.__init__(height, width, corner_chars=self.corner_chars,
            horizontal_chars=self.horizontal_chars,
            vertical_chars=self.vertical_chars, state=self.state,
            ob_class=self.ob_class, ob_args=self.ob_args)
        if added:
            self.add(self.map, self.x, self.y)


class Box(ObjectGroup):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.obs = []
        self.added = False

    def add(self, map, x, y):
        self.x = x
        self.y = y
        self.map = map
        for ob in self.obs:
            ob.add(self.map, ob.rx+self.x, ob.ry+self.y)
        self.added = True

    def add_ob(self, ob, x, y):
        self.obs.append(ob)
        ob.rx = x
        ob.ry = y
        if self.added:
            ob.add(self.map, ob.rx+self.x, ob.ry+self.y)

    def set_ob(self, ob, x, y):
        ob.rx = x
        ob.ry = y
        if self.added:
            ob.set(ob.rx+self.x, ob.ry+self.y)

    def remove(self):
        for ob in self.obs:
            ob.remove()
        self.added = False

    def resize(self, height, width):
        self.heigth = height
        self.width = width


class Circle(Box):
    def __init__(self, char, radius, state="solid", ob_class=Object,
            ob_args={}):
        super().__init__(0, 0)
        self.char = char
        self.ob_class = ob_class
        self.ob_args = ob_args
        self.state = state
        self.__gen(radius)

    def __gen(self, radius):
        self.radius = radius
        for i in range(-(int(radius)+1), int(radius+1)+1):
            for j in range(-(int(radius)+1), int(radius+1)+1):
                if math.sqrt((i)**2+(j)**2) <= radius:
                    self.add_ob(self.ob_class(self.char, state=self.state,
                                            arg_proto=self.ob_args), i, j)

    def rechar(self, char):
        self.char = char
        for ob in self.obs:
            ob.rechar(char)

    def resize(self, radius):
        if self.added:
            self.remove()
            self.obs = []
            self.__gen(radius)
            self.add(self.map, self.x, self.y)
        else:
            self.obs = []
            self.__gen(radius)


class Line(Box):
    def __init__(self, char, cx, cy, type="straight", state="solid",
            ob_class=Object, ob_args={}):
        super().__init__(0, 0)
        self.char = char
        self.ob_class = ob_class
        self.ob_args = ob_args
        self.state = state
        self.type = type
        self.__gen(cx, cy)

    def __gen(self, cx, cy):
        self.cx = cx
        self.cy = cy
        if cx**2 >= cy**2:
            for i in range(int(math.sqrt(cx**2))):
                i = int(cx/math.sqrt(cx**2)*i)
                j = {"straight": int, "crippled": round}[self.type](cy*i/cx)
                self.add_ob(self.ob_class(self.char, state=self.state,
                    arg_proto={**self.ob_args, **{"x": i, "y": cy*i/cx}}),
                    i, j)
        else:
            for j in range(int(math.sqrt(cy**2))):
                j = int(cy/math.sqrt(cy**2)*j)
                i = {"straight": int, "crippled": round}[self.type](cx*j/cy)
                self.add_ob(self.ob_class(self.char, state=self.state,
                    arg_proto={**self.ob_args, **{"x": cx*j/cy, "y": j}}),
                    i, j)

    def rechar(self, char):
        self.char = char
        for ob in self.obs:
            ob.rechar(char)

    def resize(self, cx, cy):
        if self.added:
            self.remove()
            self.obs = []
            self.__gen(cx, cy)
            self.add(self.map, self.x, self.y)
        else:
            self.obs = []
            self.__gen(cx, cy)
