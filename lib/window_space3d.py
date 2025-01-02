from lib.window_3d import Window3D
from lib.winobj_star import Star
from lib.utils import *

class WindowSpace3D(Window3D):
    def __init__(self, windowTitle, spawnStarsFn, updateCameraFn, cameraPos = v3_zero()):
        super().__init__(windowTitle, canvasColor = '#000000')

        self.spawnStarsFn = spawnStarsFn
        self.updateCameraFn = updateCameraFn
        self.initCameraPos = cameraPos
        
    def initApp(self):
        super().initApp()

        self.setCameraPos( self.initCameraPos )
        
        self.update(0)
        
    def toCameraSpace_fromLastFrame(self, pos):
        posCamSpace = self.transCamera_fromLastFrame @ v4(pos)
        return v3_from_v4(posCamSpace)

    def update(self, deltaTime):
        super().update(deltaTime)
        
        # update camera            
        if self.updateCameraFn != None:
            wasdBtns = [ self.isKeyPressed('w'), self.isKeyPressed('a'), self.isKeyPressed('s'), self.isKeyPressed('d') ]
            shiftCtrlBtns = [ self.isKeyPressed('Shift_L') or self.isKeyPressed('Shift_R'), self.isKeyPressed('Control_L') or self.isKeyPressed('Control_R') ]
            self.transCamera_fromLastFrame = self.transCamera.copy()
            self.updateCameraFn( self, wasdBtns, shiftCtrlBtns, deltaTime )
            
        # spawn stars
        if self.spawnStarsFn != None:
            numStars = self.sim.countObjectsOfType(Star)
            self.spawnStarsFn( self, numStars )
