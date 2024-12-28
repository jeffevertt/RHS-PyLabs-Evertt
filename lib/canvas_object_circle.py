from lib.canvas_object import CanvasObject

class CanvasObjectCircle(CanvasObject):
    def __init__(self, pos, radius, text = "", color = "red", canvas = None):
        self.canvas = canvas
        self.pos = pos
        self.radius = radius
        self.text = text
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
        pass

    def draw(self):
        if self.radius > 0:
            self.canvas.drawCircle(self.pos, self.radius, self.color)
        if len(self.text) > 0:
            self.canvas.drawText(self.pos, self.text, 'white')