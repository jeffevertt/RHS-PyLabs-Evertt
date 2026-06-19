from lib.window import Window
from lib.utils import *
from lib.winobj_circle import Circle
from lib.winobj_wall import Wall

######### IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB #########
# Figure out the angle to launch the ball in order to hit the target.   #
#   You are a launch position and a target position.                    #
#   You are provided a velocity in the x which you should use.          #
#   The angle you return should be in degrees, relative to std position.#
def calcLaunchAngle(launchPos :v2, targetPos :v2, velX):
    # setup
    gravityY = window.gravity[1]
    
    # TODO...figure out the angle you will need to launch the projectile in order to hit the target
    return 45  # replace this (defaulting to 45 degrees till your code is in)



####################################################################################################
############################### DO NOT MODIFY METHODS BELOW THIS LINE ##############################
####################################################################################################
hitCount, target = 0, None
def updateBallFunction(ball: Circle, deltaTime):
    global hitCount
    ball.vel += ball.window.gravity * deltaTime
    ball.pos += ball.vel * deltaTime
    window :Window = ball.window
    if length(ball.pos - target.pos) < (ball.radius + target.radius):
        ball.destroy()
        target.destroy()
        createRandomTarget()
        hitCount += 1
        window.updateSubTitle("Well Done!!!" + ("" if hitCount < 2 else f" x{hitCount}"))
def clickReleaseFn(pos, vel):
    velX = 10.0
    angDeg = calcLaunchAngle(pos, target.pos, velX)
    vel = v2(velX, tanDeg(angDeg) * velX)
    Circle(window, pos, 0.5, vel, color = "steelblue", updateFn = updateBallFunction)
def createRandomTarget():
    global target
    if target is not None:
        target.destroy()
    target = Circle(window, v2(window.maxCoordinateX() + randRange(-8,-1), randRange(window.minCoordinateY() + 1, window.minCoordinateY() + 15)), 0.5, text = "T", color = "red")
    
window = Window("Lab 05b: Launch Vector", subTitle = "Write some code to determine the launch vector to hit a target...", clickReleaseFn = clickReleaseFn)
createRandomTarget()
window.runGameLoop()
