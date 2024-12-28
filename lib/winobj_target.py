from lib.winobj import WinObj
from lib.utils import *

class Target(WinObj):
    RADIUS = 0.4
    
    def __init__(self, window, pos, vel = v2_zero()):
        super().__init__(window, pos, vel)
        
        self.startPos = pos
        self.radius = self.RADIUS
        self.timeTillDeath = 0
        self.gfxCircles = [None, None, None]
        self.gfxBody = None
  
        self.window.sim.onCreated(self)
        self.createGfx()
        
    def shouldBeCulled(self):
        return super().shouldBeCulled() or self.isOutOfBounds(1) or self.timeTillDeath >= 1
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def createGfx(self):
        if self.isMovingTarget():
            self.gfxBody = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0) ], fill = 'pink', outline = 'black', width = 2)
        for i in range(len(self.gfxCircles)):
            radius = self.radius * (1 - i * 0.33)
            color = "red" if i % 2 == 0 else "white"
            self.gfxCircles[i] = self.window.canvas.create_oval(self.window.toPixelsX(self.pos[0] - radius), self.window.toPixelsY(self.pos[1] - radius),
                                                                self.window.toPixelsX(self.pos[0] + radius), self.window.toPixelsY(self.pos[1] + radius), 
                                                                fill = color, outline = "black", width = 2)
    def destroyGfx(self):
        if self.gfxBody is not None:
            self.window.canvas.delete(self.gfxBody)
            self.gfxBody = None
        for i in range(len(self.gfxCircles)):
            if self.gfxCircles[i] != None:
                self.window.canvas.delete(self.gfxCircles[i])
                self.gfxCircles[i] = None
    def updateGfx(self):
        radiusBase = self.radius if not self.isMovingTarget() else self.radius*2/3
        if self.isMovingTarget():
            if self.gfxBody != None:
                self.window.canvas.coords(self.gfxBody, calcRotatedTrianglePtsInPixels(self.pos, -0.3, 0.6, -0.4, 0.4, angleDeg(self.vel), self.window))
                self.window.canvas.tag_raise(self.gfxBody)
        for i in range(len(self.gfxCircles)):
            radius = radiusBase * (1 - i * 0.33)
            if self.gfxCircles[i] != None:
                self.window.canvas.coords(self.gfxCircles[i], self.window.toPixelsX(self.pos[0] - radius), self.window.toPixelsY(self.pos[1] - radius), 
                                                              self.window.toPixelsX(self.pos[0] + radius), self.window.toPixelsY(self.pos[1] + radius))
                self.window.canvas.tag_raise(self.gfxCircles[i])
        
    def isDying(self):
        return self.timeTillDeath > 0
    
    def isMovingTarget(self):
        return True if self.vel[0] != 0 or self.vel[1] != 0 else False
        
    def onHitByAmmo(self, playerIdx):
        if self.isDying():
            return
        
        # trigger death spiral...
        self.timeTillDeath = max(self.timeTillDeath, 0.0001)
        
        # give up the points...
        self.window.awardPoints(20, playerIdx)
        log("(hit target: score +20)")
    
    def update(self, deltaTime):
        # if dieing, continue
        if self.timeTillDeath > 0:
            # update it
            self.timeTillDeath = min(self.timeTillDeath + deltaTime * 2.0, 1.0)
            
            # scale it down
            self.radius = self.radius * max(1.0 - self.timeTillDeath, 0.001)
            self.updateGfx()
        # moving target support
        elif self.isMovingTarget():
            self.pos += self.vel * deltaTime
            self.updateGfx()
        
        super().update(deltaTime)
