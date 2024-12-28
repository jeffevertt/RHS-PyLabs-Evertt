from lib.window_create3d import *

# challenge 1: Create a cube
# challenge 2: Create a tetrahedron
#   optional: Rotate your tetrahedron in place using updateLevel & the modelToWorld matrix
# challenge 3: Create a polygonal pyramid (based has n-sides)
# challenge 4: Create a sphere
# challenge 5: Create your own scene

def createCube(center, halfDims, addLine):
    verts = [ 
        v3(-halfDims[0], halfDims[1], -halfDims[2]) + center,
        v3(-halfDims[0], halfDims[1],  halfDims[2]) + center,
        v3( halfDims[0], halfDims[1],  halfDims[2]) + center,
        v3( halfDims[0], halfDims[1], -halfDims[2]) + center,
        v3(-halfDims[0],-halfDims[1], -halfDims[2]) + center,
        v3(-halfDims[0],-halfDims[1],  halfDims[2]) + center,
        v3( halfDims[0],-halfDims[1],  halfDims[2]) + center,
        v3( halfDims[0],-halfDims[1], -halfDims[2]) + center ]
    for i in range(4):
        addLine( verts[i], verts[(i + 1) % 4] )
        addLine( verts[i + 4], verts[(i + 1) % 4 + 4] )
        addLine( verts[i], verts[i % 4 + 4] )
def createTetrahedron(center, radius, height, addLine):
    verts = [ v3(0, height, 0) + center ]
    offset = v3_forward() * radius
    for i in range(3):
        verts.append( center + offset )
        offset = m3x3RotY(120) @ offset
    for i in range(3):
        addLine( verts[i + 1], verts[0] )
        addLine( verts[i + 1], verts[(i + 1) % 3 + 1] )

# setup level (called once when the level is created)
def setupLevel(addLine):
    # challenge 1: Create a cube
    createCube(v3(0,0,0), v3(5, 5, 5), addLine)
    createTetrahedron(v3(0,-2,0), 4, 4, addLine)

# update world (called repeatedly)
def updateLevel(deltaTime, modelToWorld):
    return modelToWorld @ m4x4RotY(deltaTime * 50)


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
WindowCreate3D(setupLevelFn = setupLevel, 
               updateLevelFn = updateLevel, 
               cameraPos = v3(0,0,-10)).runGameLoop()