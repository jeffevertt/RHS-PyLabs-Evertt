import tkinter as tk
from lib.window import Window
from lib.winobj_link import *
from lib.utils import *
from lib.winobj_obb import OBB
from lib.winobj_wall import Wall

class WindowSimInvPend(Window):
    # consts
    GROUND_HEIGHT = -8
    ROD_HALFDIMS = v2(8, 0.3)
    ROD_INIT_ANGLE_MIN_MAX = (88.0, 92.0)
    ROD_DAMP = 0.9995
    PIVOT_DAMP = 0.95
    PIVOT_HALFDIMS = v2(1, 0.5)
    PIVOT_MIN_MAX_X = v2(-20,20)
    MASS_ROD_TO_PIVOT = 0.2
    KEYBOARD_THRUST = 100
    
    def __init__(self, title, subTitle, clickDoubleFn = None, calcPivotThrust = None):
        super().__init__(title, subTitle = subTitle, gridPixelsPerUnit = 24, clickDoubleFn = clickDoubleFn)
        
        self.calcPivotThrust = calcPivotThrust
        self.ground = None
        self.pivot = None
        self.rod = None
        
    def initApp(self):
        super().initApp()

        # kick off the simulation
        self.resetSimulation()
        
    def update(self, deltaTime):
        super().update(deltaTime)
        
        # level update
        self.updateLevel(deltaTime)
            
    def onMouseLeftPressed(self, event):
        super().onMouseLeftPressed(event)
    def onMouseLeftReleased(self, event):
        super().onMouseLeftReleased(event)
    def onMouseMotion(self, event):
        #mousePos = self.toCoordFrame(v2(event.x, event.y))
        # ...
        super().onMouseMotion(event)
    def onMouseLeftDoubleClick(self, event):
        self.resetSimulation()
        
    def resetSimulation(self, fullReset = True):
        # maybe destroy all objects & do initial scene setup
        if fullReset:
            self.sim.destroyAll()
            
            # create our objects
            self.ground = Wall(self, v2(0,WindowSimInvPend.GROUND_HEIGHT), v2(0,1))
            self.pivot = OBB(self, v2(0,0), WindowSimInvPend.PIVOT_HALFDIMS[0] * 2, WindowSimInvPend.PIVOT_HALFDIMS[1] * 2, color = "blue")
            self.rod = OBB(self, v2(0,0), WindowSimInvPend.ROD_HALFDIMS[0] * 2, WindowSimInvPend.ROD_HALFDIMS[1] * 2, color = "green")

        # reset objects
        self.pivot.pos, self.pivot.angle, self.pivot.vel, self.pivot.angVel = v2(0,WindowSimInvPend.GROUND_HEIGHT), 0.0, v2_zero(), 0.0
        rodAngle = randRange(WindowSimInvPend.ROD_INIT_ANGLE_MIN_MAX[0], WindowSimInvPend.ROD_INIT_ANGLE_MIN_MAX[1])
        self.rod.pos, self.rod.angle, self.rod.vel, self.rod.angVel = v2(0,WindowSimInvPend.GROUND_HEIGHT) + rotateVec2(v2_right(), rodAngle) * WindowSimInvPend.ROD_HALFDIMS[0], rodAngle, v2_zero(), 0.0
        
        # tell the simulation about it
        self.sim.update(0)
        
    def updateLevel(self, deltaTime, firstUpdate = False):
        # user update
        pivotThrust = 0
        if self.calcPivotThrust is not None:
            pivotThrust = self.calcPivotThrust(self.pivot.pos, self.rod.angle)
            
        # user keyboard input
        keyboardThrust = WindowSimInvPend.KEYBOARD_THRUST * (0.25 if self.isKeyPressed("Shift_L") or self.isKeyPressed("Shift_R") else 1)
        if self.isKeyPressed("Left") and self.pivot.pos[0] - 0.01 > WindowSimInvPend.PIVOT_MIN_MAX_X[0]:
            pivotThrust -= keyboardThrust
        if self.isKeyPressed("Right") and self.pivot.pos[0] + 0.01 < WindowSimInvPend.PIVOT_MIN_MAX_X[1]:
            pivotThrust += keyboardThrust
            
        # update the rod's angVel on pivot position & gravity
        rodAngAccel = (self.gravity[1] * (180 / math.pi) * cosDeg(self.rod.angle) + pivotThrust * sinDeg(self.rod.angle)) / WindowSimInvPend.ROD_HALFDIMS[0]
        
        # update the rod's angle based on the angAccel
        self.rod.angVel += rodAngAccel * deltaTime
        self.rod.angle += self.rod.angVel * deltaTime
        self.rod.angle = clamp(self.rod.angle, 0.0, 180.0)
        
        # the pivot gets pushed by the rod
        gravityTorque = (self.gravity[1] * (180 / math.pi)) * cosDeg(self.rod.angle)
        if self.rod.angle <= 0 or self.rod.angle >= 180: # if the rod hits the floor, stop it rotating
            self.rod.angVel = 0
        pivotAngAccel = (gravityTorque + pivotThrust * sinDeg(self.rod.angle)) / WindowSimInvPend.ROD_HALFDIMS[0]
        pushBackForce = (pivotAngAccel * sinDeg(self.rod.angle))
        self.pivot.vel -= v2_right() * pushBackForce * WindowSimInvPend.MASS_ROD_TO_PIVOT * deltaTime

        # update pivot based on thrust
        self.pivot.vel += v2_right() * pivotThrust * deltaTime
        self.pivot.pos += self.pivot.vel * deltaTime
                
        # damp
        self.pivot.vel *= WindowSimInvPend.PIVOT_DAMP
        self.rod.angVel *= WindowSimInvPend.ROD_DAMP
        
        # clamp pivot min/max
        self.pivot.pos[0] = clamp(self.pivot.pos[0], WindowSimInvPend.PIVOT_MIN_MAX_X[0], WindowSimInvPend.PIVOT_MIN_MAX_X[1])

        # update the rod's position based on the pivot and angle
        self.rod.pos = self.pivot.pos + WindowSimInvPend.ROD_HALFDIMS[0] * v2(cosDeg(self.rod.angle), sinDeg(self.rod.angle))
        
        # graphics update
        self.sim.updateGfxAllObjects()