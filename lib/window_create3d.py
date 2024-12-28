import tkinter as tk
from lib.window import Window
from lib.window_3d import Window3D
from lib.winobj_sphere import Sphere
from lib.winobj_line import Line
from lib.utils import *

class WindowCreate3D(Window3D):
    def __init__(self, setupLevelFn = None, updateLevelFn = None, cameraPos = v3_zero()):
        super().__init__("Lab 12: Create 3D!")

        self.worldLines = [] # tuple (pt, pt, Line)
        self.setupLevelFn = setupLevelFn
        self.updateLevelFn = updateLevelFn
        self.initCameraPos = cameraPos
        self.modelToWorld = m4x4Identity()
        
    def initApp(self):
        super().initApp()

        self.setCameraPos( self.initCameraPos )
        self.updateWorldLines()
        
        if self.setupLevelFn != None:
            self.setupLevelFn(self.addLine)
        
    def addLine(self, ptA, ptB, color = "darkblue"):
        self.worldLines.append( (ptA, ptB, Line( self, ptA, ptB, color )) )
        self.updateWorldLines()
        
    def updateWorldLines(self):
        for worldLine in self.worldLines:
            ptA, ptB, line = worldLine[0], worldLine[1], worldLine[2]
            line.updateLinePositions( *self.transformAndClipLine(ptA, ptB, self.modelToWorld) )
            
    def update(self, deltaTime):
        super().update(deltaTime)
        
        updateWorldLines = False
        
        # user code level update
        if self.updateLevelFn != None:
            self.modelToWorld = self.updateLevelFn(deltaTime, self.modelToWorld)
            updateWorldLines = True
        
        # camera
        if self.updateCamera(deltaTime):
            # camera has moved, need to update the lines positions
            updateWorldLines = True
            
        # maybe retransform the world lines
        if updateWorldLines:
            self.updateWorldLines()