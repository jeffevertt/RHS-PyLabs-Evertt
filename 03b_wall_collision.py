from lib.window import Window
from lib.utils import *
from lib.winobj_circle import Circle
from lib.winobj_wall import Wall

######### IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB ########
# The circle should collide with the wall and reflect/bounce off of it #
#   Wall properties (replace 'wall' with 'wallA' and 'wallB')...
#       wall.pos        point on the wall
#       wall.normal     vector facing away from the wall (perpendicular to the wall)
def updateCircleFunction(circle, deltaTime):
    # TODO...use circle.pos and circle.vel (both 2d vectors)
    pass


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
def clickReleaseFn(pos, vel):
    vel = limitMag(vel, 50)
    Circle(window, pos, 0.5, vel = vel, text = "A", color = "steelblue", updateFn = updateCircleFunction)
    
window = Window("Lab 03b: Wall Collision", subTitle = "Goal: Bounce the ball off both walls...", clickReleaseFn = clickReleaseFn)
wallA = Wall(window, v2( 8,0), v2(-1,1))
wallB = Wall(window, v2(-8,0), v2(1,-1))
window.runGameLoop()
