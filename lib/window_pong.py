import tkinter as tk
from lib.window import Window
from lib.winobj_rectangle import Rectangle
from lib.winobj_circle import Circle
from lib.winobj_wall import Wall
from lib.utils import *
import random

class WindowPong(Window):
    def __init__(self, updateBallFn = None, onCreateWorld = None, onCreateWorldPre = None, canvasColor='#F4EAD7', bckGndImage = None):
        super().__init__("Lab 09: Pong!", gridPixelsPerUnit = 24, canvasColor=canvasColor, bckGndImage=bckGndImage)
        
        self.walls = [None, None]
        self.paddles = [None, None]
        self.ball = None
        self.ballRadius = 0.5
        self.wallThickness = 1.0
        self.paddleSpeed = 5.0
        self.timeSinceBall = 0
        self.spawnNextBallRight = True
        self.userCode = updateBallFn
        self.createWorldPre = onCreateWorldPre
        self.createWorld = onCreateWorld
        
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
        if self.userCode != None and self.ball != None:
            self.userCode(deltaTime, self.ball, self.walls, self.paddles)
            self.sim.updateGfxAllObjects()
    
    def createTimerAndScore(self):
        self.textScoreFinal = tk.Label(self.root, text = "<textScoreFinal>")
        self.textScoreFinal.pack_forget() # default hidden
        
        posPixels = (self.toPixelsX(0), self.toPixelsY(self.maxCoordinateY() - 0.55))
        self.gfxTimer = self.canvas.create_text(
            posPixels[0], posPixels[1], text = "Time: ", font=("Arial", 14), fill = "white", anchor = tk.CENTER)
        
        posPixels = (self.toPixelsX(self.maxCoordinateX() - 0.25), self.toPixelsY(self.maxCoordinateY() - 0.55))
        self.gfxScoreRight = self.canvas.create_text(
            posPixels[0], posPixels[1], text = "Score: ", font=("Arial", 14), fill = "lightgreen", anchor = tk.E)

        posPixels = (self.toPixelsX(self.minCoordinateX() + 0.25), self.toPixelsY(self.maxCoordinateY() - 0.55))
        self.gfxScoreLeft = self.canvas.create_text(
            posPixels[0], posPixels[1], text = "Score: ", font=("Arial", 14), fill = "lightblue", anchor = tk.W)
    
    def updateTimerAndScoreText(self):
        minutes, seconds = divmod(self.levelTime, 60)
        self.canvas.itemconfig(self.gfxTimer, text = f"{int(minutes):d}:{int(seconds):02d}")
        self.canvas.itemconfig(self.gfxScoreRight, text = f"Score: {self.levelScores[0]}")
        self.canvas.itemconfig(self.gfxScoreLeft, text = f"Score: {self.levelScores[1]}")
        self.canvas.lift(self.gfxTimer)
        self.canvas.lift(self.gfxScoreRight)
        self.canvas.lift(self.gfxScoreLeft)
        
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
        
    def updatePaddleLeft(self, paddle, deltaTime):
        maxPos = self.maxCoordinateY() - self.wallThickness - paddle.height / 2
        minPos = self.minCoordinateY() + self.wallThickness + paddle.height / 2
        if self.isKeyPressed('a') and paddle.pos[1] < maxPos:
            paddle.pos[1] = min(paddle.pos[1] + self.paddleSpeed * deltaTime, maxPos)
        if self.isKeyPressed('z') and paddle.pos[1] > minPos:
            paddle.pos[1] = max(paddle.pos[1] - self.paddleSpeed * deltaTime, minPos)
            
    def updatePaddleRight(self, paddle, deltaTime):
        maxPos = self.maxCoordinateY() - self.wallThickness - paddle.height / 2
        minPos = self.minCoordinateY() + self.wallThickness + paddle.height / 2
        if self.isKeyPressed('Up') and paddle.pos[1] < maxPos:
            paddle.pos[1] = min(paddle.pos[1] + self.paddleSpeed * deltaTime, maxPos)
        if self.isKeyPressed('Down') and paddle.pos[1] > minPos:
            paddle.pos[1] = max(paddle.pos[1] - self.paddleSpeed * deltaTime, minPos)
        
    def onLevelSetup(self):
        # score and timer
        self.levelScores = [0, 0]
        self.levelTime = 60

        # user callback
        if self.createWorldPre is not None:
            self.createWorldPre(self)

        # create walls
        self.walls[0] = Wall(self, v2(0, self.minCoordinateY() + self.wallThickness), v2(0, 1))
        self.walls[1] = Wall(self, v2(0, self.maxCoordinateY() - self.wallThickness), v2(0, -1))
        
        # create the paddles
        paddleDims = v2(0.5, 4)
        self.paddles[0] = Rectangle(self, v2(self.minCoordinateX() + paddleDims[0] * 2, 0), paddleDims[0], paddleDims[1], color = "blue", updateFn = self.updatePaddleLeft)
        self.paddles[1] = Rectangle(self, v2(self.maxCoordinateX() - paddleDims[0] * 2, 0), paddleDims[0], paddleDims[1], color = "green", updateFn = self.updatePaddleRight)
        
        # create the ball
        self.ball = Circle(self, v2(self.maxCoordinateX() - 3, 0), self.ballRadius, v2(-12, 0), color = "red")
        
        # first time update
        self.updateLevel(0, True)

        # text
        self.updateTimerAndScoreText()

        # user callback
        if self.createWorld is not None:
            self.createWorld(self)
        
    def checkForEndCondition(self):
        # end condition
        if self.levelTime == 0:
            if self.ball == None:
                winnerText = "It is a Tie!!!"
                if self.levelScores[0] > self.levelScores[1]:
                    winnerText = self.playerNames[0] + " Wins!"
                elif self.levelScores[0] < self.levelScores[1]:
                    winnerText = self.playerNames[1] + " Wins!"
                self.textScoreFinal.config(text = winnerText)
                
                # show and put at front
                self.textScoreFinal.pack(side = tk.TOP)
            else:
                self.levelTime = 0.000001
        else:
            self.textScoreFinal.pack_forget()

    def updateLevel(self, deltaTime, firstUpdate = False):
        # level time
        prevLevelTime = self.levelTime
        self.levelTime = max(self.levelTime - deltaTime, 0)
        self.updateTimerAndScoreText()
        if prevLevelTime > 0 and self.levelTime <= 0:
            self.checkForEndCondition()
        if self.levelTime <= 0:
            return
        
        # check for scoring
        if self.ball != None and intersectRectCircle(self.ball.pos, 0.01, v2(self.minCoordinateX() - 5, 0), v2(5, self.maxCoordinateY()), 0):
            self.awardPoints(1, 0)
            self.ball.destroy()
            self.ball = None
            self.spawnNextBallRight = False
        if self.ball != None and intersectRectCircle(self.ball.pos, 0.01, v2(self.maxCoordinateX() + 5, 0), v2(5, self.maxCoordinateY()), 0):
            self.awardPoints(1, 1)
            self.ball.destroy()
            self.ball = None
            self.spawnNextBallRight = True
        
        # check for ball outside of level
        if self.ball != None and not intersectRectCircle(self.ball.pos, self.ball.radius * 5, v2(0, 0), v2(self.maxCoordinateX(), self.maxCoordinateY()), 0):
            self.ball.destroy()
            self.ball = None
            self.spawnNextBallRight = True if random.randint(1, 10) <= 5 else False
        
        # maybe spawn a ball
        if self.ball == None:
            self.timeSinceBall += deltaTime
            if self.timeSinceBall > 2:
                spawnPosX = (self.maxCoordinateX() - 3) if self.spawnNextBallRight else (self.minCoordinateX() + 3)
                spawnVel = (unit(v2(-10, random.randint(-5,5))) * 15) if self.spawnNextBallRight else (unit(v2(10, random.randint(-5,5))) * 15)
                self.ball = Circle(self, v2(spawnPosX, 0), self.ballRadius, spawnVel, color = "red")
                self.timeSinceBall = 0
        else:
            self.timeSinceBall = 0
