import tkinter as tk
from lib.window import Window
from lib.window_3d import Window3D
from lib.winobj_sphere import Sphere
from lib.winobj_line import Line
from lib.winobj_tri3d import Tri3D
from lib.utils import *

class WindowCreate3D(Window3D):
    def __init__(self, windowTitle = "Create 3D!", setupLevelFn = None, updateLevelFn = None, cameraPos = v3_zero()):
        super().__init__(windowTitle)

        self.worldLines = [] # tuple (pt, pt, Line)
        self.worldTris = []  # tuple (pt, pt, pt, Tri3D)
        self.setupLevelFn = setupLevelFn
        self.updateLevelFn = updateLevelFn
        self.initCameraPos = cameraPos
        self.modelToWorld = m4x4Identity()
        
    def initApp(self):
        super().initApp()

        self.setCameraPos( self.initCameraPos )
        self.updateWorldGeo()
        
        if self.setupLevelFn != None:
            self.setupLevelFn(self.addLine, self.addTri)
        
    def addLine(self, ptA, ptB, color = "darkblue"):
        self.worldLines.append( (ptA, ptB, Line( self, ptA, ptB, color )) )
        self.updateWorldGeo()
        
    def addTri(self, ptA, ptB, ptC, color = "darkgreen"):
        self.worldTris.append( (ptA, ptB, ptC, Tri3D( self, ptA, ptB, ptC, color )) )
        self.updateWorldGeo()        
        
    def updateWorldGeo(self):
        for worldLine in self.worldLines:
            ptA, ptB, line = worldLine[0], worldLine[1], worldLine[2]
            line.updateLinePositions( *self.transformAndClipLine(ptA, ptB, self.modelToWorld) )
        for worldTri in self.worldTris:
            ptA, ptB, ptC, tri = worldTri[0], worldTri[1], worldTri[2], worldTri[3]
            tri.updateTriPositions( ptA, ptB, ptC ) # tri3d's positions are world space (they don't support a model transform, at least for now)
            
    def update(self, deltaTime):
        super().update(deltaTime)
        
        updateWorldGeo = False
        
        # user code level update
        if self.updateLevelFn != None:
            self.modelToWorld = self.updateLevelFn(deltaTime, self.modelToWorld)
            updateWorldGeo = True
        
        # camera
        if self.updateCamera(deltaTime):
            # camera has moved, need to update the geo positions
            updateWorldGeo = True
            
        # maybe retransform the world lines
        if updateWorldGeo:
            self.updateWorldGeo()