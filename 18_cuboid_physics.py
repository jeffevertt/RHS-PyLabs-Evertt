# 3d space - right handed, y up (z forward, x left)
from lib.window_create3d import *
from lib.utils import *
from typing import List

def setupLevel(addLine, addTri):
    addTri( v3(   0,0,10), v3( 10,0,10), v3( 0,10,10) )
    
    addLine( v3(  0,0,10), v3( 10, 0,10) )
    addLine( v3(  0,0,10), v3(  0,10,10) )
    addLine( v3(  0,0,10), v3(  0, 0,20) )

####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
########################## EXCEPT TO REMOVE TUTORIAL GAME CONFIG ARGUMENT  #########################
####################################################################################################
WindowCreate3D("Lab 18: Cuboid Physics!",
               setupLevelFn = setupLevel).runGameLoop()