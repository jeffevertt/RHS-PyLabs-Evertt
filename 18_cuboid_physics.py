# 3d space - right handed, y up (z forward, x left)
from lib.window_physics3d import *
from lib.winobj_tri3d import Tri3D
from lib.winobj_plane import Plane
from lib.utils import *
from typing import List

def setupLevel(window):
    # ground plane
    Plane(window, v3(0,-5,0), v3_up())
    
    # cuboid
    pass #TODO

def updateLevel(window, deltaTime):
    pass

####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
########################## EXCEPT TO REMOVE TUTORIAL GAME CONFIG ARGUMENT  #########################
####################################################################################################
WindowPhysics3D("Lab 18: Cuboid Physics!",
                setupLevelFn = setupLevel,
                updateLevelFn = updateLevel).runGameLoop()