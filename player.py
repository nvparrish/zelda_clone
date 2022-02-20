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
    """ A class for representing a player
    
    This could potentially could have some implementation pulled out into a base class to
    animate other creatures on the map
    """
    def __init__(self, texture = 'gfx/character.png'):
        """ Initialize the player object

        This method will populate a dictionary to encode the animation information from the image.
        Currently, the structure is hard-coded.  It would need to be more general for different
        animation types.

        The default textures came from https://opengameart.org/content/zelda-like-tilesets-and-sprites

        Keyword arguments:
        texture -- The texture to use for animating the player

        Returns:
        A Player object
        """
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
        self._animation_values[(Direction.UP, Action.HOLD)] = AnimationInfo(1, (16,32), (144,64))

        self._animation_values[(Direction.LEFT, Action.STAND)] = AnimationInfo(1, (16,32), (0,96))
        self._animation_values[(Direction.LEFT, Action.WALK)] = AnimationInfo(4, (16,32), (0,96))
        self._animation_values[(Direction.LEFT, Action.LIFT)] = AnimationInfo(3, (16,32), (80,96))
        self._animation_values[(Direction.LEFT, Action.CARRY)] = AnimationInfo(4, (16,32), (144,96))
        self._animation_values[(Direction.LEFT, Action.HOLD)] = AnimationInfo(1, (16,32), (144,96))

        self._timer = 0
        self._frame = 0
        self._player_direction = Direction.LEFT
        self._player_action = Action.CARRY

        self._position = (settings.WIDTH//2, settings.HEIGHT//2) # Currently in reference to the screen, using the upper-left corner
        self._scale = 2.0
        self._rotation = 0.0

    def set_direction(self, direction):
        """ Changes the player's direction

        Positional arguments:
        direction -- A Direction enumeration to assign to player's direction

        Returns:
        None

        Exceptions:
        Raises ValueError if input is not an Direction
        """
        if isinstance(direction, Direction):
            self._player_direction = direction
        else:
            raise ValueError()
    
    def set_action(self, action):
        """ Changes the player's action

        Positional arguments:
        action -- An Action enumeration to assign to player's action

        Returns:
        None

        Exceptions:
        Raises ValueError if input is not an Action
        """
        if isinstance(action, Action):
            self._player_action = action
        else:
            raise ValueError()

    def get_position(self):
        """ Returns the player position

        Returns:
        A Vector2 object representing the player position
        """
        return rl.Vector2(self._position[0], self._position[1])

    def draw(self, frame_time):
        """
        This function draws the player's sprite on the screen

        Positional arguments:
        frame_time -- the amount of time since the last frame, used to determine animation frame changes

        Returns:
        None
        """
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
        """ Manages a player's movements.  Uses frame time to scale by the fame rate.
            
            This checks key presses to handle movement.  The key pressing could be pulled
            into a separate class later. 
            
        Positional arguments:
        frame_time -- The time since the last frame, used to scale motion
        """
        velocity = [0, 0]
        if rl.is_key_down(rl.KEY_RIGHT):
            velocity[0] += 1
        if rl.is_key_down(rl.KEY_LEFT):
            velocity[0] -= 1
        if rl.is_key_down(rl.KEY_UP):
            velocity[1] -= 1
        if rl.is_key_down(rl.KEY_DOWN):
            velocity[1] += 1
        amplitude_sq = velocity[0]*velocity[0] + velocity[1]*velocity[1]
        if amplitude_sq < 1e-4: # Small threshold because of quantization
            # Don't change position, but change animation; no walking
            if self._player_action == Action.WALK: 
                self._player_action = Action.STAND
            elif self._player_action == Action.CARRY:
                self._player_action = Action.HOLD
        else:
            # Change the action for movement
            if self._player_action == Action.STAND:
                self._player_action = Action.WALK
            elif self._player_action == Action.HOLD:
                self._player_action = Action.CARRY

            # Set velocity and move
            velocity = [ x * settings.PLAYER_SPEED * frame_time / math.sqrt(amplitude_sq) for x in velocity ]
            self._position = [ x[0] + x[1] for x in zip(self._position, velocity) ]

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
        """ A function to rotate the player's sprite counter-clockwise 
        
        Positional arguments:
        frame_time -- the duration of the last frame, used to scale rotation rate

        Returns:
        None
        """
        self._rotation -= frame_time * 180 / 1.0 # 180 degrees per second clockwise
        self._rotation %= 360
        print("Rotation: ", self._rotation)

    def rotate_cw(self, frame_time):
        """ A function to rotate the player's sprite clockwise 
        
        Positional arguments:
        frame_time -- the duration of the last frame, used to scale rotation rate

        Returns:
        None
        """
        self._rotation += frame_time * 180 / 1.0 # 180 degrees per second counter-clockwise
        self._rotation %= 360
        print("Rotation: ", self._rotation)