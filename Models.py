import arcade
from random import randint

MOVEMENT_SPEED = 5
DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4

KEY_MAP = { arcade.key.UP: DIR_UP,
            arcade.key.DOWN: DIR_DOWN,
            arcade.key.LEFT: DIR_LEFT,
            arcade.key.RIGHT: DIR_RIGHT, }
 
DIR_OFFSETS = { DIR_STILL: (0,0),
                DIR_UP: (0,1),
                DIR_RIGHT: (1,0),
                DIR_DOWN: (0,-1),
                DIR_LEFT: (-1,0) }

class Ship:
    def __init__(self, world, horizon, vertical):
        self.world = world
        self.horizon = horizon
        self.vertical = vertical
        self.direction = DIR_STILL

    def control(self, direction):
         self.horizon += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
         self.vertical += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]
    
    def update(self, delta):
        self.control(self.direction) 

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.ship = Ship(self, 295, 50)

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.ship.direction = KEY_MAP[key]
    
    def on_key_release(self, key, key_modifiers):
        if key in KEY_MAP:
            self.ship.direction = DIR_STILL

    def update(self, delta):
        self.ship.update(delta)

    

