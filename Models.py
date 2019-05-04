import arcade
from random import randint, choice
from crashdetect import check_crash, check_crash_ship, check_crash_bonus
import time

MOVEMENT_SPEED = 5
MOVEMENT_ENEMY_SPEED = 3
MOVEMENT_BULLET_SPEED = 12
MOVEMENT_BONUS_SPEED = randint(10,15)
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
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.hp = 5

    def control(self, bonusspeed, direction):
         self.x += (MOVEMENT_SPEED+bonusspeed) * DIR_OFFSETS[direction][0]
         self.y += (MOVEMENT_SPEED+bonusspeed) * DIR_OFFSETS[direction][1]
        
    def out_of_world(self):
        if self.x > 550:
            self.x = -50
        elif self.x < -50:
            self.x = 550
        if self.y <= 26:
            self.y = 24
        elif self.y > 720:
            self.y = 720
    
    def check_hp(self):
        for i in self.world.enemy_list:
            if i.y <= -25:
                self.hp -= 1
            if self.hp == 0:
                self.world.die()

    def if_hit(self, enemy):
        return check_crash_ship(self.x, self.y, enemy.x, enemy.y)
    
    def update(self, delta):
        self.out_of_world()
        self.control(self.world.bonus_speed, self.direction)


class Bullet:
    def __init__(self,world, x, y):
        self.world = world
        self.x = x
        self.y = y

    def shoot(self, direction):
        self.y += MOVEMENT_BULLET_SPEED * DIR_OFFSETS[direction][1]

    def update(self, delta):
        self.shoot(DIR_UP)

class EnemyBullet:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

    def enemy_shoot(self, direction):
        self.y += MOVEMENT_BONUS_SPEED * DIR_OFFSETS[direction][1]

    def update(self, delta):
        self.enemy_shoot(DIR_DOWN)

class Enemy:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_DOWN

    def random_direction(self,morespeed, direction):
        self.y += (MOVEMENT_ENEMY_SPEED+morespeed) * DIR_OFFSETS[direction][1]
    
    
    def if_hit(self, bullet):
        return check_crash(bullet.x, bullet.y, self.x, self.y)
    
    def update(self, delta):
        self.random_direction(self.world.morespeed,self.direction)

class Bonus:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_DOWN
    
    def move_bonus(self, direction):
        self.y += MOVEMENT_BONUS_SPEED * DIR_OFFSETS[direction][1]
    
    def if_hit(self, ship):
        return check_crash_bonus(ship.x, ship.y, self.x, self.y)
    
    def update(self, delta):
        self.move_bonus(self.direction)


class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.state = World.STATE_FROZEN

        self.ship = Ship(self, 250, 50)
        self.bullet = Bullet(self,self.ship.x ,self.ship.y)
        self.enemy = Enemy(self, self.random_num(), 850)
        # self.enemybullet = EnemyBullet(self, self.enemy.x, self.enemy.y)
        self.bonus = Bonus(self,randint(50,450), 800)
        self.on_press = []
        self.bullet_list = []
        self.enemy_list = []
        self.bonus_list = []
        self.morespeed = 0
        self.score = 0
        self.count_time = 0
        self.time = 0
        self.bonus_speed = 0
        self.count_bonus_time = 0

        self.check_bonus = False
        self.has_shoot = False
            
    
    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.ship.direction = KEY_MAP[key]
            self.on_press.append(KEY_MAP[key])

        if key == arcade.key.SPACE:
            self.bullet = Bullet(self,self.ship.x ,self.ship.y+25)
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
            self.morespeed += 0.2
        if self.enemy_list[-1].y <= -25:
            self.ship.check_hp()
            self.enemy_list = []

    def gen_bonus(self):
        if self.time%23 == 3:
            if self.bonus_list == []:
                self.bonus = Bonus(self,randint(50,450), 800)
                self.bonus_list.append(self.bonus)
            if self.bonus_list[-1].y <= -25:
                self.bonus_list = []
                
    def random_num(self):
        list_check = [50,100,150,200,250,300,350,400,450]
        x = choice(list_check)
        return x

    def start(self):
        self.state = World.STATE_STARTED

    def freeze(self):
        self.state = World.STATE_FROZEN     

    def is_started(self):
        return self.state == World.STATE_STARTED

    def die(self):
        self.state = World.STATE_DEAD

    def is_dead(self):
        return self.state == World.STATE_DEAD 

    def Score(self):
        self.count_time += 1
        if self.count_time == 60:
            self.time += 1
            self.score = int(self.time)
            self.count_time = 0
    
    def check_bonus_hit(self):
        if self.bonus.if_hit(self.ship):
            for i in self.bonus_list:
                self.bonus_list.remove(i)
            self.check_bonus = True
        self.plus_speed()

    def plus_speed(self):
        if self.check_bonus:
            self.bonus_speed = 5
            self.count_bonus_time += 1
            if self.count_bonus_time//60 == 5:
                self.bonus_speed = 0
                self.count_bonus_time = 0
                self.check_bonus = False


    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return
        self.ship.update(delta)
        self.Score()
        self.bonus.update(delta)
        self.check_bonus_hit()
        # self.enemybullet.update(delta)
        for i in self.bullet_list:
            i.update(delta)
        for i in self.enemy_list:
            i.update(delta)
            if self.bullet_list != []:
                for bullet in self.bullet_list:
                    if i.if_hit(bullet):
                        self.bullet_list.remove(bullet)
                        self.enemy_list.remove(i)
            if self.ship.if_hit(i) and self.enemy_list != []:
                self.enemy_list.remove(i)
                self.ship.hp -= 1
                if self.ship.hp == 0:
                    self.die()