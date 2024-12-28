from lib.window import Window
from lib.utils import *
from lib.winobj_circle import Circle
from lib.winobj_rectangle import Rectangle

####### IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB #######
# The ball should collide with the box and reflect/bounce off of it #
def updateBallFunction(ball, deltaTime):
    ball.pos += ball.vel * deltaTime
    
    # collide with box
    closestPt = clampV2(ball.pos, box.pos - v2(box.width/2,box.height/2), box.pos + v2(box.width/2,box.height/2))
    if length(ball.pos - closestPt) > 0.00001:
        dst = length(ball.pos - closestPt) - ball.radius
        normal = unit(ball.pos - closestPt)
    else:
        dst = -ball.radius
        normal = unit(ball.pos - box.pos)
    if dst < 0:
        ball.pos -= normal * dst
        ball.vel += normal * (ball.vel @ normal * -2)
        


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
def clickReleaseFn(pos, vel):
    vel = limitMag(vel, 30)
    Circle(window, pos, 1.0, vel = vel, color = "hotpink", updateFn = updateBallFunction)

window = Window("Lab 13a: Box(AABB) Collision", subTitle = "Goal: Bounce your ball off the box...", clickReleaseFn = clickReleaseFn)
box = Rectangle(window, v2(0,0), 10, 5)
window.runGameLoop()
