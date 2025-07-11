from lib.window_platformer import *
from lib.winobj_circle import *

# update functions (this is where your code goes)
def update(deltaTime, ball:Circle, rectangles:list[Rectangle], isKeyPressedFn):
    #TODO: Deal with collision with walls, motion, etc
    #       You can use isKeyPressedFn to determine if keys are pressed...
    #            Examples: isKeyPressedFn('space'), isKeyPressedFn('Right'), isKeyPressedFn('a')
    pass


####################################################################################################
######## In this lab, you design & implement a platformer (the user controls a blue dot &   ########
########  tries to collect all the yellow power points). You can use the mouse to place     ########
########  the platforms/rectangles (using left click & drag) and the power points (right    ########
########  click). You need to implement all of the motion for the player.                   ########
######## Get creative, make a challenging level. Extend the game. Also, ESCAPE resets.      ########
####################################################################################################
def createRect(window:Window, pos, width, height):
    return Rectangle(window, pos, width, height)
WindowPlatformer(updateFn = update, createRectFn = createRect).runGameLoop()