import tkinter as tk
from lib.window import Window
from lib.winobj_target import Target
from lib.winobj_powerup import PowerUp
from lib.winobj_ammo import Ammo
from lib.winobj_tank import *
from lib.winobj_ship import *
from lib.utils import *
import enum
import random
import asyncio

class WindowArenaConfig(enum.Flag):
    TANKS_TUTORIAL = enum.auto()
    TANKS_DEFAULT = enum.auto()
    TANKS_ADVANCED = enum.auto()
    TANKS_INTERACTIVE = enum.auto()
    SPACE_BATTLE = enum.auto()

class WindowArena(Window):
    def __init__(self, userCode1 = None, userCode2 = None, interactExecCmd = None, interactGameDone = None, gameConfig = WindowArenaConfig.TANKS_DEFAULT, windowTitle = "Arena Window"):
        self.gameConfig = gameConfig

        bckGndImage = "res/space-background.jpg" if self.isSpaceBattle() else None
        super().__init__(windowTitle, gridPixelsPerUnit = 48, gridOriginAtLL = True, bckGndImage = bckGndImage)
        
        self.playerCount = 2 if userCode2 is not None else 1
        if self.isTanks():
            self.tanks = [ None, None ]
        elif self.isSpaceBattle():
            self.ships = [ None, None ]
        self.userCode = [ userCode1, userCode2 ]
        self.interactExecCmd = interactExecCmd
        self.interactGameDone = interactGameDone
        
    def initApp(self):
        super().initApp()

        # text UI
        self.createTimerAndScore()
        
        # kick off the simulation
        self.resetSimulation()
    
    def isTanks(self):
        if (self.gameConfig & WindowArenaConfig.TANKS_TUTORIAL) or (self.gameConfig & WindowArenaConfig.TANKS_DEFAULT) or (self.gameConfig & WindowArenaConfig.TANKS_ADVANCED) or (self.gameConfig & WindowArenaConfig.TANKS_INTERACTIVE):
            return True
        return False
    def isTanks_TutorialMode(self):
        return True if self.gameConfig & WindowArenaConfig.TANKS_TUTORIAL else False
    def isTanks_AdvancedMode(self):
        return True if ((self.gameConfig & WindowArenaConfig.TANKS_ADVANCED) or (self.gameConfig & WindowArenaConfig.TANKS_INTERACTIVE)) else False
    def isTanks_InteractiveMode(self):
        return True if self.gameConfig & WindowArenaConfig.TANKS_INTERACTIVE else False
    def isSpaceBattle(self):
        return True if self.gameConfig & WindowArenaConfig.SPACE_BATTLE else False
        
    def update(self, deltaTime):
        if self.levelTime > 0:
            super().update(deltaTime)
        
        # level update
        self.updateLevel(deltaTime)
        
        # user code update (tanks)
        if self.isTanks() and self.levelTime > 0 and not self.isTanks_InteractiveMode():
            powerUps = self.sim.objectsOfType(PowerUp)
            targets = self.sim.objectsOfType(Target)
            if self.isTanks_AdvancedMode():
                # advanced mode (list of powerups and targets)
                for i, userCode in enumerate(self.userCode):
                    if userCode != None and self.isReadyToAskCodeForNextCommand(i):
                        userCode(self.tanks[i], powerUps, targets)
            else:
                # tutorial or basic mode
                for i, userCode in enumerate(self.userCode):
                    if userCode != None and self.isReadyToAskCodeForNextCommand(i):
                        userCode(self.tanks[i], powerUps[0], targets[0] if len(targets) > 0 else None)
        elif self.isSpaceBattle():
            powerUps = self.sim.objectsOfType(PowerUp)
            targets = self.sim.objectsOfType(Target)
            # advanced mode (list of powerups and targets)
            for i, userCode in enumerate(self.userCode):
                if userCode != None and self.isReadyToAskCodeForNextCommand(i):
                    userCode(self.ships[i], powerUps, targets)

    # interactive mode support
    def onMouseLeftPressed(self, event):
        super().onMouseLeftPressed(event)
        
        # interactive support (tanks)
        if self.isTanks_InteractiveMode():
            tank = self.tanks[0]
            if not self.isAnyActionHappening():
                # if clicking on a target, shoot at it
                mousePos = self.toCoordFrame(v2(event.x, event.y))
                target = self.getTargetAtPos(mousePos)
                if target is not None:
                    if length(target.pos - tank.pos) <= (tank.ammoMaxRange + 0.5):
                        self.interactiveExecCmd( tank, TankCmd_Shoot(target.pos - tank.pos) )
                    else:
                        log(" * target out of shot range, skipping command")
                else:
                    # otherwise move there
                    delta = mousePos - tank.pos
                    self.interactiveExecCmd( tank, TankCmd_Move(delta) )
            else:
                log(" *** click ignored, tank is busy")
    def interactiveExecCmd(self, tank, tankCmd):
        # log it
        tank = self.tanks[0]
        targets = self.sim.objectsOfType(Target)
        powerUps = self.sim.objectsOfType(PowerUp)
        self.interactExecCmd(tankCmd, self.levelTime, tank, powerUps, targets)
        
        # tell the tank about it
        if isinstance(tankCmd, TankCmd_Move):
            if abs(tankCmd.dir[0]) > 0.25:
                tank.queueCommand( TankCmd_Move(v2(tankCmd.dir[0], 0)) )
            if abs(tankCmd.dir[1]) > 0.25:
                tank.queueCommand( TankCmd_Move(v2(0, tankCmd.dir[1])) )
        else:
            tank.queueCommand( tankCmd )
    def getTargetAtPos(self, pos, minDst = 0.1):
        targets = self.sim.objectsOfType(Target)
        for target in targets:
            if length(target.pos - pos) < (target.radius + minDst):
                return target
        return None
    
    def createTimerAndScore(self):
        self.textScoreFinal = tk.Label(self.root, text = "<textScoreFinal>")
        self.textScoreFinal.pack_forget() # default hidden
        
        posPixels = (self.toPixelsX(self.maxCoordinateX() / 2) - 9, self.toPixelsY(self.maxCoordinateY() - 0.3))
        timerColor = "black" if self.isTanks() else "white"
        self.gfxTimer = self.canvas.create_text(
            posPixels[0], posPixels[1], text = "Time: ", font=("Arial", 14), fill = timerColor, anchor = tk.CENTER)
        
        posPixels = (self.toPixelsX(self.maxCoordinateX() - 0.25), self.toPixelsY(self.maxCoordinateY() - 0.3))
        scoreColor = "green" if self.isTanks() else "lightgreen"
        self.gfxScoreRight = self.canvas.create_text(
            posPixels[0], posPixels[1], text = "Score: ", font=("Arial", 14), fill = scoreColor, anchor = tk.E)

        if (self.playerCount > 1):
            posPixels = (self.toPixelsX(self.minCoordinateX() + 0.25), self.toPixelsY(self.maxCoordinateY() - 0.3))
            scoreColor = "blue" if self.isTanks() else "lightblue"
            self.gfxScoreLeft = self.canvas.create_text(
                posPixels[0], posPixels[1], text = "Score: ", font=("Arial", 14), fill = scoreColor, anchor = tk.W)
    
    def updateTimerAndScoreText(self):
        minutes, seconds = divmod(self.levelTime, 60)
        self.canvas.itemconfig(self.gfxTimer, text = f"{int(minutes):d}:{int(seconds):02d}")
        self.canvas.itemconfig(self.gfxScoreRight, text = f"{self.playerNames[0]}: {self.levelScores[0]}")
        if (self.playerCount > 1):
            self.canvas.itemconfig(self.gfxScoreLeft, text = f"{self.playerNames[1]}: {self.levelScores[1]}")
        
    def onMouseLeftDoubleClick(self, event):
        self.resetSimulation(True)
        
    def awardPoints(self, points, playerIdx = 0):
        self.levelScores[0] += points if (playerIdx == 0) else 0
        self.levelScores[1] += points if (playerIdx == 1) else 0
        self.updateTimerAndScoreText()
        
    def getOtherTank(self, thisTank):
        return self.tanks[1] if self.tanks[0] == thisTank else self.tanks[0]
    def getOtherShip(self, thisShip):
        return self.ships[1] if self.ships[0] == thisShip else self.ships[0]
    
    def setPlayerName(self, playerName, playerIdx):
        if playerIdx < len(self.playerNames):
            self.playerNames[playerIdx] = playerName
    
    def resetSimulation(self, fullReset = True):
        # maybe destroy all objects
        if fullReset:
            self.sim.destroyAll()
            
            # player names
            self.playerNames = [ "Player 1", "Player 2" ]

            # level setup        
            self.onLevelSetup()
            
        # clear any end of game messages
        self.textScoreFinal.pack_forget()
        
        # tell the simulation about it
        self.sim.update(0)
        
    def onLevelSetup(self):
        # tutorial support
        isTutorial = True if self.gameConfig & WindowArenaConfig.TANKS_TUTORIAL else False

        # score and timer
        self.levelScores = [0, 0]
        self.levelTime = 60 if isTutorial else 90

        # create the tanks
        if self.isTanks():
            self.tanks[0] = Tank(self, 0, v2(1.5, 1.5), v2_right())
            if (self.playerCount > 1):
                self.tanks[1] = Tank(self, 1, clampToClosestHalfUnit(v2(self.maxCoordinateX() - 1.5, 1.5)), v2_left())
        elif self.isSpaceBattle():
            self.ships[0] = Ship(self, 0, v2(1.5, 1.5), v2_right())
            if (self.playerCount > 1):
                self.ships[1] = Ship(self, 1, clampToClosestHalfUnit(v2(self.maxCoordinateX() - 1.5, 1.5)), v2_left())

        # first time update
        self.updateLevel(0, True)

        # text
        self.updateTimerAndScoreText()
        
    def spaceBattlePickTargetDirection(self, spawnPos):
        if spawnPos[0] < self.maxCoordinateX() * 0.3:
            return v2_right()
        elif spawnPos[0] > self.maxCoordinateX() * 0.7:
            return v2_left()
        elif spawnPos[1] < self.maxCoordinateY() * 0.3:
            return v2_up()
        elif spawnPos[0] > self.maxCoordinateY() * 0.7:
            return v2_down()
        rnd = random.random()
        if rnd < 0.25: 
            return v2_right()
        elif rnd < 0.5:
            return v2_left()
        elif rnd < 0.75:
            return v2_up()
        return v2_down()

    def updateLevel(self, deltaTime, firstUpdate = False):
        # config
        levelCount_Targets = 0 if self.isTanks_TutorialMode() else (3 if self.isTanks_AdvancedMode() else 1)
        levelCount_Powerups = 3 if self.isTanks_AdvancedMode() else 1
        if self.isSpaceBattle():
            levelCount_Targets = 4
            levelCount_Powerups = 5
        
        # level time
        prevLevelTime = self.levelTime
        self.levelTime = max(self.levelTime - deltaTime, 0)
        if prevLevelTime > 0 and self.levelTime <= 0:
            self.onEndOfGame()
        if self.levelTime <= 0:
            return
        self.updateTimerAndScoreText()
        
        # spawn in center
        spawnInCenter = True if firstUpdate and self.playerCount > 1 else False
        
        # maybe spawn some targets
        targets = self.sim.objectsOfType(Target)
        while len(targets) < levelCount_Targets:
            loc = self.pickSpawnLocation(5, 3, 3, 0.9, True, spawnInCenter)
            vel = v2_zero()
            if self.isSpaceBattle():
                vel = self.spaceBattlePickTargetDirection(loc) * (random.random() * 1.0 + 1.0)
            targets.append( Target(self, loc, vel = vel) )
            
        # maybe spawn some powerups
        powerUps = self.sim.objectsOfType(PowerUp)
        while len(powerUps) < levelCount_Powerups:
            loc = self.pickSpawnLocation(5, 3, 3, 0.9, True, spawnInCenter)
            pwrUpOptions = [ "P" ]
            if not self.isTanks_TutorialMode():
                pwrUpOptions.append( "R" )
                pwrUpOptions.append( "S" )
            if self.isSpaceBattle():
                pwrUpOptions = [ "1", "1", "2", "2", "3", "R", "S" ]
            pwrUpType = pwrUpOptions[ int(len(pwrUpOptions) * random.random()) ]
            powerUps.append( PowerUp(self, loc, pwrUpType) )

        # check for object-object collisions            
        self.checkForCollisions()
        
    def onEndOfGame(self):
        if self.playerCount > 1:
            winnerText = "It is a Tie!!!"
            if self.levelScores[0] > self.levelScores[1]:
                winnerText = self.playerNames[0] + " Wins!"
            elif self.levelScores[0] < self.levelScores[1]:
                winnerText = self.playerNames[1] + " Wins!"
            self.textScoreFinal.config(text = winnerText)
        else:
            self.textScoreFinal.config(text = f"Final Score: {self.levelScores[0]}")
        
        # show and put at front
        self.textScoreFinal.pack(side = tk.TOP)
        
        # interactive mode support
        if self.isTanks_InteractiveMode() and self.interactGameDone is not None:
            self.interactGameDone()
        
        # leaderboard
        asyncio.run(self.postToLeaderboard())
            
    def checkForCollisions(self):
        # ammo
        ammos = self.sim.objectsOfType(Ammo)
        for ammo in ammos:
            # check for hitting targets
            targets = self.sim.objectsOfType(Target)
            for target in targets:
                if intersectCircles(target.pos, target.radius, ammo.pos, ammo.radius):
                    # tell the target about it & that's it for us
                    target.onHitByAmmo(ammo.playerIdx)
                    ammo.timeTillDeath = max(ammo.timeTillDeath, 0.0001)
            
            # check for hitting tanks
            tanks = self.sim.objectsOfType(Tank)
            for tank in tanks:
                # note: don't let someone hit themselves
                if ammo.playerIdx != tank.playerIdx and intersectCircles(tank.pos, tank.TANK_BODY_SIZE/2, ammo.pos, ammo.radius):
                    # award points
                    self.awardPoints(25, ammo.playerIdx)
                    log("(hit tank: score +25)")
                    
                    # kick the tank back (if you can)
                    tank.kickBackTank(unit(tank.pos - ammo.pos))
                    
                    # that's it for the ammo
                    ammo.timeTillDeath = max(ammo.timeTillDeath, 0.0001)
                    
            # check for hitting ships
            ships = self.sim.objectsOfType(Ship)
            for ship in ships:
                # note: don't let someone hit themselves
                if ammo.playerIdx != ship.playerIdx and intersectCircles(ship.pos, ship.SHIP_SHELL_RADIUS/2, ammo.pos, ammo.radius):
                    # award points
                    self.awardPoints(25, ammo.playerIdx)
                    log("(hit ship: score +25)")
                    
                    # kick the ship back (if you can)
                    ship.kickBackShip(unit(ship.pos - ammo.pos))
                    
                    # that's it for the ammo
                    ammo.timeTillDeath = max(ammo.timeTillDeath, 0.0001)

    def calcMinDstFromObjectOfType(self, pos, objType):
        minDst = 10000000
        objects = self.sim.objectsOfType(objType)
        for obj in objects:
            thisDst = length(pos - obj.pos)
            minDst = min(minDst, thisDst)
        return minDst

    def execCodeRequestedTankCommands(self, tank):
        for cmd in self.queuedCodeCommands:
            if cmd.cmd is None or cmd.paramDir is None or cmd.paramDir[0] is None or cmd.paramDir[1] is None:
                log("INVALID COMMAND: missing or invalid parameters")
                raise Exception("INVALID COMMAND: missing or invalid parameters")
                return
            tankCmd = None
            skipThisCmd = False
            if cmd.cmd.toLowerCase() == TankCmd_Move.type:
                if abs(cmd.paramDir[0]) > 0.000001 and abs(cmd.paramDir[1]) > 0.000001:
                    log("INVALID MOVE: Tanks move only horizontally & vertically")
                    raise Exception('INVALID MOVE: Tanks move only horizontally & vertically')
                if lengthSqr(cmd.paramDir) < 0.001:
                    log("INVALID MOVE: Zero distance")
                    skipThisCmd = True
                tankCmd = TankCmd_Move(cmd.paramDir)
            elif cmd.cmd.toLowerCase() == TankCmd_Turn.type: 
                tankCmd = TankCmd_Turn(cmd.paramDir)
            elif cmd.cmd.toLowerCase() == TankCmd_Shoot.type: 
                if lengthSqr(cmd.paramDir) < 0.001:
                    log("INVALID SHOT: Zero direction vector")
                    skipThisCmd = True
                tankCmd = TankCmd_Shoot(cmd.paramDir)
            else:
                log("INVALID COMMAND: " + cmd.cmd)
                raise Exception("INVALID COMMAND: " + cmd.cmd)
            
            if not skipThisCmd:
                tank.queueCommand(tankCmd)
        queuedCodeCommands = []

    def isReadyToAskCodeForNextCommand(self, playerIdx):
        if self.isTanks():
            for tank in self.tanks:
                if tank == None or tank.playerIdx != playerIdx:
                    continue
                if tank.hasCommand():
                    return False
        if self.isSpaceBattle():
            for ship in self.ships:
                if ship == None or ship.playerIdx != playerIdx:
                    continue
                if ship.hasCommand():
                    return False
        powerUps = self.sim.objectsOfType(PowerUp)
        for powerUp in powerUps:
            if powerUp.isDying():
                return False
        targets = self.sim.objectsOfType(Target)
        for target in targets:
            if target.isDying():
                return False
        ammos = self.sim.objectsOfType(Ammo)
        if len(ammos) > 0: # count an active shot as busy...
            return False
        return True

    def isAnyActionHappening(self):
        for playerIdx in range(self.playerCount):
            if not self.isReadyToAskCodeForNextCommand(playerIdx):
                return True
        ammos = self.sim.objectsOfType(Ammo)
        for ammo in ammos:
            if ammo.vel[0] != 0 or ammo.vel[1] != 0:
                return True
        targets = self.sim.objectsOfType(Target)
        for target in targets:
            if target.isDying():
                return True
        powerUps = self.sim.objectsOfType(PowerUp)
        for powerUp in powerUps:
            if powerUp.isDying():
                return True
        return False
    
    def pickSpawnLocation(self, minDstFromPlayer, minDstFromTargets, minDstFromPowerUps, minDstFromSides, clampToCenters, favorMidX):
        # loop over some number of attempts
        maxAttempts = 100
        pos = v2(self.maxCoordinateX() / 2, self.maxCoordinateY() / 2)
        for i in range(maxAttempts):
            # random
            pos = v2(random.uniform(0, self.maxCoordinateX() - 0.5), random.uniform(0, self.maxCoordinateY() - 0.5))
            
            # Support favorMidX (we use this on multiplayer, to try to keep things more fair)...
            if favorMidX:
                pos[0] = random.uniform( self.maxCoordinateX() * 0.45, self.maxCoordinateX() * 0.55 )
            
            # maybe clamp to square centers
            if clampToCenters:
                pos = v2(math.floor(pos[0]) + 0.5, math.floor(pos[1]) + 0.5)
        
            # check it against our constraints (if last attempt, just go with it)...
            if i < (maxAttempts - 1):
                # check distance from sides
                minDstFromSide = min(min(min(pos[0], pos[1]), self.maxCoordinateX() - pos[0]), self.maxCoordinateY() - pos[1])
                if minDstFromSide < minDstFromSides:
                    continue

                # next, distance from tanks, targets, powerups
                minDstFromTank = self.calcMinDstFromObjectOfType(pos, Tank)
                if minDstFromTank < minDstFromPlayer:
                    continue
                minDstFromShip = self.calcMinDstFromObjectOfType(pos, Ship)
                if minDstFromShip < minDstFromPlayer:
                    continue
                minDstFromTarget = self.calcMinDstFromObjectOfType(pos, Target)
                if minDstFromTarget < minDstFromTargets:
                    continue
                minDstFromPowerUp = self.calcMinDstFromObjectOfType(pos, PowerUp)
                if minDstFromPowerUp < minDstFromPowerUps:
                    continue
            
            # this one works, break out
            break
        
        return pos

    async def postToLeaderboard(self):
        await self.postLeaderboard(self.playerNames[0], self.levelScores[0])
        if self.playerCount > 1:
            await self.postLeaderboard(self.playerNames[1], self.levelScores[1])
