import tkinter as tk
from lib.window import Window
from lib.winobj_rectangle import Rectangle
from lib.winobj_circle import Circle
from lib.utils import *
import random

class WindowPlatformer(Window):
    def __init__(self, updateFn = None, createRectFn = None):
        super().__init__("Lab 14c: Platformer (create your own)!", gridPixelsPerUnit = 24)
        
        self.rects = []
        self.points = []
        self.pointsSpawnLoc = []
        self.ball = None
        self.ballRadius = 0.5
        self.timeSinceBall = 0
        self.updateFn = updateFn
        self.createRectFn = createRectFn
        self.rectSpawnPtA = None
        self.rectSpawn = None
        
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
        
        # user code update
        if self.updateFn != None and self.ball != None:
            self.updateFn(deltaTime, self.ball, self.rects, self.isKeyPressed)
            self.sim.updateGfxAllObjects()
    
    def createTimerAndScore(self):
        self.textScoreFinal = tk.Label(self.root, text = "<textScoreFinal>")
        self.textScoreFinal.pack_forget() # default hidden
        
    def onMouseLeftDoubleClick(self, event):
        self.resetSimulation()
        
    def resetSimulation(self, fullReset = True):
        # maybe destroy all objects
        if fullReset:
            self.sim.destroyAll()

            # level setup        
            self.onLevelSetup()
        
        # clear any final game text    
        self.textScoreFinal.pack_forget()
        
        # tell the simulation about it
        self.sim.update(0)
        
    def onLevelSetup(self):
        # create the ball
        self.spawnBall()
        
        # first time update
        self.updateLevel(0, True)
        
    def spawnBall(self):
        spawnPosX = v2(self.minCoordinateX() + 2, self.minCoordinateY() + 2)
        self.ball = Circle(self, spawnPosX, self.ballRadius, v2_zero(), color = "blue")

    def onMouseLeftPressed(self, event):
        self.rectSpawnPtA = clampToClosestWholeUnit(self.toCoordFrame(v2(event.x, event.y)))
        self.rectSpawn = None
        super().onMouseLeftPressed(event)
    def onMouseMotion(self, event):
        if self.rectSpawnPtA is not None and self.createRectFn is not None:
            rectSpawnPtB = clampToClosestWholeUnit(self.toCoordFrame(v2(event.x, event.y)))
            rectLL = v2(min(self.rectSpawnPtA[0], rectSpawnPtB[0]), min(self.rectSpawnPtA[1], rectSpawnPtB[1]))
            rectUR = v2(max(self.rectSpawnPtA[0], rectSpawnPtB[0]), max(self.rectSpawnPtA[1], rectSpawnPtB[1]))
            halfDims = (rectUR - rectLL) * 0.5
            if length(halfDims) > 0.6:
                if self.rectSpawn is None:
                    self.rectSpawn = self.createRectFn(self, rectLL + halfDims, halfDims[0] * 2, halfDims[1] * 2)
            if self.rectSpawn is not None:
                self.rectSpawn.width = halfDims[0] * 2
                self.rectSpawn.height = halfDims[1] * 2
                self.rectSpawn.pos = rectLL + halfDims
                self.rectSpawn.updateGfx()
        super().onMouseMotion(event)
    def onMouseLeftReleased(self, event):
        if self.rectSpawn is not None:
            if self.rectSpawn.width > 0.1 and self.rectSpawn.height > 0.1:
                self.rects.append(self.rectSpawn)
                self.rectSpawn = None
            else:
                self.rectSpawn.destroy()
        self.rectSpawnPtA = None  
        super().onMouseLeftReleased(event)
    def onMouseRightPressed(self, event):
        pos = self.toCoordFrame(v2(event.x, event.y))
        point = Circle(self, pos, 0.2, color = "gold")
        self.points.append(point)
        self.pointsSpawnLoc.append(pos)
        super().onMouseRightPressed(event)
    def onKeyPress(self, event):
        if event.keysym == 'Escape':
            self.resetLevel()
        super().onKeyPress(event)
        
    def resetLevel(self):
        if self.ball is not None:
            self.ball.destroy()
            self.ball = None
        for point in self.points.copy():
            point.destroy()
        self.points = []
        for pos in self.pointsSpawnLoc:
            point = Circle(self, pos, 0.2, color = "gold")
            self.points.append(point)
    def checkForEndCondition(self):
        # end condition
        if len(self.pointsSpawnLoc) > 0 and len(self.points) == 0:
            self.textScoreFinal.config(text = "You WIN!!!")
            self.textScoreFinal.pack(side = tk.TOP)
        else:
            self.textScoreFinal.pack_forget()
            
    def checkForPointsCollected(self):
        if self.ball is None:
            return
        for point in self.points.copy():
            dst = length(self.ball.pos - point.pos)
            if dst < self.ball.radius + point.radius:
                self.points.remove(point)
                point.destroy()

    def updateLevel(self, deltaTime, firstUpdate = False):
        # check for ball outside of level
        if self.ball != None and not intersectRectCircle(self.ball.pos, self.ball.radius * 25, v2(0, 0), v2(self.maxCoordinateX(), self.maxCoordinateY()), 0):
            self.ball.destroy()
            self.ball = None
            
        # check for scoring points & the end condition
        self.checkForPointsCollected()
        self.checkForEndCondition()
        
        # maybe spawn a ball
        if self.ball == None:
            self.timeSinceBall += deltaTime
            if self.timeSinceBall > 2:
                self.resetLevel()
                self.spawnBall()
                self.timeSinceBall = 0
        else:
            self.timeSinceBall = 0
