#!/usr/bin/python3

import scrap_engine as se
from pynput import keyboard

map=se.Map(background=" ")
player=se.Object(char="T")
rock=se.Object(char="A")

player.add(map, 0,0)

class Pad(se.Object):
    def action(self):
        player.remove()

pad=Pad(char="i", state="float")

rock.add(map, 10, 10)

pad.add(map, 10, 20)

map.show()

while True:
    with keyboard.Events() as events:
    # Block for as much as possible
        event = events.get(1e6)
        if event.key == keyboard.KeyCode.from_char('w'):
            player.set(player.x, player.y-1)
        elif event.key == keyboard.KeyCode.from_char('a'):
            player.set(player.x-1, player.y)
        elif event.key == keyboard.KeyCode.from_char('s'):
            player.set(player.x, player.y+1)
        elif event.key == keyboard.KeyCode.from_char('d'):
            player.set(player.x+1, player.y)
    map.show()
