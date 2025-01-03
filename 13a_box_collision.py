from lib.window import Window
from lib.utils import *
from lib.winobj_circle import Circle
from lib.winobj_rectangle import Rectangle

####### IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB #######
# The ball should collide with the box and reflect/bounce off of it #
def updateBallFunction(ball, deltaTime):
    # TODO...use ball.pos and ball.vel (both 2d vectors)
    
    # collide with the box (use: box.pos, box.width, box.height)
    pass
        


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
def clickReleaseFn(pos, vel):
    vel = limitMag(vel, 30)
    Circle(window, pos, 1.0, vel = vel, color = "hotpink", updateFn = updateBallFunction)

window = Window("Lab 13a: Box(AABB) Collision", subTitle = "Goal: Bounce your ball off the box...", clickReleaseFn = clickReleaseFn)
box = Rectangle(window, v2(0,0), 10, 5)
window.runGameLoop()
