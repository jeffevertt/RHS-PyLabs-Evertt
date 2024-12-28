import tkinter as tk
from PIL import Image as PILImage
from PIL import ImageTk
from lib.winobj import WinObj
from lib.utils import *

class Image(WinObj):
    def __init__(self, window, imagePath, pos, width, height, vel = v2(0,0), updateFn = None):
        super().__init__(window, pos, vel)
        self.window.sim.onCreated(self)
        self.updateFn = updateFn
        self.width = width
        self.height = height
        image = PILImage.open(imagePath)
        resizedImage = image.resize((int(self.window.toPixelsLength(width)), int(self.window.toPixelsLength(height))))
        self.image = ImageTk.PhotoImage(resizedImage)
        self.createGfx()
                
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def createGfx(self):
        self.gfxImage = self.window.canvas.create_image(self.window.toPixelsX(self.pos[0]), self.window.toPixelsY(self.pos[1]), image = self.image)
    def destroyGfx(self):
        if self.gfxImage != None:
            self.window.canvas.delete(self.gfxImage)
            self.gfxImage = None
    def updateGfx(self):
        if self.gfxImage != None:
            self.window.canvas.coords(self.gfxImage, self.window.toPixelsX(self.pos[0]), self.window.toPixelsY(self.pos[1]))
    
    def update(self, deltaTime):
        if self.updateFn != None:
            self.updateFn(self, deltaTime)
        self.updateGfx()
        super().update(deltaTime)
