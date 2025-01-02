from lib.window import Window
from lib.utils import *
from lib.winobj_circle import Circle

############## IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB ############
### The circle should collide with the other ball and reflect/bounce off of it ##
## Access the moving ball, circle, using circle.pos, circle.vel, circle.radius ##
####### ball that's stuck in one place is ball (use ball.pos & ball.radius) #####
#################################################################################
def updateFunction(circle, deltaTime):
    # TODO...use circle.pos and circle.vel (both 2d vectors)
    pass


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
def clickReleaseFn(pos, vel):
    vel = limitMag(vel, 30)
    Circle(window, pos, 0.5, vel = vel, text = "A", color = "steelblue", updateFn = updateFunction)
    
window = Window("Lab 4a: Ball Collision", subTitle = "Goal: Bounce your ball off the red ball...", clickReleaseFn = clickReleaseFn)
ball = Circle(window, v2(0,0), 2.0)
window.runGameLoop()
