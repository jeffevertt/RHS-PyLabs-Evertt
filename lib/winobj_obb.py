from lib.winobj import WinObj
from lib.utils import *

class OBB(WinObj):
    def __init__(self, window, pos, width, height, angle = 0, vel = v3(0,0,0), color = "green", updateFn = None):
        super().__init__(window, pos, vel)
        self.width = width
        self.height = height
        self.angle = angle
        self.color = color
        self.window.sim.onCreated(self)
        self.updateFn = updateFn
        self.createGfx()
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def right(self):
        return rotateVec2(v2_right(), self.angle)
    def up(self):
        return rotateVec2(v2_up(), self.angle)
        
    def createGfx(self):
        self.gfxOBB = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0), (0, 0) ], fill = self.color, outline = 'black', width = 3)
        self.updateGfx()
    def destroyGfx(self):
        if self.gfxOBB != None:
            self.window.canvas.delete(self.gfxOBB)
            self.gfxOBB = None
    def updateGfx(self):
        if self.gfxOBB != None:
            self.window.canvas.coords(self.gfxOBB, calcRotatedRectanglePtsInPixels(self.pos, v2(self.width/2, self.height/2), v2_zero(), self.angle, self.window))
    def overrideColor(self, color):
        if not color is None:
            self.window.canvas.itemconfig(self.gfxOBB, fill = color)
        else:
            self.window.canvas.itemconfig(self.gfxOBB, fill = self.color)
            
    def update(self, deltaTime):
        if self.updateFn != None:
            self.updateFn(self, deltaTime)
            self.updateGfx()
        super().update(deltaTime)
