from lib.winobj import WinObj
from lib.winobj_tri3d import Tri3D
from lib.utils import *

class Plane(WinObj):
    HALF_DIMS = 1000
    
    def __init__(self, window, pos, normal, color = "darkgreen"):
        super().__init__(window, pos)
        self.normal = normal
        self.color = color
        self.window.sim.onCreated(self)
        self.tris = []
        self.createTris()
            
    def destroy(self):
        super().destroy()
        
    def shouldBeCulled(self):
        # don't do auto-culling
        return False
    
    def createTris(self):
        # todo: deal with normal
        self.tris.append( Tri3D(self.window, self.pos + v3(-Plane.HALF_DIMS, 0, -Plane.HALF_DIMS),
                                             self.pos + v3(-Plane.HALF_DIMS, 0,  Plane.HALF_DIMS),
                                             self.pos + v3( Plane.HALF_DIMS, 0,  Plane.HALF_DIMS)) )
        self.tris.append( Tri3D(self.window, self.pos + v3(-Plane.HALF_DIMS, 0, -Plane.HALF_DIMS),
                                             self.pos + v3( Plane.HALF_DIMS, 0,  Plane.HALF_DIMS),
                                             self.pos + v3(-Plane.HALF_DIMS, 0, -Plane.HALF_DIMS)) )
        
    def updateGeo(self):
        # called when one of the transforms changed (like the camera) or pos change...update 3d -> 2d (pass on to tris)
        for tri in self.tris:
            tri.updateGfx()
    
    def update(self, deltaTime):
        super().update(deltaTime)
