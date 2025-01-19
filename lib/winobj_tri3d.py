from lib.winobj import WinObj
from lib.utils import *
from lib.utils_clipping import *

class Tri3D(WinObj):
    def __init__(self, window, posA, posB, posC, color = "blue"): #todo: add cull(true/false: true CCW)
        self.posA = posA
        self.posB = posB
        self.posC = posC
        centroid = (posA + posB + posC) / 3
        super().__init__(window, centroid)
        self.color = color
        self.window.sim.onCreated(self)
        self.createGfx()
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def shouldBeCulled(self):
        # don't do auto-culling of tris
        return False
        
    def createGfx(self):
        self.gfxTri = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0) ], fill = self.color, outline = 'black')
        self.updateGfx()
    def destroyGfx(self):
        if self.gfxTri != None:
            self.window.canvas.delete(self.gfxTri)
            self.gfxTri = None
    def updateGfx(self):
        poly = None
        
        # transform and clip (from 3D world space to clip space, clip, then to NDC)
        toClipSpace = self.window.transProj @ self.window.transCamera
        posA = toClipSpace @ v4(self.posA)
        posB = toClipSpace @ v4(self.posB)
        posC = toClipSpace @ v4(self.posC)
        
        # first, cull all non CCW (do this in clip space)
        if isTriWindingCCW(posA, posB, posC) or True:
            # clip tri to a poly (this may add verts)
            poly = clipTri(posA, posB, posC)

            # to NDC (perspective divide)
            if poly is not None:
                for vert in poly:
                    vert /= (vert[3] if vert[3] != 0 else 0.0000001)
        
        # update the tris
        if self.gfxTri != None:
            if poly is None:
                self.window.canvas.itemconfigure(self.gfxTri, state = "hidden")
            else:
                self.window.canvas.itemconfigure(self.gfxTri, state = "normal")
                poly2d = []
                for vert in poly: # from NDC to pixel space (with inverted y)
                    poly2d.append( (self.window.toPixelsX(vert[0] * self.window.maxCoordinateX()), self.window.toPixelsY(vert[1] * -self.window.maxCoordinateY())) )
                self.window.canvas.coords(self.gfxTri, poly2d)
        
    def updateTriPositions(self, posA, posB, posC):
        self.posA = posA
        self.posB = posB
        self.posC = posC
        self.updateGfx()
    
    def update(self, deltaTime):
        super().update(deltaTime)
