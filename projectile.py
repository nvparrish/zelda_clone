import math
import pyray as rl
from animation_info import AnimationInfo
from enum import Enum

class Stage(Enum):
    START = 0
    MIDDLE = 1
    END = 2
    DEAD = 3

class Projectile:
    def __init__(self,
                src,
                dst,
                start_animation: AnimationInfo = None, 
                middle_animation: AnimationInfo = None, 
                end_animation: AnimationInfo = None,
                texture='gfx/NES - Magician - Magic Effects.png',
                scale = 1.0,
                speed = 5.0):

        self._texture = rl.load_texture(texture)
        self._animations = {}
        if not start_animation:
            self._animations[Stage.START] = AnimationInfo(1, (16,16), (0, 150))
        if not middle_animation:
            self._animations[Stage.MIDDLE] = AnimationInfo(8, (20,20), (3,250))
        if not end_animation:
            self._animations[Stage.END] = AnimationInfo(6, (20, 20), (3, 59))
        self._stage = Stage.START
        self._timer = 0.0
        self._frame = 0
        self._angle = math.atan2(dst[1]-src[1], dst[0]-src[0])
        self._scale = scale
        self._frame_rate = 0.1
        self._speed = speed
        self._position = src
        self._src = src
        self._dst = dst
    
    def draw(self, frame_time):
        if self._stage == Stage.DEAD:
            return # Don't draw dead projectiles

        self._timer += frame_time
        if (self._timer >= self._frame_rate): 
            self._timer = 0.0
            self._frame += 1
            if (self._stage == Stage.START):
                if (self._frame >= self._animations[self._stage].frame_count):
                    self._stage = Stage.MIDDLE
                    self._frame = 0
            elif (self._stage == Stage.MIDDLE):
                self._frame %= self._animations[self._stage].frame_count
            elif (self._stage == Stage.END):
                if (self._frame >= self._animations[self._stage].frame_count):
                    self._stage = Stage.DEAD
                    return
        
        o = self._animations[self._stage].offset
        s = self._animations[self._stage].sprite_size

        """rl.draw_texture_rec(
                self._texture,
                rl.Rectangle(o[0] + self._frame * s[0], o[1], 
                             s[0], s[1]),
                rl.Vector2(self._position[0], self._position[1]),
                rl.RAYWHITE
            )"""
        rl.draw_texture_tiled(self._texture,
                rl.Rectangle(o[0] + self._frame * s[0], o[1], 
                             s[0], s[1]),
                rl.Rectangle(self._position[0], self._position[1],
                            s[0]*self._scale, s[1]*self._scale),
                rl.Vector2(s[0]*self._scale/2, s[1]*self._scale/2),
                self._angle * 180/(math.pi),
                self._scale,
                rl.RAYWHITE
        ) 

    def move(self, frame_time):
        if (self._stage == Stage.MIDDLE):
            self._position = (self._position[0] + self._speed * math.cos(self._angle), 
                                self._position[1] + self._speed * math.sin(self._angle))
            if (self._position[0]-self._src[0])**2 + (self._position[1]-self._src[1])**2 >= \
                    (self._dst[0]-self._src[0])**2 + (self._dst[1]-self._src[1])**2:
                self._stage = Stage.END
                self._frame = 0
                self._position = self._dst
    
    def is_dead(self):
        return self._stage == Stage.DEAD # Returns True if DEAD