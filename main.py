import os

os.environ["RAYLIB_BIN_PATH"] = "ext/raylib-2.0.0-Linux-amd64/lib/"
#os.environ["RAYLIB_BIN_PATH"] = "/usr/local/lib/" # Possible if 2.0.0 is system version 

import pyray as rl
import debug
import settings

class Game:
    def __init__(self):
        # Set up the window
        rl.init_window(settings.WIDTH, settings.HEIGHT, "Zelda Clone")
        rl.set_target_fps(60)

        self.debug_info = ""
    
    def run(self):
        # Main loop
        CHARACTER = rl.load_texture('gfx/character.png')
        while not rl.window_should_close():
            rl.begin_drawing()
            rl.clear_background(rl.BLACK)
            rl.draw_text("Congrats!  You created your first window!", 190, 200, 20, rl.LIGHTGRAY)
            debug.debug(self.debug_info)
            # rl.draw_texture(CHARACTER, 0, 0, rl.RAYWHITE)
            rl.draw_texture_rec(
                CHARACTER,
                rl.Rectangle(0, 0, 16, 32),
                rl.Vector2(20.0, 20.0),
                rl.RAYWHITE
            )
            rl.end_drawing()

        # clean up
        rl.close_window()

    def set_debug(self, info):
        self.debug_info  = info

    def reset_debug(self):
        self.debug_info  = ""

if __name__ == '__main__':
    game = Game()
    game.set_debug("hello :)")
    game.run()
