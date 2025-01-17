import tkinter as tk
from lib.window import Window
from lib.window_3d import Window3D
from lib.winobj_sphere import Sphere
from lib.winobj_line import Line
from lib.winobj_tri3d import Tri3D
from lib.utils import *

class WindowPhysics3D(Window3D):
    def __init__(self, windowTitle = "Physics 3D!", setupLevelFn = None, updateLevelFn = None, cameraPos = v3_zero()):
        super().__init__(windowTitle, canvasColor = '#D7EAF4')

        self.setupLevelFn = setupLevelFn
        self.updateLevelFn = updateLevelFn
        self.initCameraPos = cameraPos
        
    def initApp(self):
        super().initApp()

        self.setCameraPos( self.initCameraPos )
        self.updateWorldGeo()
        
        if self.setupLevelFn != None:
            self.setupLevelFn(self)
        
    def updateWorldGeo(self):
        # todo
        pass
            
    def update(self, deltaTime):
        super().update(deltaTime)
        
        updateWorldGeo = False
        
        # user code level update
        if self.updateLevelFn != None:
            self.updateLevelFn(deltaTime)
            updateWorldGeo = True
        
        # camera
        if self.updateCamera(deltaTime):
            # camera has moved, need to update the geo positions
            updateWorldGeo = True
            
        # maybe retransform the world lines
        if updateWorldGeo:
            self.updateWorldGeo()