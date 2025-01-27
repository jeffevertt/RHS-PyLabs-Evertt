from lib.winobj import WinObj
from lib.winobj_tri3d import Tri3D
from lib.utils import *

class Plane(WinObj):
    HALF_DIMS = 100
    
    def __init__(self, window, pos, normal, color = "darkgreen"):
        super().__init__(window, pos)
        self.normal = unit(normal)
        self.color = color
        self.window.sim.onCreated(self)
        self.tris = []
        self.createTris()
            
    def destroy(self):
        super().destroy()
        
    def shouldBeCulled(self):
        # don't do auto-culling
        return False
    
    def basisX(self):
        basX = cross( self.normal, unit(v3(1,0,0)) )
        if length(basX) < 0.9:
            basX = cross( self.normal, unit(v3(0,1,0)) )
        return basX
    def basisY(self):
        return self.normal
    def basisZ(self):
        return cross( self.basisX(), self.basisY() )
    
    def createTris(self):
        self.tris.append( Tri3D(self.window, self.pos, self.pos, self.pos, color = self.color) )
        self.tris.append( Tri3D(self.window, self.pos, self.pos, self.pos, color = self.color) )
        self.updateTris()
    def updateTris(self):
        if len(self.tris) < 2:
            return
        basX = self.basisX()
        basZ = self.basisZ()
        self.tris[0].updateTriPositions(self.pos + basX * -Plane.HALF_DIMS + basZ * -Plane.HALF_DIMS,
                                        self.pos + basX * -Plane.HALF_DIMS + basZ *  Plane.HALF_DIMS,
                                        self.pos + basX *  Plane.HALF_DIMS + basZ *  Plane.HALF_DIMS)
        self.tris[1].updateTriPositions(self.pos + basX * -Plane.HALF_DIMS + basZ * -Plane.HALF_DIMS,
                                        self.pos + basX *  Plane.HALF_DIMS + basZ *  Plane.HALF_DIMS,
                                        self.pos + basX *  Plane.HALF_DIMS + basZ * -Plane.HALF_DIMS)
        
    def updateGeo(self, updateTris = False):
        # if requested, update the tri positions (so the 3d positions, not just the projected 2d ones)
        if updateTris:
            self.updateTris()
        # called when one of the transforms changed (like the camera) or pos change...update 3d -> 2d (pass on to tris)
        for tri in self.tris:
            tri.updateGfx()
    
    def update(self, deltaTime):
        super().update(deltaTime)
