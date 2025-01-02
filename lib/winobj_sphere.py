from lib.winobj import WinObj
from lib.utils import *

class Sphere(WinObj):
    def __init__(self, window, pos, radius, vel = v3(0,0,0), color = "blue", updateFn = None):
        super().__init__(window, pos, vel)
        self.radius = radius
        self.color = color
        self.window.sim.onCreated(self)
        self.updateFn = updateFn
        self.createGfx()
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def shouldBeCulled(self):   # in 3d, 2d culling from base class doesn't work here
        return False
        
    def createGfx(self):
        self.gfxCircle = self.window.canvas.create_oval(0, 0, 1, 1, fill = self.color, outline = "black", width = 1)
        self.updateGfx()
    def destroyGfx(self):
        if self.gfxCircle != None:
            self.window.canvas.delete(self.gfxCircle)
            self.gfxCircle = None
    def updateGfx(self):
        if self.gfxCircle != None:
            pos2d = self.window.worldTo2D(self.pos, clip = True)
            if pos2d is None:
                self.window.canvas.itemconfigure(self.gfxCircle, state = "hidden")
            else:
                self.window.canvas.itemconfigure(self.gfxCircle, state = "normal")
                radiusAtPos = self.window.scaleAtPos(self.pos)
                self.window.canvas.coords(self.gfxCircle, self.window.toPixelsX(pos2d[0] - radiusAtPos), self.window.toPixelsY(pos2d[1] - radiusAtPos), 
                                                        self.window.toPixelsX(pos2d[0] + radiusAtPos), self.window.toPixelsY(pos2d[1] + radiusAtPos))
    def overrideColor(self, color):
        if not color is None:
            self.window.canvas.itemconfig(self.gfxCircle, fill = color)
        else:
            self.window.canvas.itemconfig(self.gfxCircle, fill = self.color)
            
    def update(self, deltaTime):
        if self.updateFn != None:
            self.updateFn(self, deltaTime, boxPlanes = self.window.worldBoxPlanes)
            self.updateGfx()
        super().update(deltaTime)
