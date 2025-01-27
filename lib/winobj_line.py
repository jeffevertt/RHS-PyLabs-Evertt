from lib.winobj import WinObj
from lib.utils import *

class Line(WinObj):
    def __init__(self, window, posA, posB, color = "blue", width = 4):
        self.posA = posA
        self.posB = posB
        posCenter = (posA + posB) / 2
        super().__init__(window, posCenter)
        self.color = color
        self.width = width
        self.window.sim.onCreated(self)
        self.createGfx()
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def shouldBeCulled(self):
        # don't do auto-culling of lines
        return False
        
    def createGfx(self):
        self.gfxLine = self.window.canvas.create_line(self.window.toPixelsX(self.posA[0]), self.window.toPixelsY(self.posA[1]), 
                                                      self.window.toPixelsX(self.posB[0]), self.window.toPixelsY(self.posB[1]), 
                                                      fill = self.color, width = self.width)
    def destroyGfx(self):
        if self.gfxLine != None:
            self.window.canvas.delete(self.gfxLine)
            self.gfxLine = None
    def updateGfx(self):
        if self.gfxLine != None:
            if self.posA is None or self.posB is None:
                self.window.canvas.itemconfigure(self.gfxLine, state = "hidden")
            else:
                self.window.canvas.itemconfigure(self.gfxLine, state = "normal")
                self.window.canvas.coords(self.gfxLine, self.window.toPixelsX(self.posA[0]), self.window.toPixelsY(self.posA[1]), 
                                                        self.window.toPixelsX(self.posB[0]), self.window.toPixelsY(self.posB[1]))
    
    def updateLinePositions(self, posA, posB):
        self.posA = posA
        self.posB = posB
        self.updateGfx()
    
    def update(self, deltaTime):
        super().update(deltaTime)
