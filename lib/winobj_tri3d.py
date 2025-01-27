from lib.winobj import WinObj
from lib.utils import *
from lib.utils_clipping import *

class Tri3D(WinObj):
    def __init__(self, window, posA, posB, posC, color = "blue"): #todo: add cull(true/false: true CCW)
        self.posA = posA
        self.posB = posB
        self.posC = posC
        centroid = (posA + posB + posC) / 3
        super().__init__(window, centroid)
        self.color = color
        self.window.sim.onCreated(self)
        self.createGfx()
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def shouldBeCulled(self):
        # don't do auto-culling of tris
        return False
        
    def createGfx(self):
        self.gfxTri = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0) ], fill = self.color, outline = '')
        self.updateGfx()
    def destroyGfx(self):
        if self.gfxTri != None:
            self.window.canvas.delete(self.gfxTri)
            self.gfxTri = None
    def updateGfx(self):
        poly2d = None

        # transform from 3D world space to clip space, then to NDC space
        toClipSpace = self.window.transProj @ self.window.transCamera
        posA = toClipSpace @ v4(self.posA)
        posB = toClipSpace @ v4(self.posB)
        posC = toClipSpace @ v4(self.posC)

        # to NDC, then clip vs near plane
        posA /= (posA[3] if posA[3] != 0 else 0.0000001)
        posB /= (posB[3] if posB[3] != 0 else 0.0000001)
        posC /= (posC[3] if posC[3] != 0 else 0.0000001)

        # clip to near clip plane
        poly = clipTriAgainstNearPlaneNDC(posA, posB, posC)
        
        # first, do backface cull
        if poly is None or len(poly) < 3 or isBackfaceCulledNDC(poly):
            poly2d = None
        else:
            # convert to screen space
            poly2d = [] if poly is not None else None
            if poly2d is not None:
                # from NDC to pixel space (with inverted y)
                for vert in poly:
                    poly2d.append( (self.window.toPixelsX(vert[0] * self.window.maxCoordinateX()), self.window.toPixelsY(vert[1] * -self.window.maxCoordinateY())) )

                # finally, clip to screen space
                poly2d = clipPolyScreenSpace(poly2d, self.window.width, self.window.height)

        # update the tris
        if self.gfxTri != None:
            if poly2d is None or len(poly2d) < 3:
                self.window.canvas.itemconfigure(self.gfxTri, state = "hidden")
            else:
                self.window.canvas.itemconfigure(self.gfxTri, state = "normal", fill = self.color)
                self.window.canvas.coords(self.gfxTri, poly2d)
    
    def updateTriPositions(self, posA, posB, posC):
        self.posA = v3_from_v4(posA)
        self.posB = v3_from_v4(posB)
        self.posC = v3_from_v4(posC)
        self.updateGfx()
    def calcColorFromCamLighting(self, colorDiffuseHex, minColor = "#222222"):
        faceNormal = unit( cross(self.posB - self.posA, self.posC - self.posA) )
        brightness = max(dot(self.window.getCameraForward(), -faceNormal), 0.2)
        self.color = colorHexLerp( minColor, colorDiffuseHex, brightness )
        self.updateGfx()
    
    def update(self, deltaTime):
        super().update(deltaTime)
