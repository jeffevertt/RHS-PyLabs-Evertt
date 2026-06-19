from lib.window import Window
from lib.utils import *
from lib.winobj_circle import Circle
from lib.winobj_wall import Wall

######### IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB ########
# Stop the ball when it hits the ground (set its velocity to zero)     #
def updateCircleFunction(circle :Circle, deltaTime):
    # setup
    groundHeight = ground.pos[1]
    circle.vel += circle.window.gravity * deltaTime
    
    # TODO...check for a collision with the ground, set the ball's velocity to zero.
    
    # update position
    circle.pos += circle.vel * deltaTime


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
def clickReleaseFn(pos, vel):
    Circle(window, pos, 0.5, vel = v2(0,0), text = "A", color = "steelblue", updateFn = updateCircleFunction)
    
window = Window("Lab 02c: Projectile v Ground", subTitle = "Stop the ball when it hits the ground...", clickReleaseFn = clickReleaseFn)
ground = Wall(window, v2(0,-8), v2(0,1))
window.runGameLoop()
