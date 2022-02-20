import os
import player

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
        self._player = player.Player()
        self.camera = rl.Camera2D(rl.Vector2(settings.WIDTH//2, settings.HEIGHT//2), self._player.get_position(), 0, 1)

        self.debug_info = ""
    
    def run(self):
        # Main loop
        CHARACTER = rl.load_texture('gfx/character.png')
        while not rl.window_should_close():
            rl.begin_drawing()
            rl.begin_mode_2d(self.camera)
            rl.clear_background(rl.BLACK)
            rl.draw_text("Congrats!  You created your first window!", 190, 200, 20, rl.LIGHTGRAY)
            debug.debug(self.debug_info)
            frame_time = rl.get_frame_time()
            self._player.move(frame_time)
            self.camera.target = self._player.get_position()
            # rl.update_camera(self.camera)
            # self._player.rotate_cw(frame_time)
            self._player.draw(frame_time)
            rl.end_mode_2d(self.camera)
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
