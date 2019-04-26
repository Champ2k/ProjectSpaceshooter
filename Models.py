import arcade
from random import randint, choice
from crashdetect import check_crash

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
        # self.next_direction = DIR_STILL

    def control(self, direction):
         self.horizon += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
         self.vertical += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]
        
    def out_of_world(self):
        if self.horizon > 550:
            self.horizon = -50
        elif self.horizon < -50:
            self.horizon = 550
        if self.vertical <= 26:
            self.vertical = 24
        elif self.vertical > 720:
            self.vertical = 720
    
    def update(self, delta):
        self.out_of_world()
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
        self.hp = 3
    
    def random_direction(self, direction):
        self.vertical += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]
    
    def if_hit(self, bullet):
        return check_crash(bullet.horizon, bullet.vertical, self.horizon, self.vertical)
    
    def update(self, delta):
        self.random_direction(self.direction)

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.ship = Ship(self, 250, 50)
        self.bullet = Bullet(self,self.ship.horizon ,self.ship.vertical)
        self.enemy = Enemy(self, randint(50,450), 850)
        self.on_press = []
        self.bullet_list = []
        self.enemy_list = []
        

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

    def gen_enemy(self):
        if self.enemy_list == []:
            for i in range(randint(1,5)):
                self.enemy = Enemy(self, self.random_num(), 850)
                self.enemy_list.append(self.enemy)
        if self.enemy_list[-1].vertical == -25:
            self.enemy_list = []        

    def random_num(self):
        list_check = [50,100,150,200,250,300,350,400,450]
        x = choice(list_check)
        return x
    
    # def kill(self):
    #     for i in self.enemy_list:
    #         if self.bullet_list != []:
    #                 for bullet in self.bullet_list:
    #                     if i.if_hit(bullet):
    #                         self.enemy_list.remove(i)
    #                         self.bullet_list.remove(bullet)

    def update(self, delta):
        self.ship.update(delta)
        for i in self.bullet_list:
            i.update(delta)
        for i in self.enemy_list:
            i.update(delta)
            # self.kill()
            if self.bullet_list != []:
                for bullet in self.bullet_list:
                    if i.if_hit(bullet):
                        self.bullet_list.remove(bullet)
                        self.enemy_list.remove(i)
