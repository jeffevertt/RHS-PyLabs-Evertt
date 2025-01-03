import tkinter as tk
from lib.window import Window
from lib.winobj_cannon import Cannon
from lib.winobj_image import Image
from lib.winobj_wall import Wall
from lib.winobj_ammo import Ammo
from lib.utils import *
import random

class WindowAlienInvasion(Window):
    def __init__(self, updateCannonFn = None, updateSecondPlayerFn = None, numAliensInLevel = 5):
        super().__init__("Lab 10: Alien Invasion!", gridPixelsPerUnit = 24)
        
        self.cannons = [None, None]
        self.numAliensInLevel = numAliensInLevel
        self.userCode = [updateCannonFn, updateSecondPlayerFn]
        self.playerCount = 1 if updateSecondPlayerFn is None else 2
        self.alienRadiusMinMax = v2(1.5, 2)
        
    def initApp(self):
        super().initApp()

        # text UI
        self.createTimerAndScore()
        
        # kick off the simulation
        self.resetSimulation()
        
    def update(self, deltaTime):
        super().update(deltaTime)
        
        # level update
        self.updateLevel(deltaTime)        
    
    def createTimerAndScore(self):
        self.textScoreFinal = tk.Label(self.root, text = "<textScoreFinal>")
        self.textScoreFinal.pack_forget() # default hidden
        
        posPixels = (self.toPixelsX(0), self.toPixelsY(self.minCoordinateY() + 0.55))
        self.gfxTimer = self.canvas.create_text(
            posPixels[0], posPixels[1], text = "Time: ", font=("Arial", 14), fill = "white", anchor = tk.CENTER)
        
        posPixels = (self.toPixelsX(self.minCoordinateX() + 0.25), self.toPixelsY(self.minCoordinateY() + 0.55))
        self.gfxScoreLeft = self.canvas.create_text(
            posPixels[0], posPixels[1], text = "Score: ", font=("Arial", 14), fill = "lightgreen", anchor = tk.W)

        if self.playerCount == 2:
            posPixels = (self.toPixelsX(self.maxCoordinateX() - 0.25), self.toPixelsY(self.minCoordinateY() + 0.55))
            self.gfxScoreRight = self.canvas.create_text(
                posPixels[0], posPixels[1], text = "Score: ", font=("Arial", 14), fill = "lightblue", anchor = tk.E)
        else:
            self.gfxScoreRight = None
    
    def updateTimerAndScoreText(self):
        minutes, seconds = divmod(self.levelTime, 60)
        if self.gfxTimer != None:
            self.canvas.itemconfig(self.gfxTimer, text = f"{int(minutes):d}:{int(seconds):02d}")
        self.canvas.lift(self.gfxTimer)
        if self.gfxScoreLeft != None:
            self.canvas.itemconfig(self.gfxScoreLeft, text = f"Score: {self.levelScores[0]}")
            self.canvas.lift(self.gfxScoreLeft)
        if self.gfxScoreRight != None:
            self.canvas.itemconfig(self.gfxScoreRight, text = f"Score: {self.levelScores[1]}")
            self.canvas.lift(self.gfxScoreRight)
        
    def onMouseLeftDoubleClick(self, event):
        self.resetSimulation()
        
    def awardPoints(self, points, playerIdx = 0):
        self.levelScores[0] += points if (playerIdx == 0) else 0
        self.levelScores[1] += points if (playerIdx == 1) else 0
        self.updateTimerAndScoreText()
        
    def resetSimulation(self, fullReset = True):
        # maybe destroy all objects
        if fullReset:
            self.sim.destroyAll()
            
            # player names
            self.playerNames = [ "Green", "Blue" ]
            
            # level setup        
            self.onLevelSetup()
        
        # clear any final game text    
        self.textScoreFinal.pack_forget()
        
        # tell the simulation about it
        self.sim.update(0)
        
    def onLevelSetup(self):
        # score and timer
        self.levelScores = [0, 0]
        self.levelTime = 60
        
        # create the cannon(s)
        cannonHeightAboveGround = 1
        if self.playerCount == 1:
            self.cannons[0] = Cannon(self, 0, v2(0, self.minCoordinateY() + cannonHeightAboveGround))
        else:
            self.cannons[0] = Cannon(self, 0, v2(self.minCoordinateX() * 0.5, self.minCoordinateY() + cannonHeightAboveGround))
            self.cannons[1] = Cannon(self, 1, v2(self.maxCoordinateX() * 0.5, self.minCoordinateY() + cannonHeightAboveGround))

        # create the ground
        self.ground = Wall(self, v2(0, self.minCoordinateY() + cannonHeightAboveGround), v2(0, 1))
        
        # first time update
        self.updateLevel(0, True)

        # text
        self.updateTimerAndScoreText()
        
    def checkForEndCondition(self):
        # end condition
        if self.levelTime == 0:
            winnerText = "It is a Tie!!!"
            if self.playerCount < 2:
                winnerText = "GAME OVER"  
            elif self.levelScores[0] > self.levelScores[1]:
                winnerText = self.playerNames[0] + " Wins!"
            elif self.levelScores[0] < self.levelScores[1]:
                winnerText = self.playerNames[1] + " Wins!"
            self.textScoreFinal.config(text = winnerText)
            
            # show and put at front
            self.textScoreFinal.pack(side = tk.TOP)
            
            # leaderboard
            self.postToLeaderboard()
        else:
            self.textScoreFinal.pack_forget()
            
    async def postToLeaderboard(self):
        await self.postLeaderboard(self.playerNames[0], self.levelScores[0])
        if self.playerCount > 1:
            await self.postLeaderboard(self.playerNames[1], self.levelScores[1])
            
    def updateAlien(self, alien, deltaTime):
        alien.pos += alien.vel * deltaTime
            
    def updateAliens(self, deltaTime, firstUpdate = False):
        # check for scoring
        ammos = self.sim.objectsOfType(Ammo)
        for ammo in ammos:
            aliens = self.sim.objectsOfType(Image)
            for alien in aliens:
                if intersectCircles(ammo.pos, ammo.radius, alien.pos, alien.width/3):
                    self.awardPoints(5, ammo.playerIdx)
                    ammo.destroy()
                    alien.destroy()
                    break

        # maybe spawn aliens
        aliens = self.sim.objectsOfType(Image)
        while len(aliens) < self.numAliensInLevel:
            spawnPosY = self.maxCoordinateY() * (-0.1 + 1.0 * random.random())
            if random.random() < 0.5:
                spawnPos = v2(self.minCoordinateX() - self.alienRadiusMinMax[1], spawnPosY) if not firstUpdate else v2(self.minCoordinateX() + random.random() * (self.maxCoordinateX() - self.minCoordinateX()), spawnPosY)
            else:
                spawnPos = v2(self.maxCoordinateX() + self.alienRadiusMinMax[1], spawnPosY) if not firstUpdate else v2(self.minCoordinateX() + random.random() * (self.maxCoordinateX() - self.minCoordinateX()), spawnPosY)
            spawnVel = v2(random.randint(5,8), 0) if spawnPos[0] < 0 else v2(random.randint(-8,-5), 0)
            spawnRadius = self.alienRadiusMinMax[0] + random.random() * (self.alienRadiusMinMax[1] - self.alienRadiusMinMax[0])
            aliens.append( Image(self, "res/alien.png", spawnPos, spawnRadius * 2, spawnRadius * 2, spawnVel, updateFn = self.updateAlien) )

    def updateLevel(self, deltaTime, firstUpdate = False):
        # level time
        prevLevelTime = self.levelTime
        self.levelTime = max(self.levelTime - deltaTime, 0)
        self.updateTimerAndScoreText()
        if prevLevelTime > 0 and self.levelTime <= 0:
            self.checkForEndCondition()
        if self.levelTime <= 0:
            return
        
        # check for ammo and aliens outside of level
        ammos = self.sim.objectsOfType(Ammo)
        for ammo in ammos:
            if not intersectRectCircle(ammo.pos, ammo.radius * 5, v2(0, 0), v2(self.maxCoordinateX(), self.maxCoordinateY()), 0):
                ammo.destroy()
        aliens = self.sim.objectsOfType(Image)
        for alien in aliens:
            if not intersectRectCircle(alien.pos, alien.width/2 * 5, v2(0, 0), v2(self.maxCoordinateX(), self.maxCoordinateY()), 0):
                alien.destroy()

        # update aliens
        self.updateAliens(deltaTime, firstUpdate)
        
        # user code update
        aliens = self.sim.objectsOfType(Image)
        for i, userCode in enumerate(self.userCode):
            if userCode != None and self.cannons[i].isIdle():
                userCode(self.cannons[i], aliens, deltaTime)
                
        # update the cannons
        for cannon in self.cannons:
            if cannon != None:
                cannon.update(deltaTime)        