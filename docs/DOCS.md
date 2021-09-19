# Scrap_engine documentation

## Table of contents
1. [Concept](#concept)
2. [Classes](#classes)
	1. [scrap_engine.Map](#scrap_enginemap)
  	2. [scrap_engine.Object](#scrap_engineobject)
  	3. [scrap_engine.ObjectGroup](#scrap_engineobjectgroup)
  	4. [scrap_engine.Text](#scrap_enginetext)
  	5. [scrap_engine.Square](#scrap_enginesquare)
  	6. [scrap_engine.Frame](#scrap_engineframe)
  	7. [scrap_engine.Box](#scrap_enginebox)
    8. [scrap_engine.Circle](#scrap_enginecircle)
    9. [scrap_engine.Submap](#scrap_enginesubmap)
3. [Errors](#errors)
	1. [CoordinateError](#coordinateerror)
4. [Examples](#examples)
## Concept
The basic concept of scrap_engine evolves around having a ```map``` that is basically a coordinate system that represents the column and rows in the console/terminal.
On this maps ```objects``` can be added, moved, and removed according to given rules.
![example](../pics/example1.jpg)

## Classes
Note: The most constructor/method arguments of class directly translate to their attributes and, with some exceptions (state, dynfps, type...), should not be manipulated directly.

There may be some method descriptions missing for some classes, that's because those methods are described in their mother classes description. 

### scrap_engine.Map
The basic map class to add scrap_engine.objects on.

#### Method ```scrap_engine.Map.__init__(self, height=height-1, width=width, background="#", dynfps=True)```
Constructor.
- height:```int``` Height of the map
- width:```int``` Width of the map
- background:```String``` Default char, that will be used as the maps background
- dynfps:```boolean``` If changes of the map will be checked a ```scrap_engine.Map.show()```

#### Method ```scrap_engine.Map.show(self, init=False)```
Shows a frame.
- init:```boolean``` Forces printing

#### Method ```scrap_engine.Map.resize(self, height, width, background="#")```
Resizes the map.
- height:```int``` New height of the map
- width:```int``` New width of the map
- background:```String``` Default char, that will be used as the maps background

#### Method ```scrap_engine.Map.blur_in(self, blurmap, esccode="\033[37m")```
Blurs another map as the background into the map
- blurmap:```scrap_engine.Map``` The map to use as the background
- esccode:```String``` Escape code used to blur the blurmap

---

### scrap_engine.Object
An object that can be added and moved on a ```scrap_engine.Map```.

#### Method ```scrap_engine.Object.__init__(self, char, state="solid", arg_proto={})```
Constructor.
- char:```String``` A string that represents to object on the map
- state:```String``` State ```"solid"``` or ```"float"```, that indices the behaviour of the Object. ```"solid"``` means that not other objects can be put over the object, ```"float"``` means that it is possible.
- arg_proto:```dictionary``` A custom dictionary that can be passed to custom objects in, for example ```scrap_engine.Text```

#### Method ```scrap_engine.Object.add(self, map, x, y)```
Adds the object to a given map at a given coordinate.
- map:```scrap_engine.Map``` The map the object should be added to
- x:```int``` The x coordinate the object will be set to
- y:```int``` The y coordinate the object will be set to

#### Method ```scrap_engine.Object.set(self, x, y)```
Sets the object to a given coordinate on the map.
If this fails, the method will return 1.
- x:```int``` The new x coordinate the object will be set to
- y:```int``` The new y coordinate the object will be set to

#### Method ```scrap_engine.Object.remove(self)```
Removes the object from the map.

#### Method ```scrap_engine.Object.redraw(self)```
Redraws the object on the map.

#### Method ```scrap_engine.Object.rechar(self, char)```
Changes the char of the Object, that represents the object on the map.
- char:```String``` The new string that represents to object on the map

#### Method ```scrap_engine.Object.action(self, ob)```
Method that is executed, when another object is laid over it self. This just works, if ```self.state = "float"```. This function returns nothing and does nothing, it can be used in custom daughter classes of ```scrap_engine.Object```.
- ob:```scrap_engine.Object``` The object, that is laid over self.

#### Method ```scrap_engine.Object.bump(self, ob, x, y)```
Method that's executed, when it's tried to lay this object over another object with ```self.state = "solid"```. This function returns nothing and does nothing, it can be used in custom daughter classes of ```scrap_engine.Object```.
- ob:```scrap_engine.Object``` The object, that self tried to be laid over
- x:```int``` X coordinate of the object, that self tried to be laid over
- y:```int``` Y coordinate of the object, that self tried to be laid over

#### Method ```scrap_engine.Object.bump_left(self)```
This method is executed when trying to set self over the left boarders of the map. This function returns nothing and does nothing, it can be used in custom daughter classes of ```scrap_engine.Object```.

#### Method ```scrap_engine.Object.bump_right(self)```
This method is executed when trying to set self over the right boarders of the map. This function returns nothing and does nothing, it can be used in custom daughter classes of ```scrap_engine.Object```.

#### Method ```scrap_engine.Object.bump_top(self)```
This method is executed when trying to set self over the top boarders of the map. This function returns nothing and does nothing, it can be used in custom daughter classes of ```scrap_engine.Object```.

#### Method ```scrap_engine.Object.bump_bottom(self)```
This method is executed when trying to set self over the bottom boarders of the map. This function returns nothing and does nothing, it can be used in custom daughter classes of ```scrap_engine.Object```.

#### Method ```scrap_engine.Object.pull_ob(self)```
This method is executed when trying to move self from a place out of the boarders of the map to a place inside the boarders. This function returns nothing and does nothing, it can be used in custom daughter classes of ```scrap_engine.Object```.

#### Method ```scrap_engine.Object.set_state(self, state)```
Sets the state of the Object.
- state:```String``` The new state ("float" or "solid")

---

### scrap_engine.ObjectGroup
More a meta class to organize ```scrap_engine.Object```s and daughter objects to do certain actions with a group of those at once.

#### Method ```scrap_engine.ObjectGroup.__init__(self, obs)```
Constructor.
- obs:```list<scrap_engine.Object>``` The initial list of ```scrap_engine.Object```s.

#### Method ```scrap_engine.ObjectGroup.add_ob(self, ob)```
Adds an ```scrap_engine.Object``` to the group.
- ob:```scrap_engine.Object``` A single ```scrap_engine.Object```, that's added to the list of ```scrap_engine.Object```s.

#### Method ```scrap_engine.ObjectGroup.add_obs(self, obs)```
Adds a list of ```scrap_engine.Object```s to the group.
- obs:```list<scrap_engine.Object>``` A list of ```scrap_engine.Object```s, that's added to the group.

#### Method ```scrap_engine.ObjectGroup.rem_ob(self, ob)```
Removes an ```scrap_engine.Object``` from the group.
- ob:```scrap_engine.Object``` The ```scrap_engine.Object``` that's going to be removed.

#### Method ```scrap_engine.ObjectGroup.move(self, x=0, y=0)```
Moves all objects of the group with a given vector.
- x:```int``` X component of the vector
- y:```int``` Y component of the vector

#### Method ```scrap_engine.ObjectGroup.remove(self)```
Removes all ```scrap_engine.Object```s in the group from the map.

#### Method ```scrap_engine.ObjectGroup.set(self, x, y)```
Moves the group to a given coordinate. THIS JUST WORKS WITH DAUGHTER CLASSES, BECAUSE ```scrap_engine.ObjectGroup``` HAS NO COORDINATE BY IT SELF.
- x:```int``` The new x coordinate the group will be set to
- y:```int``` The new y coordinate the group will be set to

#### Method ```scrap_engine.ObjectGroup.set_state(self, state)```
Sets the state of the Object.
- state:```String``` The new state ("float" or "solid")

---

### scrap_engine.Text
An easy way to generate text labels. This is a daughter class of ```scrap_engine.ObjectGroup``` and shares all its methods. Texts can be added together.

#### Method ```scrap_engine.Text.__init__(self, text, state="solid", esccode="", ob_class=Object, ob_args={}, ignore="")```
Constructor.
- text:```String``` The text of the label.
- state:```String``` State ```"solid"``` or ```"float"```, that indices the behaviour of the Obeject. ```"solid"``` means that not other objects can be put over the object, ```"float"``` means that it is possible.
- esccode:```String``` The ansii escape code that can be used to colour the text or make it bold/italic...
- ob_class:```class``` The class of the objects in the label, that should be used.
- ob_args:```dictionary``` This dictionary is passed as ```arg_proto``` to the objects.
- ignore:```String``` Character of objects that should be ignored not be added to the map.

#### Method ```scrap_engine.Text.add(self, map, x, y)```
Adds the text to a map.
- map:```scrap_engine.Map``` The map the text should be added to
- x:```int``` The x coordinate the text will be set to
- y:```int``` The y coordinate the text will be set to

#### Method ```scrap_engine.Text.remove(self)```
Removes the text from the map.

#### Method ```scrap_engine.Text.rechar(self, text, esccode="")```
Changes the text of the text.
- text:```String``` The text of the label.
- esccode:```String``` The ansii escape code that can be used to colour the text or make it bold/italic...

---

### scrap_engine.Square
An easy way to generate rectangles. This is a daughter class of ```scrap_engine.ObjectGroup``` and shares all its methods.

#### Method ```scrap_engine.Square.__init__(self, char, width, height, state="solid", ob_class=Object, ob_args={}, threads=False)```
Constructor.
- char:```String``` The character that's used in the rectangle
- width:```int``` Width of the rectangle
- height:```int``` Height of the rectangle
- state:```String``` State ```"solid"``` or ```"float"```, that indices the behaviour of the Object. ```"solid"``` means that not other objects can be put over the object, ```"float"``` means that it is possible.
- esccode:```String``` The ansii escape code that can be used to color the text or make it bold/italic...
- ob_class:```class``` The class of the objects in the label, that should be used
- ob_args:```dictionary``` This dictionary is passed as ```arg_proto``` to the objects
- threads:```boolean``` If or if not threading should be used for generating the rectangle (useful for big rectangles)

#### Method ```scrap_engine.Square.add(self, map, x, y)```
Adds the rectangle to a map.
- map:```scrap_engine.Map``` The map the rectangle should be added to
- x:```int``` The x coordinate the rectangle will be set to
- y:```int``` The y coordinate the rectangle will be set to

#### Method ```scrap_engine.Square.rechar(self, char)```
Changes char for the character of the rectangle.
- char:```String``` The new character of the rectangle

#### Method ```scrap_engine.Square.resize(self, width, height)```
Changes the size of the rectangle.
- width:```int``` Width of the rectangle
- height:```int``` Height of the rectangle

---

### scrap_engine.Frame
An easy way to generate frames. This is a daughter class of ```scrap_engine.ObjectGroup``` and shares all its methods.

#### Method ```scrap_engine.Frame.__init__(self, height, width, corner_chars=["+", "+", "+", "+"], horizontal_chars=["-", "-"], vertical_chars=["|", "|"], state="solid", ob_class=Object, ob_args={})```
Constructor.
- height:```int``` Height of the frame
- width:```int``` Width of the frame
- corner_chars:```list<String>``` Chars used for frame corners, [lefttop, righttop, leftbottom, rightbottom]
- horizontal_chars:```list<String>``` Chars used for horizontals, [top, bottom]
- vertical_chars:```list<String>``` Chars used for verticals, [left, right]
- state:```String``` State ```"solid"``` or ```"float"```, that indices the behaviour of the Object. ```"solid"``` means that not other objects can be put over the object, ```"float"``` means that it is possible.
- ob_class:```class``` The class of the objects in the label, that should be used
- ob_args:```dictionary``` This dictionary is passed as ```arg_proto``` to the objects

#### Method ```scrap_engine.Frame.add(self, map, x, y)```
Adds the frame to a map.
- map:```scrap_engine.Map``` The map the frame should be added to
- x:```int``` The x coordinate the frame will be set to
- y:```int``` The y coordinate the frame will be set to

#### Method ```scrap_engine.Frame.set(self, x, y)```
Moves the frame to a given coordinate.
- x:```int``` The new x coordinate the frame will be set to
- y:```int``` The new y coordinate the frame will be set to

#### Method ```scrap_engine.Frame.rechar(self, corner_chars=["+", "+", "+", "+"], horizontal_char="-", vertical_char="|")```
Changes char for the character of the rectangle.
- corner_chars:```list<String>``` Chars used for frame corners, [lefttop, righttop, leftbottom, rightbottom]
- horizontal_chars:```list<String>``` Chars used for horizontals, [top, bottom]
- vertical_chars:```list<String>``` Chars used for verticals, [left, right]

#### Method ```scrap_engine.Frame.remove(self)```
Removes the frame from the map.

#### Method ```scrap_engine.Frame.resize(self, height, width)```
Resizes the frame.
- height:```int``` Height of the frame
- width:```int``` Width of the frame

---

### scrap_engine.Box
A box to pack objects/groups/frames etc. into relative to a coordinate. This is a daughter class of ```scrap_engine.ObjectGroup``` and shares all its methods.

#### Method ```scrap_engine.Box.__init__(self, height, width)```
Constructor.
- height:```int``` Height of the box
- width:```int``` Width of the box

#### Method ```scrap_engine.Box.add(self, map, x, y)```
Adds the box to a map.
- map:```scrap_engine.Map``` The map the box should be added to
- x:```int``` The x coordinate the box will be set to
- y:```int``` The y coordinate the box will be set to

#### Method ```scrap_engine.Box.add_ob(self, ob, rx, ry)```
Adds an object/group etc. to the box.
- ob:```scrap_engine.Object```/```scrap_engine.ObjectGroup``` etc. The object/group that's added to the box
- rx:```int``` The x coordinate the object will be set to in the box
- ry:```int``` The y coordinate the object will be set to in the box

#### Method ```scrap_engine.Box.set_ob(self, ob, rx, ry)```
Sets an object to another coordinate in the box.
- ob:```scrap_engine.Object```/```scrap_engine.ObjectGroup``` etc. The object/group that's is
- rx:```int``` The new x coordinate the object will be set to in the box
- ry:```int``` The new y coordinate the object will be set to in the box

#### Method ```scrap_engine.Box.remove(self)```
Removes the box from the map.

#### Method ```scrap_engine.Box.resize(self, height, width)```
Resizes the box.
- height:```int``` Height of the box
- width:```int``` Width of the box

---

### scrap_engine.Circle
An easy way to create a circle with a given radius, that's more like an ellipse. This is a daughter class of ```scrap_engine.Box``` and shares all its methods.

#### Method ```scrap_engine.Circle.__init__(self, char, radius, state="solid", ob_class=Object, ob_args={})```
Constructor.
- char:```String``` Character used for the circle
- radius:```float``` Radius of the circle
- state:```String``` State ```"solid"``` or ```"float"```, that indices the behaviour of the Object. ```"solid"``` means that not other objects can be put over the object, ```"float"``` means that it is possible.
- ob_class:```class``` The class of the objects in the label, that should be used
- ob_args:```dictionary``` This dictionary is passed as ```arg_proto``` to the objects

#### Method ```scrap_engine.Circle.rechar(self, char)```
Changes char for the character of the circle.
- char:```String``` The new character of the circle

#### Method ```scrap_engine.Circle.resize(self, radius)```
Changes the radius of the circle
- radius:```float``` Radius of the circle

---

### scrap_engine.Line
A line that can be drawn on the map, that's described by a vector. This is a daughter class of ```scrap_engine.Box``` and shares all its methods. The unrounded coordinates of the single points Objects of the line are passed in arg_proto to the Objects.

#### Method ```scrap_engine.Line.__init__(self, char, cx, cy, l_type="straight", state="solid", ob_class=Object, ob_args={})```
Constructor.
- char:```String``` Character used for the circle
- cx: ```float``` X component of the vector
- cy: ```float``` Y component of the vector
- state:```String``` State ```"solid"``` or ```"float"```, that indices the behaviour of the Object. ```"solid"``` means that not other objects can be put over the object, ```"float"``` means that it is possible.
- l_type:```String``` The type the line should have `straight` or `crippled` 
- ob_class:```class``` The class of the objects in the label, that should be used
- ob_args:```dictionary``` This dictionary is passed as ```arg_proto``` to the objects

#### Method ```scrap_engine.Line.rechar(self, char)```
Changes char for the character of the line.
- char:```String``` The new character of the circle

#### Method ```scrap_engine.Line.resize(self, cx, cy)```
Changes the vector of the line.
- cx: ```float``` X component of the vector
- cy: ```float``` Y component of the vector

---

### scrap_engine.Submap
A map that's background is a cut-out of another map. This is a daughter class of ```scrap_engine.Map``` and shares all its methods.

#### Method ```scrap_engine.Submap.__init__(self, bmap, x, y, height=height-1, width=width, dynfps=True)```
Constructor.
- bmap:```scrap_engine.Map``` The map that's the background
- x:```int``` The x coordinate the map will be set to
- y:```int``` The y coordinate the map will be set to
- height:```int``` Height of the map
- width:```int``` Width of the map
- dynfps:```boolean``` If changes of the map will be checked a ```scrap_engine.Map.show()```

#### Method ```scrap_engine.Submap.remap(self)```
Updates the background.

#### Method ```scrap_engine.Submap.set(self, x, y)```
Moves the map to a given coordinate.
- x:```int``` The new x coordinate the map will be set to
- y:```int``` The new y coordinate the map will be set to

#### Method ```scrap_engine.Submap.full_show(self, init=False)```
A wrapper for ```scrap_engine.Submap.show()``` and ```scrap_engine.Submap.remap(self)```
- init:```boolean``` Forces printing

## Errors
### CoordinateError
The CoordinateError is raised, when an Object is tried to add to an impossible coordinate.
Its' attributes are:
- obj:`scrap_engine.Object` The Object that's tried to add
- map_:`scrap_engine.Map` The Map the Object is tried to add to
- x:`int` The x coordinate the Object is tried to add to
- y:`int` The y coordinate the Object is tried to add to

## Examples
This is just a simple example program that adds a an "a" to the coordinate (10|5) in the terminal.
```python
import scrap_engine as se  # imports scrap_engine

mymap = se.Map(background=" ")  # defines mymap as a map as big as the terminal window with the background " "
myob = se.Object("a")  # defines myob as an object with "a" as character

myob.add(mymap, 10, 5)  # adds myob to mymap at (10|5)
mymap.show()  # shows mymap
```

Another small example that moves the a in a line over the screen.
```python
import scrap_engine as se  # imports scrap_engine
import time

mymap = se.Map(background=" ")  # defines mymap as a map as big as the terminal window with the background " "
myob = se.Object("a")  # defines myob as an object with "a" as character

myob.add(mymap, 10, 5)  # adds myob to mymap at (10|5)
mymap.show()  # shows mymap

for i in range(5):
  time.sleep(0.3)  # waiting 0.3 seconds
  myob.set(myob.x+1, 5)  # sets myob to its own x coordinate +1 and y coordinate 5
  mymap.show()  # shows mymap
```

An example of the Text, Square and Frame class.
```python
import scrap_engine as se  # imports scrap_engine

mymap = se.Map(background=" ")  # defines mymap as a map as big as the terminal window with the background " "
mytext = se.Text("Hello world")  # defines a text as "Hello world"
myrectangle = se.Square(height=5, width=6, char="#")  # defines a rectangle width height 5, width 6 and the character "#"
myframe = se.Frame(height=7, width=8, corner_chars=["┌", "┐", "└", "┘"], horizontal_chars=["─", "─"], vertical_chars=["│", "│"])  # defines a frame see scrap_engine.Frame

mytext.add(mymap, 0, 0)  # adds mytext to (0|0)
myrectangle.add(mymap, 2, 2)  # adds myrectangle to (2|2)
myframe.add(mymap, 1, 1)  # adds myframe to (1|1)

mymap.show()  # now a frame with a rectangle and a text above it should be shown
```

An example of a line across the screen with a moving "#" in it.
```python
import scrap_engine as se
import time

map = se.Map(background=" ")
line = se.Line("a", 10, 5, type="straight")  # makes a straight line described by the vector (10 5) with "a" as its char

line.add(map, 0, 0)  # addes line to (0|0)

map.show()

for i in range(len(line.obs)):  # list.obs is the list of all Objects that are part of the line
    line.obs[i].rechar("#")  # rechars the Object to "#"
    if i != 0:
        line.obs[i-1].rechar(line.char)  # line.char is the default char of the line
    time.sleep(0.4)
    map.show()
```

Example for a clock like line rotation.
```python
import scrap_engine as se
import time, math

map = se.Map(background=" ")
line = se.Line("#", 0, 10)  # downwards facing line of the vector (0 10)
line.add(map, 10, 10)
map.show()

# loops i until 360 and resizes the line with the vector (sin(i)*10 cos(i)*10)
for i in range(360):
    line.resize(math.sin(math.radians(i))*10, math.cos(math.radians(i))*10)
    time.sleep(0.05)
    map.show()

```

An example that shows how Texts are added.
```python
import scrap_engine as se

map = se.Map(background=" ")
text1 = se.Text("Hey")
text2 = se.Text(" You!")

text1 += text2
text1.add(map, 0, 0) # Those two steps can even be switched

#>>> Hey You!

```
