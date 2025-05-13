from lib.window import Window
from lib.utils import *
from lib.winobj_circle import Circle

# Update method  ****** IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB ******
# The goal here is to update the ball so that it behaves with physics as you expect.
#   The app already support creating circles (i.e. balls) with some initial velocity. 
# However, by default, they don't use that velocity. They just sit there. Run the app
# to see what I mean. Then figure out how to update "circle.pos" to apply the velocity
# to the position at each update timeslice. 
#   Then, apply some gravity (gravity at earths surface is -9.8 m/s^2)
def updateCircleFunction(circle, deltaTime):
    # TODO...use circle.pos and circle.vel (both 2d vectors)
    pass


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
def clickReleaseFn(pos, vel):
    vel = limitMag(vel, 50)
    Circle(window, pos, 0.5, vel = vel, color = "steelblue", updateFn = updateCircleFunction)

window = Window("Lab 02: Projectile Motion", subTitle = "Click, drag, and release to launch a ball (goal is for the ball to respond to velocity & gravity)...", clickReleaseFn = clickReleaseFn)
window.runGameLoop()
