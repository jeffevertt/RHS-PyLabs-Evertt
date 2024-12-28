from lib.winobj import WinObj
from lib.utils import *
import math

class Wall(WinObj):
    def __init__(self, window, pos, normal, color = "darkslategray"):
        super().__init__(window, pos, v2(0,0))
        self.normal = unit( v2(normal[0], normal[1]) )
        self.dir = v2(-self.normal[1], self.normal[0]) if self.normal[0] > 0 else v2(self.normal[1], -self.normal[0])
        self.angle = posAngleDeg( math.degrees(math.atan2(normal[1], normal[0])) )
        self.color = color
        self.window.sim.onCreated(self)
        self.createGfx()
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
      
    def polygonFromClippedRectangle(self, rectUL, rectLR, point, dirUnit, normUnit):
        # Setup rect...
        rectCorners = [v2(rectUL[0], rectUL[1]),
                       v2(rectLR[0], rectUL[1]),
                       v2(rectLR[0], rectLR[1]),
                       v2(rectUL[0], rectLR[1]) ]
        rectULr = rectCorners[1] - rectUL # UL-Right (not normalized)
        rectULd = rectCorners[3] - rectUL # UL-Down  (not normalized)
        rectLRl = rectCorners[3] - rectLR # LR-Left  (not normalized)
        rectLRu = rectCorners[1] - rectLR # LR-Down  (not normalized)

        # Intersect ray with edges of rectangle...
        segDir = dirUnit * 2000
        segStart = point - segDir * 0.5
        pts = [ intersectSegments(segStart, segDir, rectUL, rectULr), 
                intersectSegments(segStart, segDir, rectLR, rectLRu),
                intersectSegments(segStart, segDir, rectLR, rectLRl),
                intersectSegments(segStart, segDir, rectUL, rectULd) ]
        
        # Loop over the points, building the polygon...
        poly = []
        firstIntersection = None
        firstIntersectionIdx = None
        for i, pt in enumerate(pts):
            if pt is None:
                continue
            if firstIntersection is None:
                # First intersection...
                firstIntersectionIdx = i
                firstIntersection = pt
            else:
                # Figure out our first corner to fill...
                firstCornerIdx = (firstIntersectionIdx + 1) if (distancePointToPlane(rectCorners[firstIntersectionIdx + 1], point, normUnit) < 0) else (i + 1)

                # Now, walk the corners...
                for j in range(firstCornerIdx, firstCornerIdx + 4):
                    cornerIdx = j % 4
                    dst = distancePointToPlane(rectCorners[cornerIdx], point, normUnit)
                    if dst < 0:
                        if len(poly) == 0:
                            if firstCornerIdx == (firstIntersectionIdx + 1):
                                poly.append( self.window.toPixels(firstIntersection) )
                                firstIntersection = None
                            else:
                                poly.append( self.window.toPixels(pt) )
                        poly.append( self.window.toPixels(rectCorners[cornerIdx]) )
                if firstIntersection is not None:
                    poly.append( self.window.toPixels(firstIntersection) )
                    firstIntersection = None
                else:
                    poly.append( self.window.toPixels(pt) )
                break
        return poly
        
    def createGfx(self):
        poly = self.polygonFromClippedRectangle(self.window.coordUL(), self.window.coordLR(), self.pos, self.dir, self.normal)
        polyFlat =  [item for pair in poly for item in pair]
        self.gfxPoly = self.window.canvas.create_polygon(polyFlat, fill = self.color, outline = "black", width = 3)
    def destroyGfx(self):
        if self.gfxPoly != None:
            self.window.canvas.delete(self.gfxPoly)
            self.gfxPoly = None
            
    def drawOrderToBack(self):
        if self.gfxPoly != None:
            self.window.canvas.lower(self.gfxPoly)
    
    def update(self, deltaTime):
        super().update(deltaTime)
