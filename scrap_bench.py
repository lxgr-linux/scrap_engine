#!/usr/bin/env python3

import scrap_engine as se
import time, random, os

def main():
    os.system("")
    map = se.Map(background=" ")
    text = se.Text("0")
    avr = se.Text("0")
    text.add(map, round((map.width-len(str(text.text)))/2-10), round(map.height/2)-1)
    avr.add(map, round((map.width-len(str(text.text)))/2-10), round(map.height/2))
    tcount = 0
    times = 0
    obs = []
    for i in range(50):
        for j in range(10):
            exec("ob_%s_%s = se.Object('\033[34ma\033[0m')"%(str(i), str(j)))
            exec("ob_%s_%s.add(map, i, j)"%(str(i), str(j)))
            exec("obs.append(ob_%s_%s)"%(str(i), str(j)))

    map.show(init=True)
    time2 = 0
    while True:
        time0 = time.time()
        times += time2
        for ob in obs:
            ob.set(random.choice([ob.x, ob.x+1, ob.x-1]), random.choice([ob.y, ob.y+1, ob.y-1]))
        text.rechar(str(time2))
        avr.rechar(str(times/tcount if tcount != 0 else 1))
        map.show()
        tcount += 1
        time2 = time.time()-time0

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
