import os

os.environ["RAYLIB_BIN_PATH"] = "ext/raylib-2.0.0-Linux-amd64/lib/"

import raylibpy

class Game:
    def __init__(self):
        pass
    
    def run(self):
        # Set up the window
        raylibpy.init_window(800, 450, "Zelda Clone")
        raylibpy.set_target_fps(60)

        # Main loop
        while not raylibpy.window_should_close():
            raylibpy.begin_drawing()
            raylibpy.clear_background(raylibpy.RAYWHITE)
            raylibpy.draw_text("Congrats!  You created your first window!", 190, 200, 20, raylibpy.LIGHTGRAY)
            raylibpy.end_drawing()

        # clean up
        raylibpy.close_window()

if __name__ == '__main__':
    game = Game()
    game.run()
