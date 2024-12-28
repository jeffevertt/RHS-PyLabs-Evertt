from lib.winobj import WinObj
from lib.utils import *

class Ammo(WinObj):
    RADIUS = 0.15
    SPEED = 8
    
    def __init__(self, window, playerIdx, pos, dir, maxRange, radius = RADIUS, speed = SPEED):
        super().__init__(window, pos, unit(dir) * speed)
        
        self.playerIdx = playerIdx
        self.startPos = pos
        self.maxRange = maxRange
        self.radiusMax = radius
        self.radius = self.radiusMax
        self.timeTillDeath = 0
  
        self.window.sim.onCreated(self)
        self.createGfx()
        
    def shouldBeCulled(self):
        return super().shouldBeCulled() or self.timeTillDeath >= 1
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def createGfx(self):
        self.gfxCircle = self.window.canvas.create_oval(self.window.toPixelsX(self.pos[0] - self.radius), self.window.toPixelsY(self.pos[1] - self.radius), 
                                                        self.window.toPixelsX(self.pos[0] + self.radius), self.window.toPixelsY(self.pos[1] + self.radius), 
                                                        fill = 'darkred', outline = "black", width = 2)
    def destroyGfx(self):
        if self.gfxCircle != None:
            self.window.canvas.delete(self.gfxCircle)
            self.gfxCircle = None
    def updateGfx(self):
        if self.gfxCircle != None:
            self.window.canvas.coords(self.gfxCircle, self.window.toPixelsX(self.pos[0] - self.radius), self.window.toPixelsY(self.pos[1] - self.radius), 
                                                      self.window.toPixelsX(self.pos[0] + self.radius), self.window.toPixelsY(self.pos[1] + self.radius))
    
    def update(self, deltaTime):
        # if dieing, continue
        if self.timeTillDeath > 0:
            # update it
            self.timeTillDeath = min(self.timeTillDeath + deltaTime * 10.0, 1.0)
            
            # scale it down
            self.radius = self.radiusMax * max(1.0 - self.timeTillDeath, 0.001)
        else:
            # update position
            self.pos = self.pos + self.vel * deltaTime

            # check max range...
            if lengthSqr(self.pos - self.startPos) >= (self.maxRange * self.maxRange):
                self.timeTillDeath = max(self.timeTillDeath, 0.0001)

        self.updateGfx()
        super().update(deltaTime)
