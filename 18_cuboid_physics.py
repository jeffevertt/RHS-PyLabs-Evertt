# 3d space - right handed, y up (z forward, x left)
from lib.window_physics3d import *
from lib.winobj_plane import Plane
from lib.winobj_cuboid import Cuboid
from lib.utils import *
from typing import List

# global state
bumpProgress = 0.0
bumpDirVec = v3_zero()

# functions
def setupLevel(window):
    # ground plane
    plane = Plane( window, v3(0, -10, 0), v3_up(), color = "green" )
    
    # cuboid
    cuboid = Cuboid( window, v3(0, 20, 0), v3(10, 10, 10), color = "#8A2BE2", vel = v3(2,15,0), velAng = v3(0,0,2) )
    cuboid.setCollisionPlane(plane)

def updateLevel(window, deltaTime):
    global bumpProgress
    global bumpDirVec

    # get the objects
    plane = window.sim.firstObjectOfType(Plane)
    cuboid = window.sim.firstObjectOfType(Cuboid)
    
    # plane "bump" support
    planeNeedsBumpUpdate = False
    if window.isKeyPressed("space"):
        # if starting
        if bumpProgress == 0:
            randFactor = 0.5
            bumpDirVec = unit( v3(randRange(-randFactor,randFactor),1,randRange(-randFactor,randFactor)) )
        if bumpProgress < 1:
            bumpProgress = min(bumpProgress + deltaTime * 5.0, 1.0)
            planeNeedsBumpUpdate = True
    elif bumpProgress > 0:
        bumpProgress = max(bumpProgress - deltaTime * 10.0, 0.0)
        planeNeedsBumpUpdate = True
    if planeNeedsBumpUpdate:
        posPrev = plane.pos
        plane.pos = v3(0, -10, 0) + (v3_up() * 4 + bumpDirVec * 2) * bumpProgress
        plane.vel = (plane.pos - posPrev) / max(deltaTime, 0.001)
    else:
        plane.vel = v3_zero()

    # keep the plane under the cuboid
    plane.pos = v3(cuboid.pos[0], plane.pos[1], cuboid.pos[2])
    plane.updateGeo(updateTris = True)

####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
########################## EXCEPT TO REMOVE TUTORIAL GAME CONFIG ARGUMENT  #########################
####################################################################################################
WindowPhysics3D("Lab 18: Cuboid Physics!", 
                cameraPos = v3(0,0,-50),
                setupLevelFn = setupLevel,
                updateLevelFn = updateLevel).runGameLoop()