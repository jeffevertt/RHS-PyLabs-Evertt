from lib.winobj import WinObj
from lib.winobj_tank import Tank
from lib.winobj_ship import Ship
from lib.utils import *
from typing import Union

class PowerUp(WinObj):
    HALFDIMS = 0.4
    
    def __init__(self, window, pos, type = "P"):
        super().__init__(window, pos)
        
        self.type = type
        self.timeTillDeath = 0
        self.halfDims = self.HALFDIMS
  
        self.window.sim.onCreated(self)
        self.createGfx()
        
    def isDying(self):
        return self.timeTillDeath > 0

    def shouldBeCulled(self):
        return super().shouldBeCulled() or self.timeTillDeath >= 1
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def createGfx(self):
        self.gfxRect = self.window.canvas.create_rectangle(
            self.window.toPixelsX(self.pos[0] - self.halfDims), self.window.toPixelsY(self.pos[1] + self.halfDims), 
            self.window.toPixelsX(self.pos[0] + self.halfDims), self.window.toPixelsY(self.pos[1] - self.halfDims), 
            fill = 'yellow', outline = 'indigo', width = 3)
        self.gfxText = self.window.canvas.create_text(self.window.toPixelsX(self.pos[0]), self.window.toPixelsY(self.pos[1]), 
                                                          text = self.type, font=("Arial", 12), fill = "black")
        
    def destroyGfx(self):
        if self.gfxRect != None:
            self.window.canvas.delete(self.gfxRect)
            self.gfxRect = None
        if self.gfxText != None:
            self.window.canvas.delete(self.gfxText)
            self.gfxText = None
    def updateGfx(self):
        if self.gfxRect != None:
            self.window.canvas.coords(self.gfxRect, self.window.toPixelsX(self.pos[0] - self.halfDims), self.window.toPixelsY(self.pos[1] - self.halfDims), 
                                                    self.window.toPixelsX(self.pos[0] + self.halfDims), self.window.toPixelsY(self.pos[1] + self.halfDims))

    def typeAsInt(self):
        try:
            pointValue = int(self.type)
            return pointValue
        except:
            if self.type == "P":
                return 4
            elif self.type == "S":
                return 5
            elif self.type == "R":
                return 6
        return 0
    def pointsPowerupValue(self):
        try:
            pointValue = int(self.type)
            return pointValue
        except:
            return 0
    def onCollected(self, player: Union[Tank, Ship]):
        if self.isDying():
            return
        
        # figure out the player type
        playerIsTank = isinstance(player, Tank)
        playerIsShip = isinstance(player, Ship)

        # trigger death spiral...
        self.timeTillDeath = max(self.timeTillDeath, 0.0001)
        
        # give up the points...
        pointValueType = self.pointsPowerupValue()
        if pointValueType > 0:
            if playerIsShip:
                player.ammo += pointValueType
        elif self.type == "S":              # Speed
            if playerIsTank:
                player.tankMoveSpeed *= 1.15
                player.tankTurnSpeed *= 1.15
            elif playerIsShip:
                player.shipMoveSpeed *= 1.15
                player.shipTurnSpeed *= 1.15
            log("(powerup: speed +15%)")
        elif self.type == "R":              # Shot range
            player.ammoMaxRange *= 1.25
            log("(powerup: range +25%)")
        elif self.type == "P":              # Points
            self.window.awardPoints(25, player.playerIdx)
            log("(powerup: score +25)")
        else:
            log("Invalid powerup type = " + self.type)

    def update(self, deltaTime):
        # if dieing, continue...
        if self.isDying():
            # update it...
            self.timeTillDeath = min(self.timeTillDeath + deltaTime * 2.0, 1.0)
            
            # scale it down...
            self.halfDims = self.halfDims * max(1.0 - self.timeTillDeath, 0.001)
            self.updateGfx()
        else:
            # check for tanks collecting us...
            tanks = self.window.sim.objectsOfType(Tank)
            for tank in tanks:
                if intersectCirclePt(self.pos, self.HALFDIMS * 2, tank.pos):
                    # react to it & that's it for us
                    self.onCollected(tank)
                    self.timeTillDeath = max(self.timeTillDeath, 0.0001)
            # check for ships collecting us...
            ships = self.window.sim.objectsOfType(Ship)
            for ship in ships:
                if intersectCirclePt(self.pos, self.HALFDIMS * 2, ship.pos):
                    # react to it & that's it for us
                    self.onCollected(ship)
                    self.timeTillDeath = max(self.timeTillDeath, 0.0001)

        super().update(deltaTime)
