#!/usr/bin/env python3

import scrap_engine as se
import time, random, os

def main():
    global avr, tcount

    os.system("")
    b_map = se.Map(background=" ")
    text = se.Text("0")
    avr = se.Text("0")
    rectangle = se.Square('\033[34ma\033[0m', 50, 10)
    text.add(b_map, round((b_map.width-len(text.text))/2-10),
             round(b_map.height/2)-1)
    avr.add(b_map, round((b_map.width-len(text.text))/2-10),
            round(b_map.height/2))
    rectangle.add(b_map, 0, 0)

    tcount = 0
    times = 0
    time2 = 0

    b_map.show()
    while True:
        time0 = time.time()
        times += time2
        for ob in rectangle.obs:
            ob.set(random.choice([ob.x, ob.x+1, ob.x-1]), random.choice([ob.y, ob.y+1, ob.y-1]))
        text.rechar(str(time2))
        avr.rechar(str(times/tcount if tcount != 0 else 1))
        b_map.show()
        tcount += 1
        time2 = time.time()-time0

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"""KeyboardInterrupt

Screen size:        {se.screen_width}x{se.screen_height}
Average frame time: {avr.text}s
Frames drawn:       {tcount}""")
