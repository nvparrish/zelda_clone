import pyray as rl
import settings
import math

from enum import Enum

class Direction(Enum):
    DOWN = 0
    RIGHT = 1
    UP = 2
    LEFT = 3

class Action(Enum):
    STAND = 0
    WALK = 1
    LIFT = 2
    CARRY = 3
    HOLD = 4

class AnimationInfo:
    def __init__(self, frame_count, sprite_size, offset):
        self.frame_count = frame_count
        self.sprite_size = sprite_size
        self.offset = offset

class Player:
    """
    The textures came from https://opengameart.org/content/zelda-like-tilesets-and-sprites

    """
    def __init__(self, texture = 'gfx/character.png'):

        self._texture =  rl.load_texture(texture)

        self._animation_values = {}
        self._animation_values[(Direction.DOWN, Action.STAND)] = AnimationInfo(1, (16,32), (0,0))
        self._animation_values[(Direction.DOWN, Action.WALK)] = AnimationInfo(4, (16,32), (0,0))
        self._animation_values[(Direction.DOWN, Action.LIFT)] = AnimationInfo(3, (16,32), (80,0))
        self._animation_values[(Direction.DOWN, Action.CARRY)] = AnimationInfo(4, (16,32), (144,0))
        self._animation_values[(Direction.DOWN, Action.HOLD)] = AnimationInfo(1, (16,32), (144,0))

        self._animation_values[(Direction.RIGHT, Action.STAND)] = AnimationInfo(1, (16,32), (0,32))
        self._animation_values[(Direction.RIGHT, Action.WALK)] = AnimationInfo(4, (16,32), (0,32))
        self._animation_values[(Direction.RIGHT, Action.LIFT)] = AnimationInfo(3, (16,32), (80,32))
        self._animation_values[(Direction.RIGHT, Action.CARRY)] = AnimationInfo(4, (16,32), (144,32))
        self._animation_values[(Direction.RIGHT, Action.HOLD)] = AnimationInfo(1, (16,32), (144,32))

        self._animation_values[(Direction.UP, Action.STAND)] = AnimationInfo(1, (16,32), (0,64))
        self._animation_values[(Direction.UP, Action.WALK)] = AnimationInfo(4, (16,32), (0,64))
        self._animation_values[(Direction.UP, Action.LIFT)] = AnimationInfo(3, (16,32), (80,64))
        self._animation_values[(Direction.UP, Action.CARRY)] = AnimationInfo(4, (16,32), (144,64))
        self._animation_values[(Direction.UP, Action.HOLD)] = AnimationInfo(4, (16,32), (144,64))

        self._animation_values[(Direction.LEFT, Action.STAND)] = AnimationInfo(4, (16,32), (0,96))
        self._animation_values[(Direction.LEFT, Action.WALK)] = AnimationInfo(4, (16,32), (0,96))
        self._animation_values[(Direction.LEFT, Action.LIFT)] = AnimationInfo(3, (16,32), (80,96))
        self._animation_values[(Direction.LEFT, Action.CARRY)] = AnimationInfo(4, (16,32), (144,96))
        self._animation_values[(Direction.LEFT, Action.HOLD)] = AnimationInfo(4, (16,32), (144,96))

        self._timer = 0
        self._frame = 0
        self._player_direction = Direction.LEFT
        self._player_action = Action.CARRY

        self._position = (settings.WIDTH//2, settings.HEIGHT//2) # Currently in reference to the screen, using the upper-left corner
        self._scale = 2.0
        self._rotation = 0.0

    def set_direction(self, direction):
        self._player_direction = direction
    
    def set_action(self, action):
        self._player_action = action

    def draw(self, frame_time):
        self._timer += frame_time
        animation_values = self._animation_values[(self._player_direction, self._player_action)]
        if (self._timer >= 0.2): 
            self._timer = 0.0
            self._frame += 1
            if (self._player_action == Action.LIFT and 
                    self._frame >= animation_values.frame_count):
                self._player_action = Action.HOLD # Or CARRY, if moving
        
        self._frame = self._frame % animation_values.frame_count
        o = animation_values.offset
        s = animation_values.sprite_size

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
                rl.Vector2(s[0], s[1]),
                self._rotation,
                self._scale,
                rl.RAYWHITE
        ) 

    def move(self, frame_time):
        velocity = [0, 0]
        if rl.is_key_down(rl.KEY_RIGHT):
            velocity[0] += 1
        if rl.is_key_down(rl.KEY_LEFT):
            velocity[0] -= 1
        if rl.is_key_down(rl.KEY_UP):
            velocity[1] -= 1
        if rl.is_key_down(rl.KEY_DOWN):
            velocity[1] += 1
        amplitude = velocity[0]*velocity[0] + velocity[1]*velocity[1]
        if amplitude < 1e-5:
            pass # Don't change position or scale speed
        else:
            if abs(velocity[0]) == abs(velocity[1]):
                # A player moving diagonally could face either direction
                possible_directions = []
                possible_directions.append(Direction.LEFT if velocity[0] < 0 else Direction.RIGHT)
                possible_directions.append(Direction.UP if velocity[1] < 0 else Direction.DOWN)
                if not self._player_direction in possible_directions:
                    # Favor the direction the player was already facing, but only if it is in the angle direction
                    self._player_direction = possible_directions[0]
            elif abs(velocity[0]) > abs(velocity[1]):
                # Player is moving right or left
                if velocity[0] < 0:
                    self._player_direction = Direction.LEFT
                else:
                    self._player_direction = Direction.RIGHT
            else:
                # Player is moving up or down
                if velocity[1] < 0:
                    self._player_direction = Direction.UP
                else:
                    self._player_direction = Direction.DOWN

    def rotate_ccw(self, frame_time):
        self._rotation -= frame_time * 180 / 1.0 # 180 degrees per second clockwise
        self._rotation %= 360
        print("Rotation: ", self._rotation)

    def rotate_cw(self, frame_time):
        self._rotation += frame_time * 180 / 1.0 # 180 degrees per second counter-clockwise
        self._rotation %= 360
        print("Rotation: ", self._rotation)