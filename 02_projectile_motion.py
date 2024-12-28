from lib.window import Window
from lib.utils import *
from lib.winobj_circle import Circle

# Update method  ****** IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB ******
def updateCircleFunction(circle, deltaTime):
    # TODO...use circle.pos and circle.vel (both 2d vectors)
    pass


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
def clickReleaseFn(pos, vel):
    vel = limitMag(vel, 50)
    Circle(window, pos, 0.5, vel = vel, text = "A", color = "steelblue", updateFn = updateCircleFunction)
    
window = Window("Lab 02: Projectile Motion", subTitle = "Click, drag, and release to launch a ball (goal is for the ball to respond to velocity & gravity)...", clickReleaseFn = clickReleaseFn)
window.runGameLoop()
