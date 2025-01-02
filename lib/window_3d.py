import tkinter as tk
from lib.window import Window
from lib.utils import *

# right handed, y up (z forward, x left)
class Window3D(Window):
    def __init__(self, title):
        super().__init__(title, gridEnable = False)
        
    def initApp(self):
        super().initApp()

        # transforms
        self.cameraFov_fullDeg = 100
        self.setCameraTransform( m3x3Identity(), v3(0,0,0.01) )
        self.transProj = m4x4Proj(self.cameraFov_fullDeg, aspectWoverH = self.width / self.height)
        
        # member vars
        self.cameraRotatedViaMouse = False
    
    def getCameraPos(self):
        return self.cameraPos
    def getCameraRight(self):
        return self.cameraOrient[0]
    def getCameraUp(self):
        return self.cameraOrient[1]
    def getCameraForward(self):
        return self.cameraOrient[2]
    def getCameraLeft(self):
        return -self.getCameraRight()
    def getCameraDown(self):
        return -self.getCameraUp()
    def getCameraBackwards(self):
        return -self.getCameraForward()
    def setCameraPos(self, pos):
        self.setCameraTransform(self.cameraOrient, pos)
    def getCameraOrient(self):
        return self.cameraOrient
    def setCameraOrient(self, orient):
        self.setCameraTransform(orient, self.cameraPos)
    def setCameraTransform(self, orient, pos):
        self.cameraPos = pos
        self.cameraOrient = orient
        self.transCamera = np.eye(4)
        self.transCamera[:3, :3] = self.cameraOrient
        self.transCamera[:3, 3] = -self.cameraOrient @ self.cameraPos
        
    def worldTo2D(self, pos, clip = False):
        toScreenSpace = self.transProj @ self.transCamera
        x, y, z, w = toScreenSpace @ v4(pos)
        x, y, z = x / w, y / w, z / w                                   # in normalized device coordinates (-1 to 1)
        if clip and (z < -1 or z > 1):
            return None
        y = -y                                                          # inverted y
        return v2(x * self.maxCoordinateX(), y * self.maxCoordinateY()) # screen space scaling

    def transformAndClipLine(self, posA, posB, modelToWorld = m4x4Identity()):
        toScreenSpace = self.transProj @ self.transCamera @ modelToWorld
        posA = toScreenSpace @ v4(posA)
        posB = toScreenSpace @ v4(posB)
        posA /= posA[3]
        posB /= posB[3]
        posA, posB = clipLineAgainstNearPlane(posA, posB)
        if posA is None or posB is None:
            return None, None
        posA[1], posB[1] = -posA[1], -posB[1]                           # inverted y
        return v2(posA[0] * self.maxCoordinateX(), posA[1] * self.maxCoordinateY()), v2(posB[0] * self.maxCoordinateX(), posB[1] * self.maxCoordinateY())
    
    def scaleAtPos(self, pos):
        posPt = self.worldTo2D(pos)
        posOneOver = self.worldTo2D(pos + self.getCameraRight())
        return (posOneOver[0] - posPt[0])
    
    def onMouseMotion(self, event):
        prevMousePos = self.lastMousePos
        super().onMouseMotion(event)
        if prevMousePos is None or self.lastMousePos is None:
            return
        # camera rotation support with mouse
        if self.isMouseRightDown:
            mouseMoveToAngle = 3.0
            delta = self.lastMousePos[0] - prevMousePos[0]
            rotAngles = delta * mouseMoveToAngle
            self.setCameraOrient(self.cameraOrient @ m3x3RotAxis(self.getCameraUp(), rotAngles[0]))
            self.setCameraOrient(self.cameraOrient @ m3x3RotAxis(self.getCameraRight(), rotAngles[1]))
            self.setCameraOrient(m3x3LookAt(self.getCameraForward(), v3_up())) # keep y up
            self.cameraRotatedViaMouse = True
    
    def updateCamera(self, deltaTime):
        moveSpeed = 40.0
        rotSpeed = 50.0
        hasMoved = self.cameraRotatedViaMouse
        self.cameraRotatedViaMouse = False
        if self.isKeyPressed("Up") or self.isKeyPressed("w") or self.isKeyPressed("Down") or self.isKeyPressed("s"):
            transDst = moveSpeed * deltaTime * (-1 if self.isKeyPressed("Down") or self.isKeyPressed("s") else 1)
            self.setCameraPos(self.cameraPos + self.getCameraForward() * transDst)
            hasMoved = True
        if self.isKeyPressed("Left") or self.isKeyPressed("a") or self.isKeyPressed("Right") or self.isKeyPressed("d"):
            transDst = moveSpeed * deltaTime * (-1 if self.isKeyPressed("Left") or self.isKeyPressed("a") else 1)
            self.setCameraPos(self.cameraPos + self.getCameraLeft() * transDst)
            hasMoved = True
        if self.isKeyPressed("e") or self.isKeyPressed("q"):
            rotAngle = rotSpeed * deltaTime * (1 if self.isKeyPressed("e") else -1)
            self.setCameraOrient(self.cameraOrient @ m3x3RotAxis(self.getCameraUp(), rotAngle))
            hasMoved = True
        return hasMoved
    
    def update(self, deltaTime):
        super().update(deltaTime)
