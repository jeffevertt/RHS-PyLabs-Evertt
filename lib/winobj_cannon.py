from lib.winobj import WinObj
from lib.winobj_ammo import Ammo
from lib.utils import *
import time

class Cannon(WinObj):
    TURN_SPEED          = 30    # degrees per second
    SHOT_SPEED          = 15    # units per second
    MIN_SHOT_PERIOD     = 0.5   # in seconds
    
    CANNON_RADIUS       = 1.0
    CANNON_LENGTH       = 2.5
    CANNON_WIDTH        = 0.5
            
    def __init__(self, window, playerIdx, pos):
        super().__init__(window, pos)
        
        self.playerIdx = playerIdx
        self.angle = 90.0
        self.timeLastShot = time.time()
        
        self.trgShotAngle = None
  
        self.window.sim.onCreated(self)
        self.createGfx()
        
    def shouldBeCulled(self):
        return False
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def createGfx(self):
        color = 'lightblue' if self.playerIdx > 0 else 'lightgreen'
        self.gfxBarrel = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0), (0, 0) ], fill = color, outline = 'black', width = 2)
        self.gfxCircle = self.window.canvas.create_oval(self.window.toPixelsX(self.pos[0] - Cannon.CANNON_RADIUS), self.window.toPixelsY(self.pos[1] - Cannon.CANNON_RADIUS), 
                                                        self.window.toPixelsX(self.pos[0] + Cannon.CANNON_RADIUS), self.window.toPixelsY(self.pos[1] + Cannon.CANNON_RADIUS), 
                                                        fill = 'darkgray', outline = "black", width = 2)
        self.updateGfx()
    def destroyGfx(self):
        if self.gfxBarrel != None:
            self.window.canvas.delete(self.gfxBarrel)
            self.gfxBarrel = None
        if self.gfxCircle != None:
            self.window.canvas.delete(self.gfxCircle)
            self.gfxCircle = None
    def updateGfx(self):
        if self.gfxBarrel != None:
            self.window.canvas.coords(self.gfxBarrel, calcRotatedRectanglePtsInPixels(self.pos, v2(Cannon.CANNON_LENGTH, Cannon.CANNON_WIDTH/2), v2_zero(), self.angle, self.window))
        if self.gfxCircle != None:
            self.window.canvas.coords(self.gfxCircle, self.window.toPixelsX(self.pos[0] - Cannon.CANNON_RADIUS), self.window.toPixelsY(self.pos[1] - Cannon.CANNON_RADIUS), 
                                                      self.window.toPixelsX(self.pos[0] + Cannon.CANNON_RADIUS), self.window.toPixelsY(self.pos[1] + Cannon.CANNON_RADIUS))
    
    def forward(self):
        return rotateVec2(v2_right(), self.angle)
    def right(self):
        return rotateVec2(v2_down(), self.angle)
    def ammoSpawnLocation(self):
        return self.toWorld(v2(Cannon.CANNON_LENGTH + Cannon.CANNON_WIDTH * 0.6, 0))
 
    def toWorld(self, pt):
        return self.pos + self.forward() * pt[0] + self.right() * pt[1]

    def shoot(self, dir):
        maxTurnAngle = 75
        angle = v2ToAngleDeg(dir) - 90
        self.trgShotAngle = clamp(90 + angle, 90 - maxTurnAngle, 90 + maxTurnAngle)
        self.window.awardPoints(-1, self.playerIdx)
    def isIdle(self):
        if self.trgShotAngle != None:
            return False
        return True

    def update(self, deltaTime):
        # possibly turn & shoot
        if (time.time() - self.timeLastShot) >= Cannon.MIN_SHOT_PERIOD:
            if self.trgShotAngle != None:
                if self.trgShotAngle > self.angle:
                    self.angle = min(self.angle + Cannon.TURN_SPEED * deltaTime, self.trgShotAngle)
                else:
                    self.angle = max(self.angle - Cannon.TURN_SPEED * deltaTime, self.trgShotAngle)
                if self.trgShotAngle == self.angle:
                    Ammo(self.window, self.playerIdx, self.ammoSpawnLocation(), self.forward(), 1000, radius = Cannon.CANNON_WIDTH * 0.6, speed = Cannon.SHOT_SPEED)
                    self.trgShotAngle = None
                    self.timeLastShot = time.time()
        
        self.updateGfx()
        super().update(deltaTime)