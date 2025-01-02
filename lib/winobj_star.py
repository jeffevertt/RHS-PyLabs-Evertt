from lib.winobj import WinObj
from lib.utils import *

class Star(WinObj):
    POINT_SIZE_MIN = 0.02
    POINT_SIZE_MAX = 0.15
    POINT_SIZE_SCALE = 0.075
    DEFAULT_TRAIL_SPRING_K = 50.0
    FADE_IN_TIME = 0.15
    
    def __init__(self, window, pos, trailLenScalar = 1.0, color = "white"):
        super().__init__(window, pos)
        self.posPrevCamSpace = self.window.toCameraSpace_fromLastFrame(pos)
        self.trailLenScalar = trailLenScalar
        self.color = color
        self.timeSinceBorn = 0
        self.window.sim.onCreated(self)
        self.createGfx()
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def shouldBeCulled(self):
        return False if self.window.isPointInViewFrustum(self.pos) else True
        
    def createGfx(self):
        pos2d = self.window.worldTo2D(self.pos)
        rad2d = min(max(self.window.scaleAtPos(self.pos) * Star.POINT_SIZE_SCALE, Star.POINT_SIZE_MIN), Star.POINT_SIZE_MAX)
        self.gfxCircle = self.window.canvas.create_oval(self.window.toPixelsX(pos2d[0] - rad2d), self.window.toPixelsY(pos2d[1] - rad2d), 
                                                        self.window.toPixelsX(pos2d[0] + rad2d), self.window.toPixelsY(pos2d[1] + rad2d), 
                                                        fill = self.color if Star.FADE_IN_TIME == 0 else "#000000", width = 0)
        self.gfxLine = self.window.canvas.create_line(self.window.toPixelsX(pos2d[0]), self.window.toPixelsY(pos2d[1]), 
                                                      self.window.toPixelsX(pos2d[0]), self.window.toPixelsY(pos2d[1]), 
                                                      fill = self.color if Star.FADE_IN_TIME == 0 else "#000000", width = 1)
    def destroyGfx(self):
        if self.gfxCircle != None:
            self.window.canvas.delete(self.gfxCircle)
            self.gfxCircle = None
        if self.gfxLine != None:
            self.window.canvas.delete(self.gfxLine)
            self.gfxLine = None
    def updateGfx(self, fadeInPerc = None):
        if self.gfxCircle != None:
            pos2d = self.window.worldTo2D(self.pos)
            rad2d = min(max(self.window.scaleAtPos(self.pos) * Star.POINT_SIZE_SCALE, Star.POINT_SIZE_MIN), Star.POINT_SIZE_MAX)
            self.window.canvas.itemconfigure(self.gfxCircle, state = "normal" if self.window.isInFrontOfCamera(self.pos) else "hidden")
            self.window.canvas.coords(self.gfxCircle, self.window.toPixelsX(pos2d[0] - rad2d), self.window.toPixelsY(pos2d[1] - rad2d), 
                                                      self.window.toPixelsX(pos2d[0] + rad2d), self.window.toPixelsY(pos2d[1] + rad2d))
            # fade in support
            if fadeInPerc is not None:
                self.window.canvas.itemconfig(self.gfxCircle, fill = colorHexLerp("#000000", colorNamedToHex(self.color), fadeInPerc))
        if self.gfxLine != None:
            posPrev = self.window.toWorldSpaceFromCameraSpace(self.posPrevCamSpace)
            lineA, lineB = self.window.transformAndClipLine(self.pos, posPrev)
            if lineA is None or lineB is None:
                self.window.canvas.itemconfigure(self.gfxLine, state = "hidden")
            else:
                self.window.canvas.itemconfigure(self.gfxLine, state = "normal")
                self.window.canvas.coords(self.gfxLine, self.window.toPixelsX(lineA[0]), self.window.toPixelsY(lineA[1]), 
                                                        self.window.toPixelsX(lineB[0]), self.window.toPixelsY(lineB[1]))
                # fade in support
                if fadeInPerc is not None:
                    self.window.canvas.itemconfig(self.gfxLine, fill = colorHexLerp("#000000", colorNamedToHex(self.color), fadeInPerc))

        
    def trailPosition(self, trgPos, curPos, deltaTime, springK):
        delta = trgPos - curPos
        damping = 2 * math.sqrt(springK) # for critically damped spring
        velocity = delta * (damping / 2)
        return curPos + velocity * deltaTime
    
    def update(self, deltaTime):
        super().update(deltaTime)
        
        # time since born and fade in support
        prevTimeSinceBorn = self.timeSinceBorn
        self.timeSinceBorn += deltaTime
        fadeInPerc = None
        if Star.FADE_IN_TIME != 0 and prevTimeSinceBorn < Star.FADE_IN_TIME:
            fadeInPerc = min(self.timeSinceBorn / Star.FADE_IN_TIME, 1)
        
        # update posPrevCamSpace (this is a historical end position, which trails the current position)
        #  ...it is stored in camera space so that when the camera moves, you get a trail (camera burn/blur effect)
        posCamSpace = self.window.toCameraSpace(self.pos)
        self.posPrevCamSpace = self.trailPosition(posCamSpace, self.posPrevCamSpace, deltaTime, Star.DEFAULT_TRAIL_SPRING_K / self.trailLenScalar)

        # keep the gfx up to date (they are in 2d & due to the end point interp, changes pretty much every frame)
        self.updateGfx(fadeInPerc)
