from lib.winobj import WinObj
from lib.winobj_tri3d import Tri3D
from lib.winobj_line import Line
from lib.utils import *

class Cuboid(WinObj):
    def __init__(self, window, pos, halfDims, vel = v3_zero(), orient = m3x3Identity(), color = "darkseagreen"):
        super().__init__(window, pos, vel = vel)
        self.halfDims = halfDims
        self.orient = orient
        self.color = color
        self.window.sim.onCreated(self)
        self.tris = []
        self.lines = []
        self.createGeo()
            
    def destroy(self):
        super().destroy()
        
    def shouldBeCulled(self):
        # don't do auto-culling
        return False
    
    def basisX(self):
        return self.orient[0, :]
    def basisY(self):
        return self.orient[1, :]
    def basisZ(self):
        return self.orient[2, :]
    def modelToWorld(self):
        return m4x4ModelToWorld(self.orient, self.pos)
    
    def calcVerts(self):
        return [ self.pos + self.orient @ v3( self.halfDims[0], -self.halfDims[1], -self.halfDims[2]),
                 self.pos + self.orient @ v3( self.halfDims[0], -self.halfDims[1],  self.halfDims[2]),
                 self.pos + self.orient @ v3(-self.halfDims[0], -self.halfDims[1],  self.halfDims[2]),
                 self.pos + self.orient @ v3(-self.halfDims[0], -self.halfDims[1], -self.halfDims[2]),
                 self.pos + self.orient @ v3( self.halfDims[0],  self.halfDims[1], -self.halfDims[2]),
                 self.pos + self.orient @ v3( self.halfDims[0],  self.halfDims[1],  self.halfDims[2]),
                 self.pos + self.orient @ v3(-self.halfDims[0],  self.halfDims[1],  self.halfDims[2]),
                 self.pos + self.orient @ v3(-self.halfDims[0],  self.halfDims[1], -self.halfDims[2]) ]
    
    def createGeo(self):
        verts = self.calcVerts()
        
        self.tris.append( (Tri3D(self.window, verts[0], verts[1], verts[2], self.color),0,1,2) ) # bottom
        #self.tris.append( (Tri3D(self.window, verts[0], verts[2], verts[3], self.color),0,2,3) )
        
        self.lines.append( (Line(self.window, verts[0], verts[1], "black"),0,1) ) # bottom
        self.lines.append( (Line(self.window, verts[1], verts[2], "black"),1,2) )
        self.lines.append( (Line(self.window, verts[2], verts[3], "black"),2,3) )
        self.lines.append( (Line(self.window, verts[3], verts[0], "black"),3,0) )
        
        self.lines.append( (Line(self.window, verts[4], verts[5], "black"),4,5) ) # top
        self.lines.append( (Line(self.window, verts[5], verts[6], "black"),5,6) )
        self.lines.append( (Line(self.window, verts[6], verts[7], "black"),6,7) )
        self.lines.append( (Line(self.window, verts[7], verts[4], "black"),7,4) )

        self.lines.append( (Line(self.window, verts[0], verts[4], "black"),0,4) ) # vert sides
        self.lines.append( (Line(self.window, verts[1], verts[5], "black"),1,5) )
        self.lines.append( (Line(self.window, verts[2], verts[6], "black"),2,6) )
        self.lines.append( (Line(self.window, verts[3], verts[7], "black"),3,7) )
        
    def updateGeo(self):
        # called when one of the transforms changed (like the camera) or pos change...update 3d -> 2d (pass on to tris & lines)
        verts = self.calcVerts()
        modelToWorld = self.modelToWorld()
        for tri in self.tris:
            tri[0].updateTriPositions( modelToWorld @ v4(verts[tri[1]]), modelToWorld @ v4(verts[tri[2]]), modelToWorld @ v4(verts[tri[3]]) )
        for line in self.lines:
            line[0].updateLinePositions( *self.window.transformAndClipLine(verts[line[1]], verts[line[2]], modelToWorld) )
    
    def update(self, deltaTime):
        super().update(deltaTime)
