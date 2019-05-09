import arcade
from Models import World, Ship, Bullet, Enemy, Heart
from Fps import FPSCounter


WIDTH = 500
HEIGHT = 750

class SpaceWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)
        self.background = arcade.load_texture('background.png')

        self.game_setup(width, height)

    def game_setup(self, width, height):
        self.world = World(WIDTH, HEIGHT) 
        
        self.Shipsprite = ModelSprite('Character\Ship.png',
                                        model=self.world.ship)

        self.Bulletsprite = ModelSprite('Character\Bullet.png',
                                        model=self.world.bullet)
        
        self.Enemysprite = ModelSprite('Character\Enemy1.png',
                                        model=self.world.enemy)
        
        self.Bonussprite= ModelSprite('Character\Bonus.png',
                                        model=self.world.bonus)
        
        self.set_update_rate(1/70)

        self.fps = FPSCounter()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(WIDTH // 2, HEIGHT // 2,
                                      WIDTH, HEIGHT, self.background)
        
        self.Shipsprite.draw()

        self.draw_shoot()

        self.draw_enemy()

        self.draw_hp()
        
        self.check_state()

        self.score_draw()

        self.draw_bonus()

        self.fps.tick()

        arcade.draw_text(f'FPS: {self.fps.get_fps():.0f}', WIDTH - 40, HEIGHT - 20, arcade.color.WHITE, 10)

    def draw_enemy(self):
        self.world.gen_enemy()
        for i in self.world.enemy_list:
            ModelSprite('Character\Enemy1.png',
                                        model=i).draw()

    def draw_shoot(self):
        for i in self.world.bullet_list:
            ModelSprite('Character\Bullet.png',
                                        model=i).draw()
    
    def draw_bonus(self):
        self.world.gen_bonus()
        for i in self.world.bonus_list:
            ModelSprite('Character\Bonus.png',
                                        model=i).draw()
    
    def draw_hp(self):
        for i in self.world.hp_list:
            if i.has_live:
                ModelSprite("Character\Full Heart.png",
                                            model=i).draw()

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)
        if not self.world.is_dead():
             self.world.start()
        if key == arcade.key.R and self.world.state == World.STATE_DEAD:
            self.game_setup(WIDTH, HEIGHT)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def game_over_draw(self):
        output = "GameOver"
        output_2 = "Press R to play again"
        output_3 = f"Total time : {self.world.time}"
        output_4 = f"Total Score: {self.world.score}"
        arcade.draw_text(output, WIDTH-315, HEIGHT-325, arcade.color.WHITE, 25)
        arcade.draw_text(output_3, WIDTH-334, HEIGHT-360, arcade.color.WHITE, 25)
        arcade.draw_text(output_4, WIDTH-334, HEIGHT-395, arcade.color.WHITE, 25)
        arcade.draw_text(output_2, WIDTH-373, HEIGHT-430, arcade.color.WHITE, 25)

    def game_start_draw(self):
        output = "Press any keys"
        output_2 = "To start"
        arcade.draw_text(output, WIDTH - 350, (HEIGHT/2) + 20, arcade.color.WHITE,30)
        arcade.draw_text(output_2, WIDTH - 300, (HEIGHT/2) - 20, arcade.color.WHITE,30)
    
    def score_draw(self):
        output = f"Score: {self.world.score}"
        arcade.draw_text(output, WIDTH - 130, HEIGHT - 25, arcade.color.WHITE,20)

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
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()


def main():
    SpaceWindow(WIDTH, HEIGHT)
    arcade.run()

if __name__ == '__main__':
    window = SpaceWindow(WIDTH, HEIGHT)
    arcade.run()