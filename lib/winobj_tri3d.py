from lib.winobj import WinObj
from lib.utils import *

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
        self.gfxTriA = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0) ], fill = self.color, outline = '')
        self.gfxTriB = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0) ], fill = self.color, outline = '')
        self.updateGfx()
    def destroyGfx(self):
        if self.gfxTriA != None:
            self.window.canvas.delete(self.gfxTriA)
            self.gfxTriA = None
        if self.gfxTriB != None:
            self.window.canvas.delete(self.gfxTriB)
            self.gfxTriB = None
    def updateGfx(self):
        # transform and clip
        toScreenSpace = self.window.transProj @ self.window.transCamera
        posA = toScreenSpace @ v4(self.posA)
        posA /= posA[3]
        posB = toScreenSpace @ v4(self.posB)
        posB /= posB[3]
        posC = toScreenSpace @ v4(self.posC)
        posC /= posC[3]
        triA, triB = clipTriAgainstNearPlaneNDC(posA, posB, posC)
        # update the tris (going from NDC to pixels, by way of the 2d coordinate space...and need to invert after above transform)
        if self.gfxTriA != None:
            if triA is None:
                self.window.canvas.itemconfigure(self.gfxTriA, state = "hidden")
            else:
                self.window.canvas.itemconfigure(self.gfxTriA, state = "normal") # note: inverted y (pixel space is inverted)
                self.window.canvas.coords(self.gfxTriA, [ ( self.window.toPixelsX(triA[0][0] * self.window.maxCoordinateX()), self.window.toPixelsY(triA[0][1] * -self.window.maxCoordinateY()) ),
                                                          ( self.window.toPixelsX(triA[1][0] * self.window.maxCoordinateX()), self.window.toPixelsY(triA[1][1] * -self.window.maxCoordinateY()) ), 
                                                          ( self.window.toPixelsX(triA[2][0] * self.window.maxCoordinateX()), self.window.toPixelsY(triA[2][1] * -self.window.maxCoordinateY()) ) ])
        if self.gfxTriB != None:
            if triB is None:
                self.window.canvas.itemconfigure(self.gfxTriB, state = "hidden")
            else:
                self.window.canvas.itemconfigure(self.gfxTriB, state = "normal")
                self.window.canvas.coords(self.gfxTriB, [ ( self.window.toPixelsX(triB[0][0] * self.window.maxCoordinateX()), self.window.toPixelsY(triB[0][1] * -self.window.maxCoordinateY()) ), 
                                                          ( self.window.toPixelsX(triB[1][0] * self.window.maxCoordinateX()), self.window.toPixelsY(triB[1][1] * -self.window.maxCoordinateY()) ), 
                                                          ( self.window.toPixelsX(triB[2][0] * self.window.maxCoordinateX()), self.window.toPixelsY(triB[2][1] * -self.window.maxCoordinateY()) ) ])
        
    def updateTriPositions(self, posA, posB, posC):
        self.posA = posA
        self.posB = posB
        self.posC = posC
        self.updateGfx()
    
    def update(self, deltaTime):
        super().update(deltaTime)
