from lib.window import Window
from lib.utils import *
from lib.winobj_circle import Circle
from lib.winobj_obb import OBB
import random

####### IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB #######
# The ball should collide with the box and reflect/bounce off of it #
def updateBallFunction(ball, deltaTime):
    # TODO...use ball.pos and ball.vel (both 2d vectors)
    
    # collide with the box (use: box.pos, box.width, box.height, box.right(), box.up())
    pass


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
def clickReleaseFn(pos, vel):
    vel = limitMag(vel, 30)
    Circle(window, pos, 1.0, vel = vel, color = "yellow", updateFn = updateBallFunction)

window = Window("Lab 13b: Box(OBB) Collision", subTitle = "Goal: Bounce your ball off the box...", clickReleaseFn = clickReleaseFn)
box = OBB(window, v2(0,0), 10, 5, angle = random.random() * 60.0 + 20, color = "orange")
window.runGameLoop()
