# Scrap_engine documentation

## Concept
The basic concept of scrap_engine evolves around having a ```map``` that is basicaly a cordinatesystem that represents the colloms and rows in the console/terminal.
On this maps ```objects``` can be added, moved, and removed acording to given rules.
![example](../pics/example1.jpg)

## Classes

### scrap_engine.Map
The basic map class to add scrap_engine.objects on.

#### Method ```scrap_engine.Map.__init__(self, height=height-1, width=width, background="#", dynfps=True)```
Constructor.
- height:```int``` Heigt of the map
- width:```int``` Width of the map
- background:```String``` Default char, that will be used as the maps background
- dynfps:```boolean``` If changes of the map will be checked a ```scrap_engine.Map.show()```

#### Method ```scrap_engine.Map.show(self, init=False)```
Shows a frame.
- init:```boolean``` Forces printing

#### Method ```scrap_engine.Map.resize(self, height, width, background="#")```
Resizes the map.
- height:```int``` New heigt of the map
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
- state:```String``` State ```"solid"``` or ```"float"```, that indices the behavior of the Obeject. ```"solid"``` means that not other objects can be put over the object, ```"float"``` means that it is possible.
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
Method thats executed, when it's tried to lay this object over another object with ```self.state = "solid"```. This function returns nothing and does nothing, it can be used in custom daughter classes of ```scrap_engine.Object```.
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
---

### scrap_engine.ObjectGroup
More a metha class to arganize ```scrap_engine.Object```s and daughter objects to do certain actions with a group of those at once.

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
Moves the group to a given coordinate. THIS JUST WIRKS WITH DAUGHTER CLASSES, BECAUSE ```scrap_engine.ObjectGroup``` HAS NO COORDINATE BY IT SELF.
- x:```int``` The new x coordinate the group will be set to
- y:```int``` The new y coordinate the group will be set to
---

### scrap_engine.Text
An easy way to generate text labels. This is a daughter class of ```scrap_engine.ObjectGroup``` and shares all its methods.

#### Method ```scrap_engine.Text.__init__(self, text, state="solid", esccode="", ob_class=Object, ob_args={}, ignore="")```
Constructor.
- text:```String``` The text of the label.
- state:```String``` State ```"solid"``` or ```"float"```, that indices the behavior of the Obeject. ```"solid"``` means that not other objects can be put over the object, ```"float"``` means that it is possible.
- esccode:```String``` The ansii escape code that can be used to color the text or make it bold/italic...
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
- esccode:```String``` The ansii escape code that can be used to color the text or make it bold/italic...
