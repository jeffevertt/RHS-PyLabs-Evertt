# 3d space - right handed, y up (z forward, x left)
from lib.window_create3d import *

# challenge 1: Create a cube
# challenge 2: Create a tetrahedron
#   optional: Rotate your tetrahedron in place using updateLevel & the modelToWorld matrix
# challenge 3: Create a polygonal pyramid (based has n-sides)
# challenge 4: Create a sphere
# challenge 5: Create your own scene

# setup level (called once when the level is created)
def setupLevel(addLine, addTri):
    #TODO: add your code here
    addLine( v3(-10,0,0), v3(10,0,0) ) # example (how to add a line)

# update world (called repeatedly)
def updateLevel(deltaTime, modelToWorld):
    #OPTIONAL: you can control how the model sits in the world with the modelToWorld transformation
    return m4x4Identity()


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
WindowCreate3D("Lab 12: Create 3D!",
               setupLevelFn = setupLevel, 
               updateLevelFn = updateLevel, 
               cameraPos = v3(0,0,-10)).runGameLoop()