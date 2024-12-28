import math
from lib.canvas_object import CanvasObject

class CanvasObjectRectangle(CanvasObject):
    def __init__(self, pos, halfDims, angleDeg, color = "red", canvas = None, angVelDeg = 0):
        self.canvas = canvas
        self.pos = pos
        self.halfDims = halfDims
        self.angleDeg = angleDeg
        self.angVelDeg = float(angVelDeg)
        self.color = color
        if self.canvas != None:
            self.canvas.onCreated(self)
            
    def setCanvas(self, canvas):
        if self.canvas == None and canvas != None:
            canvas.onCreated(self)
        elif self.canvas != None and canvas == None:
            self.canvas.onDestroyed(self)
        self.canvas = canvas

    def destroy(self):
        super().destroy()
    
    def update(self, deltaTime):
        if self.angVelDeg != 0:
            self.angleDeg += self.angVelDeg * deltaTime

    def draw(self):
        self.canvas.drawRectOriented(self.pos, self.halfDims, self.angleDeg, self.color)
