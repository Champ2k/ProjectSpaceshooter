import arcade
from crashdetect import *
from Models import World,Ship,Bullet,Enemy


WIDTH = 500
HEIGHT = 750

class SpaceWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)
        self.background = arcade.load_texture('background.png')
        self.world = World(WIDTH, HEIGHT) 
        self.Shipsprite = ModelSprite('Character\Ship.png',
                                        model=self.world.ship)

        self.Bulletsprite = ModelSprite('Character\Bullet.png',
                                        model=self.world.bullet)
        
        self.Enemysprite = ModelSprite('Character\Enemy1.png',
                                        model=self.world.enemy)
        
        self.set_update_rate(1/70)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(WIDTH // 2, HEIGHT // 2,
                                      WIDTH, HEIGHT, self.background)
        
        self.Shipsprite.draw()

        self.draw_shoot()

        self.draw_enemy()
        
        self.check_state()

        self.score_draw()
    
    def draw_enemy(self):
        self.world.gen_enemy()
        for i in self.world.enemy_list:
            ModelSprite('Character\Enemy1.png',
                                        model=i).draw()

    
    def draw_shoot(self):
        for i in self.world.bullet_list:
            ModelSprite('Character\Bullet.png',
                                        model=i).draw()
    
    def on_key_press(self, key, key_modifiers):
         self.world.on_key_press(key, key_modifiers)
         if not self.world.is_dead():
             self.world.start()
    
    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def game_over_draw(self):
        
        output = "GameOver"
        arcade.draw_text(output,173,350,arcade.color.WHITE,30)

    def game_start_draw(self):
        
        output = "Press any keys"
        output_2 = "To start"
        arcade.draw_text(output,150,380,arcade.color.WHITE,30)
        arcade.draw_text(output_2,200,330,arcade.color.WHITE,30)
    
    def score_draw(self):
        output = f"Score {self.world.score}"
        arcade.draw_text(output,380,700,arcade.color.WHITE,20)

    def check_state(self):
        if self.world.state == World.STATE_DEAD:
            self.game_over_draw()
        if self.world.state == World.STATE_FROZEN:
            self.game_start_draw()

    def update(self, delta):
        self.world.update(delta)

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.horizon, self.model.vertical)

    def draw(self):
        self.sync_with_model()
        super().draw()


def main():
    SpaceWindow(WIDTH, HEIGHT)
    arcade.run()

if __name__ == '__main__':
    window = SpaceWindow(WIDTH, HEIGHT)
    arcade.run()