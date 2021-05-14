import scrap_engine as se

map = se.Map(background=" ")

a = se.Object("a", state="float")
b = se.Object("b", state="float")
c = se.Object("c", state="float")

a.add(map, 1, 1)
b.add(map, 1, 1)
c.add(map, 1, 1)

b.set(0, 0)
c.set(0, 0)

map.show()
