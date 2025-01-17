# 3d space - right handed, y up (z forward, x left)
from lib.window_physics3d import *
from lib.winobj_plane import Plane
from lib.utils import *
from typing import List

def setupLevel(window):
    # ground plane
    Plane(window, v3_zero(), v3_up())
    pass

####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
########################## EXCEPT TO REMOVE TUTORIAL GAME CONFIG ARGUMENT  #########################
####################################################################################################
WindowPhysics3D("Lab 18: Cuboid Physics!",
                setupLevelFn = setupLevel).runGameLoop()