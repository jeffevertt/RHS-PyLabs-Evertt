from lib.window import Window
from lib.utils import *
from lib.winobj_wall import Wall
from lib.winobj_obb import OBB
import random

# helper function - gets the vertices of the obb
#  TODO: calculate the four corners of the box and return them.
#           you can use rotateVec2 to help with this. 
#           you'll need to use: obb.pos obb.width, obb.height, and obb.angle
def calcObbCorners(obb: OBB):
    ul = obb.pos
    ur = obb.pos
    lr = obb.pos
    ll = obb.pos
    return [ ul, ur, lr, ll ]

####### IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB #######
# The box should collide with the floor & bounce off of it.
def updateBoxFunction(obb, deltaTime):
    # You will use obb.pos, obb.vel, obb.angle, and obb.angVel (pos & vel are 2d vectors...angle & angVel is a scalars)
    #   ...and for the wall, use wall.pos and wall.normal
    
    # check each corner for collision with the wall (use the provided helper function to get the corners)
    #   you'll want to find a single corner that is the deepest inside of the wall and use that for the next step
    # TODO
    
    # next, collision response (when there is a corner inside the wall)
    #   push it out, along the wall's normal, as you've done before
    #   calc relative velocity at contact point (inclusing the OBB's velocity & the effect of the angular velocity)
    #   once you have that, you need to apply it to linear & angular velocity. here's some code to help with that...
    #      rCrossN = cross(r, wall.normal)
    #      impulseMag = (-(1 + obb.restitution) * velAlongNormal)/((1/obb.mass) + (rCrossN * rCrossN) / obb.inertiaTensor)
    #      impulse = wall.normal * impulseMag
    #      obb.vel += (impulse / obb.mass)
    #      impulseAng = cross(r, impulse) # torque = r x impulse
    #      obb.angVel += math.degrees(impulseAng / obb.inertiaTensor)
    
    # finally, update pos/vel/angle (and you might want to damp the velocities)
    # TODO
    pass


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
def clickReleaseFn(pos, vel):
    vel = limitMag(vel, 15)
    obb = OBB(window, pos, 2, 2, vel = vel, color = "steelblue", updateFn = updateBoxFunction)
    obb.mass = 200
    obb.inertiaTensor = (obb.mass * (obb.width * obb.width + obb.height * obb.height)) / 12
    obb.restitution = 0.8
    obb.angVel = random.choice([-50,50])

window = Window("Lab 13c: Bouncy Box(OBB) - Collision & Response", subTitle = "Goal: Bounce the box off the floor...", clickReleaseFn = clickReleaseFn)
wall = Wall(window, v2(0, -10), v2(0,1))
window.runGameLoop()
