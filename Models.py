import arcade
from random import randint

MOVEMENT_SPEED = 5
MOVEMENT_BULLET_SPEED = 12
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

class Bullet:
    def __init__(self,world, Horizon, Vertical):
        self.world = world
        self.horizon = Horizon
        self.vertical = Vertical

    def shoot(self, direction):
        self.vertical += MOVEMENT_BULLET_SPEED * DIR_OFFSETS[direction][1]

    def update(self, delta):
        self.shoot(DIR_UP)

class Enemy:
    def __init__(self, world, Horizon, Vertical):
        self.world = world
        self.horizon = Horizon
        self.vertical = Vertical
        self.direction = DIR_DOWN
        self.enemy_list = []

    def move(self, direction):
        self.horizon += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.vertical += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]
    
    def random_direction(self, direction):
        x = randint(1,2)
        if x == 1:
            self.direction = DIR_LEFT
        elif x == 2:
            self.direction = DIR_RIGHT
    
    def update(self, delta):
        self.move(self.direction)
        # self.random_direction(self.direction)
    

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.ship = Ship(self, 250, 50)
        self.bullet = Bullet(self,self.ship.horizon ,self.ship.vertical)
        self.enemy = Enemy(self, 250, 650)
        self.on_press = []
        self.bullet_list = []

        self.has_shoot = False
    
    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.ship.direction = KEY_MAP[key]
            self.on_press.append(KEY_MAP[key])
        if key == arcade.key.SPACE:
            self.bullet = Bullet(self,self.ship.horizon ,self.ship.vertical+25)
            self.has_shoot = True
            self.bullet_list.append(self.bullet)

    
    def on_key_release(self, key, key_modifiers):
        if key in KEY_MAP:
            self.on_press.remove(KEY_MAP[key])
            if self.on_press == []:
                self.ship.direction = DIR_STILL
            elif self.check_on_key():
                if self.ship.direction == DIR_RIGHT:
                    self.ship.direction = DIR_LEFT
                else:
                    self.ship.direction = DIR_RIGHT
    
    def check_on_key(self):
        if self.ship.direction in self.on_press:
            return False
        else:
            return True

    def update(self, delta):
        self.ship.update(delta)
        for i in self.bullet_list:
            i.update(delta)
        self.enemy.update(delta)
        

    

