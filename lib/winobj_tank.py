from lib.winobj import WinObj
from lib.winobj_ammo import Ammo
from lib.utils import *
import time

class TankCmd:
    def __init__(self, dir):
        self.progress = 0
        self.dir = dir
    def typeAsInt(self):
        return -1
    def description(self):
        return "TankCmd"
class TankCmd_Move(TankCmd):
    def __init__(self, dir):
        super().__init__(dir)
    def typeAsInt(self):
        return 0
    def description(self):
        return "Move"
class TankCmd_Turn(TankCmd):
    def __init__(self, dir):
        super().__init__(unit(dir))
    def typeAsInt(self):
        return 1
    def description(self):
        return "Turn"
class TankCmd_Shoot(TankCmd):
    def __init__(self, dir):
        super().__init__(unit(dir))
    def typeAsInt(self):
        return 2
    def description(self):
        return "Shoot"

class Tank(WinObj):
    DEFAULT_AMMO_RANGE  = 5     # in world units
    DEFAULT_MOVE_SPEED  = 2.5   # units per second
    DEFAULT_TURN_SPEED  = 90    # degrees per second
    
    TANK_BODY_SIZE      = 0.75
    TANK_TREAD_WIDTH    = 0.13
    TANK_TREAD_LENGTH   = 0.85
    TANK_TURRET_INSET   = 0.15
    TANK_TURRET_LENGTH  = 0.7
    TANK_TURRET_WIDTH   = 0.15
            
    def __init__(self, window, playerIdx, pos, dir):
        super().__init__(window, pos)
        
        self.playerIdx = playerIdx
        self.dir = dir
        self.ammoMaxRange = Tank.DEFAULT_AMMO_RANGE
        self.timeLastShot = time.time()
        
        self.activeCommand = None
        self.queuedCommands = []
        
        self.tankMoveSpeed = Tank.DEFAULT_MOVE_SPEED
        self.tankTurnSpeed = Tank.DEFAULT_TURN_SPEED
        
        self.timeSinceLastCmd = 1000.0
  
        self.window.sim.onCreated(self)
        self.createGfx()
        
    def shouldBeCulled(self):
        return False
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def createGfx(self):
        isSecondTank = self.window.sim.countObjectsOfType(Tank) > 1
        self.bodyColor1 = 'lightblue' if isSecondTank else 'lightgreen'
        self.bodyColor2 = 'darkblue' if isSecondTank else 'darkgreen'
        self.gfxBody = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0), (0, 0) ], fill = self.bodyColor1, outline = 'black', width = 2)
        self.gfxTreadLeft = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0), (0, 0) ], fill = 'darkgray', outline = 'black', width = 2)
        self.gfxTreadRight = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0), (0, 0) ], fill = 'darkgray', outline = 'black', width = 2)
        self.gfxTurret = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0), (0, 0) ], fill = 'blue' if isSecondTank else 'green', outline = 'black', width = 2)
        self.updateGfx()
    def destroyGfx(self):
        if self.gfxBody != None:
            self.window.canvas.delete(self.gfxBody)
            self.gfxBody = None
        if self.gfxTreadLeft != None:
            self.window.canvas.delete(self.gfxTreadLeft)
            self.gfxTreadLeft = None
        if self.gfxTreadRight != None:
            self.window.canvas.delete(self.gfxTreadRight)
            self.gfxTreadRight = None
        if self.gfxTurret != None:
            self.window.canvas.delete(self.gfxTurret)
            self.gfxTurret = None
    def updateGfx(self):
        angle = angleDeg(self.dir)
        if self.gfxBody != None:
            colorInner = colorHexLerp( colorNamedToHex(self.bodyColor2), colorNamedToHex(self.bodyColor1), min(0.5 + self.timeSinceLastCmd * 1, 1) )
            self.window.canvas.itemconfig(self.gfxBody, fill = colorInner)
            self.window.canvas.coords(self.gfxBody, calcRotatedRectanglePtsInPixels(self.pos, v2(Tank.TANK_BODY_SIZE/2, Tank.TANK_BODY_SIZE/2), v2_zero(), angle, self.window))
            self.window.canvas.tag_raise(self.gfxBody)
        if self.gfxTreadLeft != None:
            self.window.canvas.coords(self.gfxTreadLeft, calcRotatedRectanglePtsInPixels(self.pos, v2(Tank.TANK_TREAD_LENGTH/2, Tank.TANK_TREAD_WIDTH/2), v2(0, Tank.TANK_BODY_SIZE/2), angle, self.window))
            self.window.canvas.tag_raise(self.gfxTreadLeft)
        if self.gfxTreadRight != None:
            self.window.canvas.coords(self.gfxTreadRight, calcRotatedRectanglePtsInPixels(self.pos, v2(Tank.TANK_TREAD_LENGTH/2, Tank.TANK_TREAD_WIDTH/2), v2(0, -Tank.TANK_BODY_SIZE/2), angle, self.window))
            self.window.canvas.tag_raise(self.gfxTreadRight)
        if self.gfxTurret != None:
            self.window.canvas.coords(self.gfxTurret, calcRotatedRectanglePtsInPixels(self.pos, v2(Tank.TANK_TURRET_LENGTH/2, Tank.TANK_TURRET_WIDTH/2), v2(Tank.TANK_TURRET_INSET, 0), angle, self.window))
            self.window.canvas.tag_raise(self.gfxTurret)
    
    def forward(self):
        return self.dir
    def right(self):
        return v2(self.dir[1], -self.dir[0])
    def ammoSpawnLocation(self):
        return self.toWorld(v2(Tank.TANK_TURRET_LENGTH - Tank.TANK_TURRET_INSET + 0.1, 0))
    def getOther(self):
        return self.window.getOtherTank(self)
    
    def setPlayerName(self, playerName):
        self.window.setPlayerName(playerName, self.playerIdx)
 
    def kickBackTank(self, dir):
        # If we are in the middle of a move, stop it...
        if self.activeCommand != None and isinstance(self.activeCommand, TankCmd_Move):
            self.finishActiveCommand()
        
        # Do the kick back...
        kickBackLoc = clampToClosestHalfUnit(self.pos + unit(dir) * 1.414)
        if isInsideField(self.window, kickBackLoc, 0.25):
            self.pos = kickBackLoc
            self.updateGfx()
        else:
            kickBackLoc = self.pos + unit(dir) * (1.414 / 2)
            if isInsideField(self.window, kickBackLoc, 0.25):
                self.pos = kickBackLoc
                self.updateGfx()
        
        # Check for tank overlap...
        otherTank = self.window.getOtherTank(self)
        if otherTank != None and intersectCircles(self.pos, Tank.TANK_BODY_SIZE/2, otherTank.pos, Tank.TANK_BODY_SIZE/2):
            self.pos += dir * 0.1
            otherTank.pos += dir * -0.1

    def toWorld(self, pt):
        return self.pos + self.forward() * pt[0] + self.dir * pt[1]
    
    def calcMoveVel(self):
        if self.activeCommand != None and isinstance(self.activeCommand, TankCmd_Move):
            return unit(self.activeCommand.dir) * self.tankMoveSpeed
        return v2_zero()

    def calcAngVel(self):
        if self.activeCommand != None and isinstance(self.activeCommand, TankCmd_Turn):
            trgAngle = angleDeg(self.activeCommand.dir)
            angleDelta = minAngleToAngleDelta(angleDeg(self.activeCommand.startDir), trgAngle)
            return self.tankTurnSpeed * (-1 if (angleDelta < 0) else 1)
        return 0

    def queueCommand(self, command, insertFront = False):
        if insertFront:
            self.queuedCommands.insert(0, command)
        else:
            self.queuedCommands.append(command)
        self.timeSinceLastCmd = 0

    def finishActiveCommand(self):
        # done with this one
        self.activeCommand = None
        
        # if no more, then exit out...
        if len(self.queuedCommands) == 0:
            return
        
        # if it's a move or shoot, might need to do a turn first...
        needToTurnFirst = False
        nextCommand = self.queuedCommands[0]
        if isinstance(nextCommand, TankCmd_Move) or isinstance(nextCommand, TankCmd_Shoot):
            if dot(unit(self.dir), unit(nextCommand.dir)) < 0.999:
                nextCommand = TankCmd_Turn(nextCommand.dir)
                needToTurnFirst = True
        
        # grab the next queued command
        self.activeCommand = nextCommand
        if not needToTurnFirst:
            self.queuedCommands.pop(0)
        
        # log it
        log(("    " if needToTurnFirst else "--> ") + self.activeCommand.description() + ": dir=" + f"({self.activeCommand.dir[0]:.2f}, {self.activeCommand.dir[1]:.2f})")
        
        # setup next new command (save off starting information)...
        self.activeCommand.startPos = self.pos
        self.activeCommand.startDir = self.dir
        
        # Make it cost something...
        pointCost = -2 if isinstance(self.activeCommand, TankCmd_Shoot) else -1
        self.window.awardPoints(pointCost, self.playerIdx)

    def updateCommand(self, deltaTime):
        if self.activeCommand == None:
            # check for queued
            if len(self.queuedCommands) > 0:
                self.finishActiveCommand()
            if self.activeCommand == None:
                return
        if isinstance(self.activeCommand, TankCmd_Move):
            moveVec = self.activeCommand.dir
            moveDst = length(moveVec)
            moveTravelTime = moveDst / self.tankMoveSpeed
            
            # check for invalid move
            skipThisCmd = False
            if abs(moveVec[0]) > 0.000001 and abs(moveVec[1]) > 0.000001:
                log("INVALID MOVE: Tanks move only horizontally & vertically")
                raise Exception('INVALID MOVE: Tanks move only horizontally & vertically')
                return
            if lengthSqr(moveVec) < 0.001:
                log("INVALID MOVE: Zero distance")
                skipThisCmd = True
            
            # update the active command
            if not skipThisCmd:
                self.activeCommand.progress = min(self.activeCommand.progress + deltaTime / moveTravelTime, 1)
                self.pos = self.activeCommand.startPos + moveVec * self.activeCommand.progress
                
                # check for tank overlap
                otherTank = self.window.getOtherTank(self)
                if otherTank != None and intersectCircles(self.pos, Tank.TANK_BODY_SIZE/2, otherTank.pos, Tank.TANK_BODY_SIZE/2):
                    deltaVec = unit(self.pos - otherTank.pos)
                    self.pos += deltaVec * 0.1
                    self.activeCommand.progress = 1

                # keep in bounds
                if self.pos[0] <= Tank.TANK_BODY_SIZE/2:
                    self.pos += v2_right() * 0.1
                    self.activeCommand.progress = 1
                if self.pos[1] <= Tank.TANK_BODY_SIZE/2:
                    self.pos += v2_up() * 0.1
                    self.activeCommand.progress = 1
                if self.pos[0] >= self.window.maxCoordinateX() - Tank.TANK_BODY_SIZE/2:
                    self.pos += v2_left() * 0.3
                    self.activeCommand.progress = 1
                if self.pos[1] >= self.window.maxCoordinateY() - Tank.TANK_BODY_SIZE/2:
                    self.pos += v2_down() * 0.3
                    self.activeCommand.progress = 1
            
            # and check for done
            if self.activeCommand.progress == 1 or skipThisCmd:
                self.finishActiveCommand()
        elif isinstance(self.activeCommand, TankCmd_Turn):
            trgAngle = angleDeg(self.activeCommand.dir)
            angleDelta = minAngleToAngleDelta(angleDeg(self.activeCommand.startDir), trgAngle)
            moveTravelTime = abs(angleDelta) / self.tankTurnSpeed
            
            # update the active command
            self.activeCommand.progress = min(self.activeCommand.progress + deltaTime / moveTravelTime, 1)
            self.dir = unit(rotateVec2(self.activeCommand.startDir, angleDelta * self.activeCommand.progress))
            
            # and...check for done...
            if (self.activeCommand.progress == 1):
                self.finishActiveCommand()
        elif isinstance(self.activeCommand, TankCmd_Shoot):
            # enforce a max shot period
            timeSinceShot = (time.time() - self.timeLastShot)
            if (timeSinceShot > 1):
                # check for invalid shot
                skipThisCmd = False
                if lengthSqr(self.activeCommand.dir) < 0.001:
                    log("INVALID SHOT: Zero direction vector")
                    skipThisCmd = True
                    
                # shoot, save off the time, and then we're done with the cmd
                if not skipThisCmd:
                    Ammo(self.window, self.playerIdx, self.ammoSpawnLocation(), self.dir, self.ammoMaxRange)
                    self.timeLastShot = time.time()
                self.finishActiveCommand()
        self.timeSinceLastCmd += deltaTime

    def hasCommand(self):
        return self.activeCommand != None or len(self.queuedCommands) > 0
 
    def update(self, deltaTime):
        # command
        if deltaTime != 0:
            self.updateCommand(deltaTime)
        
        self.updateGfx()
        super().update(deltaTime)