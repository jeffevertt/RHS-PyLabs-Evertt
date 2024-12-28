from lib.winobj import WinObj
from lib.utils import *

class Rectangle(WinObj):
    def __init__(self, window, pos, width, height, vel = v3(0,0,0), color = "green", updateFn = None):
        super().__init__(window, pos, vel)
        self.width = width
        self.height = height
        self.color = color
        self.window.sim.onCreated(self)
        self.updateFn = updateFn
        self.createGfx()
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def createGfx(self):
        self.gfxRectangle = self.window.canvas.create_rectangle(0, 0, 1, 1, fill = self.color, outline = "black", width = 3)
        self.updateGfx()
    def destroyGfx(self):
        if self.gfxRectangle != None:
            self.window.canvas.delete(self.gfxRectangle)
            self.gfxRectangle = None
    def updateGfx(self):
        if self.gfxRectangle != None:
            self.window.canvas.coords(self.gfxRectangle, self.window.toPixelsX(self.pos[0] - self.width / 2), self.window.toPixelsY(self.pos[1] - self.height / 2), 
                                                         self.window.toPixelsX(self.pos[0] + self.width / 2), self.window.toPixelsY(self.pos[1] + self.height / 2))
    def overrideColor(self, color):
        if not color is None:
            self.window.canvas.itemconfig(self.gfxRectangle, fill = color)
        else:
            self.window.canvas.itemconfig(self.gfxRectangle, fill = self.color)
            
    def update(self, deltaTime):
        if self.updateFn != None:
            self.updateFn(self, deltaTime)
            self.updateGfx()
        super().update(deltaTime)
