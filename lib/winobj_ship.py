from lib.winobj import WinObj
from lib.winobj_ammo import Ammo
from lib.utils import *
import time

class ShipCmd:
    def __init__(self):
        self.progress = 0
    def description(self):
        return "ShipCmd"
class ShipCmd_Thrust(ShipCmd):
    def __init__(self, dst):
        super().__init__()
        self.dst = dst
    def description(self):
        return f"Thrust ({self.dst:.2f})"
class ShipCmd_ThrustLeft(ShipCmd):
    def __init__(self, angle):
        super().__init__()
        self.angle = abs(angle)
    def description(self):
        return f"ThrustLeft ({self.angle:.2f}°)"
class ShipCmd_ThrustRight(ShipCmd):
    def __init__(self, angle):
        super().__init__()
        self.angle = abs(angle)
    def description(self):
        return f"ThrustRight ({self.angle:.2f}°)"
class ShipCmd_Shoot(ShipCmd):
    def __init__(self, dir):
        super().__init__()
        self.dir = unit(dir)
    def description(self):
        return f"Shoot ({self.dir[0]:.2f}, {self.dir[1]:.2f})"

class Ship(WinObj):
    DEFAULT_AMMO_RANGE  = 10    # in world units
    DEFAULT_MOVE_SPEED  = 6     # units per second
    DEFAULT_TURN_SPEED  = 180   # degrees per second
    
    SHIP_SHELL_RADIUS   = 0.5
    SHIP_BODY_SIZE_XN   = -0.3
    SHIP_BODY_SIZE_XP   = 0.55
    SHIP_BODY_SIZE_Y    = 0.5
    SHIP_BODY_INNER_SCL = 0.5
    SHIP_THRUST_WIDTH   = 0.15
    SHIP_THRUST_LENGTH  = 0.3
    SHIP_THRUST_OFF_X   = -0.36
    SHIP_THRUST_OFF_Y   = 0.26
    SHIP_THRUST_CLR_ON  = 'yellow'
    SHIP_THRUST_CLR_OFF = 'darkslateblue'
            
    def __init__(self, window, playerIdx, pos, dir):
        super().__init__(window, pos)
        
        self.playerIdx = playerIdx
        self.dir = dir
        self.ammo = 0
        self.ammoMaxRange = Ship.DEFAULT_AMMO_RANGE
        self.timeLastShot = time.time()
        
        self.activeCommand = None
        self.queuedCommands = []
        
        self.shipMoveSpeed = Ship.DEFAULT_MOVE_SPEED
        self.shipTurnSpeed = Ship.DEFAULT_TURN_SPEED
        
        self.timeSinceLastCmd = 1000.0
  
        self.window.sim.onCreated(self)
        self.createGfx()
        
    def shouldBeCulled(self):
        return False
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def createGfx(self):
        isSecondShip = self.window.sim.countObjectsOfType(Ship) > 1
        self.gfxShell = self.window.canvas.create_oval(self.window.toPixelsX(self.pos[0] - Ship.SHIP_SHELL_RADIUS), self.window.toPixelsY(self.pos[1] - Ship.SHIP_SHELL_RADIUS),
                                                       self.window.toPixelsX(self.pos[0] + Ship.SHIP_SHELL_RADIUS), self.window.toPixelsY(self.pos[1] + Ship.SHIP_SHELL_RADIUS),
                                                       outline = 'darkblue' if isSecondShip else 'darkgreen', fill = None, width = 5)
        self.gfxBody = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0) ], fill = 'lightblue' if isSecondShip else 'lightgreen', outline = 'black', width = 2)
        self.gfxBodyInner = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0) ], fill = 'orange', outline = 'black', width = 2)
        self.gfxThrustLeft = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0), (0, 0) ], fill = Ship.SHIP_THRUST_CLR_OFF, outline = "black", width = 2)
        self.gfxThrustRight = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0), (0, 0) ], fill = Ship.SHIP_THRUST_CLR_OFF, outline = "black", width = 2)
        self.updateGfx()
    def destroyGfx(self):
        if self.gfxShell != None:
            self.window.canvas.delete(self.gfxShell)
            self.gfxShell = None
        if self.gfxBody != None:
            self.window.canvas.delete(self.gfxBody)
            self.gfxBody = None
        if self.gfxBodyInner != None:
            self.window.canvas.delete(self.gfxBodyInner)
            self.gfxBodyInner = None
        if self.gfxThrustLeft != None:
            self.window.canvas.delete(self.gfxThrustLeft)
            self.gfxThrustLeft = None
        if self.gfxThrustRight != None:
            self.window.canvas.delete(self.gfxThrustRight)
            self.gfxThrustRight = None
    def updateGfx(self):
        angle = angleDeg(self.dir)
        if self.gfxShell != None:
            self.window.canvas.coords(self.gfxShell, self.window.toPixelsX(self.pos[0] - Ship.SHIP_SHELL_RADIUS), self.window.toPixelsY(self.pos[1] - Ship.SHIP_SHELL_RADIUS), 
                                      self.window.toPixelsX(self.pos[0] + Ship.SHIP_SHELL_RADIUS), self.window.toPixelsY(self.pos[1] + Ship.SHIP_SHELL_RADIUS))
            self.window.canvas.tag_raise(self.gfxShell)
        if self.gfxBody != None:
            self.window.canvas.coords(self.gfxBody, calcRotatedTrianglePtsInPixels(self.pos, Ship.SHIP_BODY_SIZE_XN, Ship.SHIP_BODY_SIZE_XP, -Ship.SHIP_BODY_SIZE_Y, Ship.SHIP_BODY_SIZE_Y, angle, self.window))
            self.window.canvas.tag_raise(self.gfxBody)
        if self.gfxBodyInner != None:
            colorInner = colorHexLerp( colorNamedToHex('red'), colorNamedToHex('darkgray'), min(self.timeSinceLastCmd * 2, 1) )
            self.window.canvas.itemconfig(self.gfxBodyInner, fill = colorInner)
            self.window.canvas.coords(self.gfxBodyInner, calcRotatedTrianglePtsInPixels(self.pos, Ship.SHIP_BODY_SIZE_XN * Ship.SHIP_BODY_INNER_SCL, Ship.SHIP_BODY_SIZE_XP * Ship.SHIP_BODY_INNER_SCL, -Ship.SHIP_BODY_SIZE_Y * Ship.SHIP_BODY_INNER_SCL, Ship.SHIP_BODY_SIZE_Y * Ship.SHIP_BODY_INNER_SCL, angle, self.window))
            self.window.canvas.tag_raise(self.gfxBodyInner)
        if self.gfxThrustLeft != None:
            self.window.canvas.coords(self.gfxThrustLeft, calcRotatedRectanglePtsInPixels(self.pos, v2(Ship.SHIP_THRUST_WIDTH/2, Ship.SHIP_THRUST_LENGTH/2), v2(Ship.SHIP_THRUST_OFF_X, -Ship.SHIP_THRUST_OFF_Y), angle, self.window))
            self.window.canvas.tag_raise(self.gfxThrustLeft)
        if self.gfxThrustRight != None:
            self.window.canvas.coords(self.gfxThrustRight, calcRotatedRectanglePtsInPixels(self.pos, v2(Ship.SHIP_THRUST_WIDTH/2, Ship.SHIP_THRUST_LENGTH/2), v2(Ship.SHIP_THRUST_OFF_X, Ship.SHIP_THRUST_OFF_Y), angle, self.window))
            self.window.canvas.tag_raise(self.gfxThrustRight)
    def updateThrusterGfx(self, leftOn, rightOn):
        if self.gfxThrustLeft != None:
            self.window.canvas.itemconfig(self.gfxThrustLeft, fill = Ship.SHIP_THRUST_CLR_ON if leftOn else Ship.SHIP_THRUST_CLR_OFF)
        if self.gfxThrustRight != None:
            self.window.canvas.itemconfig(self.gfxThrustRight, fill = Ship.SHIP_THRUST_CLR_ON if rightOn else Ship.SHIP_THRUST_CLR_OFF)
    
    def forward(self):
        return self.dir
    def right(self):
        return v2(self.dir[1], -self.dir[0])
    def ammoSpawnLocation(self):
        return self.toWorld(v2(Ship.SHIP_SHELL_RADIUS, 0))
    
    def setPlayerName(self, playerName):
        self.window.setPlayerName(playerName, self.playerIdx)
 
    def kickBackShip(self, dir):
        # If we are in the middle of a move, stop it...
        if self.activeCommand != None and isinstance(self.activeCommand, ShipCmd_Thrust):
            self.finishActiveCommand()
        
        # Do the kick back...
        kickBackLoc = clampToClosestHalfUnit(self.pos + unit(dir) * 1.414)
        if isInsideField(kickBackLoc, 0.25):
            self.pos = kickBackLoc
            self.updateGfx()
        else:
            kickBackLoc = self.pos + unit(dir) * (1.414 / 2)
            if isInsideField(kickBackLoc, 0.25):
                self.pos = kickBackLoc
                self.updateGfx()
        
        # Check for ship overlap...
        otherShip = self.window.getOtherShip(self)
        if otherShip != None and intersectCircles(self.pos, Ship.SHIP_SHELL_RADIUS/2, otherShip.pos, Ship.SHIP_SHELL_RADIUS/2):
            self.pos += dir * 0.1
            otherShip.pos += dir * -0.1

    def toWorld(self, pt):
        return self.pos + self.forward() * pt[0] + self.dir * pt[1]

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
        if isinstance(nextCommand, ShipCmd_Shoot):
            shotDir = unit(nextCommand.dir)
            dotValue = dot(unit(self.dir), shotDir)
            if dotValue < 0.999:
                dotRight = dot(shotDir, self.right())
                angle = math.degrees(math.acos(dotValue))
                if dotRight > 0:
                    nextCommand = ShipCmd_ThrustLeft(angle)
                else:
                    nextCommand = ShipCmd_ThrustRight(angle)
                needToTurnFirst = True
        
        # grab the next queued command
        self.activeCommand = nextCommand
        if not needToTurnFirst:
            self.queuedCommands.pop(0)
        
        # log it
        log(("    " if needToTurnFirst else "--> ") + self.activeCommand.description())
        
        # setup next new command (save off starting information)...
        self.activeCommand.startPos = self.pos
        self.activeCommand.startDir = self.dir
        
        # Make it cost something...
        pointCost = -2 if isinstance(self.activeCommand, ShipCmd_Shoot) else -1
        self.window.awardPoints(pointCost, self.playerIdx)

    def updateCommand(self, deltaTime):
        if self.activeCommand == None:
            # check for queued
            if len(self.queuedCommands) > 0:
                self.finishActiveCommand()
            if self.activeCommand == None:
                return
        if isinstance(self.activeCommand, ShipCmd_Thrust):
            moveDst = self.activeCommand.dst
            moveTravelTime = moveDst / self.shipMoveSpeed
            moveVec = self.dir * moveDst
            
            # update the active command
            self.activeCommand.progress = min(self.activeCommand.progress + deltaTime / moveTravelTime, 1)
            self.pos = self.activeCommand.startPos + moveVec * self.activeCommand.progress
            self.updateThrusterGfx(True, True)
            self.vel = self.dir * (moveDst / moveTravelTime)
            
            # check for ship overlap
            otherShip = self.window.getOtherShip(self)
            if otherShip != None and intersectCircles(self.pos, Ship.SHIP_SHELL_RADIUS/2, otherShip.pos, Ship.SHIP_SHELL_RADIUS/2):
                deltaVec = unit(self.pos - otherShip.pos)
                self.pos += deltaVec * 0.1
                self.activeCommand.progress = 1
            
            # keep in bounds
            if self.pos[0] <= Ship.SHIP_SHELL_RADIUS/2:
                self.pos += v2_right() * 0.1
                self.activeCommand.progress = 1
            if self.pos[1] <= Ship.SHIP_SHELL_RADIUS/2:
                self.pos += v2_up() * 0.1
                self.activeCommand.progress = 1
            if self.pos[0] >= self.window.maxCoordinateX() - Ship.SHIP_SHELL_RADIUS/2:
                self.pos += v2_left() * 0.3
                self.activeCommand.progress = 1
            if self.pos[1] >= self.window.maxCoordinateY() - Ship.SHIP_SHELL_RADIUS/2:
                self.pos += v2_down() * 0.3
                self.activeCommand.progress = 1
            
            # and check for done
            if self.activeCommand.progress == 1:
                self.vel = v2_zero()
                self.updateThrusterGfx(False, False)
                self.finishActiveCommand()
        elif isinstance(self.activeCommand, ShipCmd_ThrustLeft) or isinstance(self.activeCommand, ShipCmd_ThrustRight):
            leftRightScalar = 1 if isinstance(self.activeCommand, ShipCmd_ThrustRight) else -1
            angleDelta = self.activeCommand.angle
            moveTravelTime = abs(angleDelta) / self.shipTurnSpeed if angleDelta != 0 else 0.000001
            
            # update the active command
            self.activeCommand.progress = min(self.activeCommand.progress + deltaTime / moveTravelTime, 1)
            self.dir = unit(rotateVec2(self.activeCommand.startDir, angleDelta * self.activeCommand.progress * leftRightScalar))
            self.updateThrusterGfx(isinstance(self.activeCommand, ShipCmd_ThrustRight), isinstance(self.activeCommand, ShipCmd_ThrustLeft))
            
            # and...check for done...
            if self.activeCommand.progress == 1:
                self.updateThrusterGfx(False, False)
                self.finishActiveCommand()
        elif isinstance(self.activeCommand, ShipCmd_Shoot):
            # enforce a max shot period
            timeSinceShot = (time.time() - self.timeLastShot)
            if timeSinceShot > 1 and self.ammo > 0:
                # shoot, save off the time, and then we're done with the cmd
                self.ammo -= 1
                Ammo(self.window, self.playerIdx, self.ammoSpawnLocation(), self.dir, self.ammoMaxRange)
                self.timeLastShot = time.time()
                self.finishActiveCommand()
            elif self.ammo <= 0:
                log("    (shooting without any ammo)")
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