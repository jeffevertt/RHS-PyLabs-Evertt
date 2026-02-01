from lib.winobj import WinObj
from lib.winobj_wall import Wall
from lib.utils import *

class Drone2D(WinObj):
    # consts
    MAX_THRUST_ANGLE        = 15.0  # in degress (plus or minus this value)
    MAX_THRUST_MAG          = 18    # from zero to this value
    MOMENT_OF_INERTIA       = 30.0
    DAMP_VEL_LINEAR         = 0.99
    DAMP_VEL_ANGULAR        = 0.96
    GFX_THRUST_VIS_MIN      = 2.0
    GFX_THRUST_VIS_SCALE    = 0.075
    
    def __init__(self, window, pos, width = 3.0, height = 1.0, angle = 0, vel = v2(0,0), ground:Wall = None, color = "blue", calcThrustFn = None):
        super().__init__(window, pos, vel)
        self.width = width
        self.height = height
        self.angle = angle
        self.angVel = 0
        self.color = color
        self.thrustAngle = 0    # local space, 0 indicates directly upwards (positive counter clockwise)
        self.thrustMag = 10     # force vector mag
        self.ground = ground
        self.window.sim.onCreated(self)
        self.calcThrustFn = calcThrustFn
        self.createGfx()
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
    def shouldBeCulled(self):
        return False
    
    def right(self):
        return rotateVec2(v2_right(), self.angle)
    def up(self):
        return rotateVec2(v2_up(), self.angle)
    def forward(self):          # aka up()
        return rotateVec2(v2_up(), self.angle)
    
    def setThrust(self, angle, mag):
        self.thrustAngle = clamp(angle, -Drone2D.MAX_THRUST_ANGLE, Drone2D.MAX_THRUST_ANGLE)
        self.thrustMag = clamp(mag, 0, Drone2D.MAX_THRUST_MAG)
    def thrustVec(self):
        return rotateVec2(v2_up(), self.angle + self.thrustAngle) * self.thrustMag
    def thrustDirVec_Forward(self):
        return rotateVec2(v2_up(), self.angle + self.thrustAngle)
    def thrustDirVec_Right(self):
        return rotateVec2(v2_right(), self.angle + self.thrustAngle)
        
    def createGfx(self):
        self.gfxThrust = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0) ], fill = 'gold', outline = 'crimson', width = 5)
        self.gfxBody = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0) ], fill = self.color, outline = 'black', width = 3)
        self.updateGfx()
    def destroyGfx(self):
        if self.gfxBody != None:
            self.window.canvas.delete(self.gfxBody)
            self.gfxBody = None
        if self.gfxThrust != None:
            self.window.canvas.delete(self.gfxThrust)
            self.gfxThrust = None
    def updateGfx(self):
        if self.gfxBody != None:
            p0 = self.window.toPixels( self.pos + self.right() * (self.width/2) - self.up() * (self.height/2) )
            p1 = self.window.toPixels( self.pos - self.right() * (self.width/2) - self.up() * (self.height/2) )
            p2 = self.window.toPixels( self.pos + self.up() * (self.height/2) )
            self.window.canvas.coords( self.gfxBody, [ (p0[0], p0[1]), (p2[0], p2[1]), (p1[0], p1[1]) ] )
        if self.gfxThrust != None:
            thrustVecForVis = self.thrustVec()
            thrustVecLen = length(thrustVecForVis)
            if thrustVecLen > 0.01:
                thrustVecForVis *= (thrustVecLen + Drone2D.GFX_THRUST_VIS_SCALE) / thrustVecLen
            p0 = self.window.toPixels( self.pos + self.right() * (self.width/2 * 0.35) - self.up() * (self.height/2) )
            p1 = self.window.toPixels( self.pos - self.right() * (self.width/2 * 0.35) - self.up() * (self.height/2) )
            p2 = self.window.toPixels( self.pos - self.up() * (self.height/2) - thrustVecForVis * self.height * Drone2D.GFX_THRUST_VIS_SCALE * randRange(0.8, 1.2) )
            self.window.canvas.coords( self.gfxThrust, [ (p0[0], p0[1]), (p2[0], p2[1]), (p1[0], p1[1]) ] )
                        
    def update(self, deltaTime):
        if self.calcThrustFn != None:
            targetPos = self.window.lastMousePos[0] if self.window.lastMousePos is not None else v2_zero()
            (thrustAngle, thrustMag) = self.calcThrustFn(self, targetPos, deltaTime)
            if isinstance(thrustAngle, (int, float)) and isinstance(thrustMag, (int, float)):
                self.setThrust(thrustAngle, thrustMag)
            # update thrust & motion
            self.vel += (self.thrustVec() + self.window.gravity) * deltaTime
            self.angVel += self.thrustAngle * Drone2D.MOMENT_OF_INERTIA * deltaTime
            self.angle += self.angVel * deltaTime
            self.pos += self.vel * deltaTime
            if self.ground != None:
                # collision (model with two circles)
                colCircleRad = self.height/2
                colCenters = (self.pos + self.right() * self.width/4, self.pos - self.right() * self.width/4)
                hitGround = False
                for colCenter in colCenters:
                    dst = dot(colCenter - self.ground.pos, self.ground.normal) - colCircleRad
                    if dst < 0.0:
                        colCenter += self.ground.normal * -dst
                        hitGround = True
                if hitGround:
                    newRight = unit(colCenters[0] - colCenters[1])
                    self.angle = atan2Deg(newRight[1], newRight[0])
                    self.pos = (colCenters[0] + colCenters[1]) / 2
                    restitution = 1.35
                    self.vel = self.vel - dot(self.vel, self.ground.normal) * self.ground.normal * restitution
                    self.angVel *= 0.85
            # damp
            self.vel *= Drone2D.DAMP_VEL_LINEAR
            self.angVel *= Drone2D.DAMP_VEL_ANGULAR
            # gfx update
            self.updateGfx()
        super().update(deltaTime)
