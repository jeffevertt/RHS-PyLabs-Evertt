import tkinter as tk
from lib.window import Window
from lib.window_3d import Window3D
from lib.winobj_sphere import Sphere
from lib.winobj_line import Line
from lib.utils import *

class WindowBounce3D(Window3D):
    def __init__(self, updateBallFn = None):
        super().__init__("Lab 08: Bounce 3D!")

        self.ballColorNext = 0
        self.ballColors = [ 'blue', 'darkgreen', 'magenta', 'cadetblue', 'cornsilk', 'deeppink', 'darksalmon', 'darkorchid', 'goldenrod', 'indigo', 'khaki', 'greenyellow', 'orange' ];
        self.ballRadius = 1.0
        self.updateBallFn = updateBallFn
        
        self.initApp()
        
    def initApp(self):
        super().initApp()

        # world box & lines
        self.worldBoxHalfSize = v3(10, 10, 10)
        self.createWorldBoxLines()
    
    def createWorldBoxLines(self):
        self.sim.destroyAllOfType(Line)

        lineColor = "black"
        self.worldBoxVerts = [ v3(-self.worldBoxHalfSize[0],  self.worldBoxHalfSize[1], 0), v3( self.worldBoxHalfSize[0],  self.worldBoxHalfSize[1], 0), 
                               v3(-self.worldBoxHalfSize[0], -self.worldBoxHalfSize[1], 0), v3( self.worldBoxHalfSize[0], -self.worldBoxHalfSize[1], 0),
                               v3(-self.worldBoxHalfSize[0],  self.worldBoxHalfSize[1], 2 * self.worldBoxHalfSize[2]), v3( self.worldBoxHalfSize[0],  self.worldBoxHalfSize[1], 2 * self.worldBoxHalfSize[2]), 
                               v3(-self.worldBoxHalfSize[0], -self.worldBoxHalfSize[1], 2 * self.worldBoxHalfSize[2]), v3( self.worldBoxHalfSize[0], -self.worldBoxHalfSize[1], 2 * self.worldBoxHalfSize[2]) ];
        self.worldBoxPlanes = [ (self.worldBoxVerts[0], v3_forward()), (self.worldBoxVerts[7], v3_backwards()),
                                (self.worldBoxVerts[0], v3_right()), (self.worldBoxVerts[7], v3_left()),
                                (self.worldBoxVerts[0], v3_down()), (self.worldBoxVerts[7], v3_up()) ]
        self.worldBoxLines = []
        for i in range(4 * 3):
            self.worldBoxLines.append( Line( self, v3_zero(), v3_zero(), "black" ) )
        self.updateWorldBoxLines(0)
        
    def updateWorldBoxLines(self, deltaTime):
        self.worldBoxLines[0].updateLinePositions( *self.transformAndClipLine(self.worldBoxVerts[0], self.worldBoxVerts[1]) )
        self.worldBoxLines[1].updateLinePositions( *self.transformAndClipLine(self.worldBoxVerts[2], self.worldBoxVerts[3]) )
        self.worldBoxLines[2].updateLinePositions( *self.transformAndClipLine(self.worldBoxVerts[0], self.worldBoxVerts[2]) )
        self.worldBoxLines[3].updateLinePositions( *self.transformAndClipLine(self.worldBoxVerts[1], self.worldBoxVerts[3]) )

        self.worldBoxLines[4].updateLinePositions( *self.transformAndClipLine(self.worldBoxVerts[4], self.worldBoxVerts[5]) )
        self.worldBoxLines[5].updateLinePositions( *self.transformAndClipLine(self.worldBoxVerts[6], self.worldBoxVerts[7]) )
        self.worldBoxLines[6].updateLinePositions( *self.transformAndClipLine(self.worldBoxVerts[4], self.worldBoxVerts[6]) )
        self.worldBoxLines[7].updateLinePositions( *self.transformAndClipLine(self.worldBoxVerts[5], self.worldBoxVerts[7]) )

        self.worldBoxLines[8].updateLinePositions( *self.transformAndClipLine(self.worldBoxVerts[0], self.worldBoxVerts[4]) )
        self.worldBoxLines[9].updateLinePositions( *self.transformAndClipLine(self.worldBoxVerts[2], self.worldBoxVerts[6]) )
        self.worldBoxLines[10].updateLinePositions( *self.transformAndClipLine(self.worldBoxVerts[1], self.worldBoxVerts[5]) )
        self.worldBoxLines[11].updateLinePositions( *self.transformAndClipLine(self.worldBoxVerts[3], self.worldBoxVerts[7]) )
        
    def onMouseLeftPressed(self, event):
        super().onMouseLeftPressed(event)
        
        # create a ball/sphere and send it on its way
        toScreenSpace = self.transProj @ self.transCamera

        # figure out the ray vector
        normScreenSpace = v4(self.toCoordFrameX(event.x) / self.maxCoordinateX(), -self.toCoordFrameY(event.y) / self.maxCoordinateY(), -1.0, 1)
        x, y, z, w = np.linalg.inv(toScreenSpace) @ normScreenSpace
        ptNearClipInWorldSpace = v3(x / w, y / w, z / w)
        dirVec = unit(v3_from_v4(ptNearClipInWorldSpace) - self.getCameraPos())

        # and the ball pos (intersect with back plane, at zero)
        ballPos = self.getCameraPos() + dirVec * self.ballRadius #intersectLinePlane(v3(0,0,self.ballRadius + 0.1), v3_backwards(), self.getCameraPos(), dirVec)
        ballVel = dirVec * 20.0

        # launch it
        Sphere(self, ballPos, self.ballRadius, ballVel, updateFn = self.updateBallFn, color = self.ballColors[self.ballColorNext % len(self.ballColors)])
        self.ballColorNext += 1
    
    def cullNotInField(self, field):
        balls = self.sim.objectsOfType(Sphere)
        ballsToDestroy = []
        for ball in balls:
            pt2d = self.worldTo2D(ball.pos)
            if not isInsideField(self, pt2d, ball.radius * 2):
                ballsToDestroy.append(ball)
        for ball in ballsToDestroy:
            ball.destroy()
            
    def isInsideWorld(self, pos):
        buffer = self.ballRadius * 0.5
        return not ((pos[0] < -self.worldBoxHalfSize[0] - buffer) or (pos[0] > self.worldBoxHalfSize[0] + buffer) or
                    (pos[1] < -self.worldBoxHalfSize[1] - buffer) or (pos[1] > self.worldBoxHalfSize[1] + buffer) or
                    (pos[2] < -buffer)                           or (pos[2] > 2 * self.worldBoxHalfSize[2] + buffer))
            
    def sortGraphicsObjects(self):
        balls = self.sim.objectsOfType(Sphere)
        balls.sort( key = lambda x: lengthSqr(self.cameraPos - x.pos) + (0 if self.isInsideWorld(x.pos) else 100), reverse=True )
        for ball in balls:
            self.canvas.tag_raise(ball.gfxCircle)
            ball.overrideColor(None if self.isInsideWorld(ball.pos) else self.canvasColor)
        # for (let i = 0; i < this.lines.length; i++):
        #     this.lines[i].toBack()
    
    def update(self, deltaTime):
        super().update(deltaTime)
        
        # camera
        if self.updateCamera(deltaTime):
            # camera has moved, need to update the lines positions
            self.updateWorldBoxLines(deltaTime)
        
        self.sortGraphicsObjects()