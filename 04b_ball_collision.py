from lib.window import Window
from lib.utils import *
from lib.winobj_circle import Circle

############# IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB #############
# The circle should collide with the other balls and reflect/bounce off of them #
def updateFunction(circle, deltaTime):
    # TODO...use circle.pos and circle.vel (both 2d vectors)
    
    # collide with each ball (both balls should get an updated velocity)
    balls = [ ballA, ballB, ballC ]
    for ball in balls:
        pass


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
def clickReleaseFn(pos, vel):
    vel = limitMag(vel, 30)
    Circle(window, pos, 2.0, vel = vel, color = "steelblue", updateFn = updateFunction)
def updateBallFunction(ball, deltaTime):
    #ball.vel += window.gravity * deltaTime
    ball.pos += ball.vel * deltaTime
    
window = Window("Lab 4b: Ball Collision", subTitle = "Goal: Bounce your ball off the red balls...", clickReleaseFn = clickReleaseFn)
ballA = Circle(window, v2(5,0), 2.0, updateFn = updateBallFunction)
ballB = Circle(window, v2(-5,0), 2.0, updateFn = updateBallFunction)
ballC = Circle(window, v2(0,5), 2.0, updateFn = updateBallFunction)
window.runGameLoop()
