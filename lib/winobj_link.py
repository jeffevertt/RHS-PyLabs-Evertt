from lib.winobj import WinObj
from lib.utils import *

class Link(WinObj):
    def __init__(self, window, pos, angle = -90, length = 3, width = 0.5, radius = 0.5, parent = None, child = None, color = "blue"):
        super().__init__(window, pos, v2(0,0))
        self.dirVec = rotateVec2( v2(1, 0), angle )
        self.color = color
        self.width = width
        self.length = length
        self.radius = radius
        self.parent = None
        self.child = None
        self.prevPos = None # if using verlet integration
        self.setParent(parent)
        self.setChild(child)
        self.window.sim.onCreated(self)
        self.createGfx()
            
    def destroy(self):
        self.destroyGfx()
        super().destroy()
        
    def setParent(self, parent):
        self.parent = parent
        if self.parent is not None and parent.child != self:
            self.parent.setChild(self)
    def setChild(self, child):
        self.child = child
        if self.child is not None and child.parent != self:
            self.child.setParent(self)
        self.updateDirVec()
    
    def translate(self, deltaVec):
        self.pos += deltaVec
    def updateDirVec(self): # based on the child node position
        if self.child is not None:
            self.dirVec = unit(self.child.pos - self.pos)
    def updatePrevPos(self):
        if self.prevPos is not None:
            self.prevPos = self.pos

    def posStart(self):
        return self.pos
    def posEnd(self):
        return self.pos + self.dirVec * self.length
    def posEndGfx(self):
        gfxLength = self.length
        if self.child is not None:
            gfxLength = length(self.pos - self.child.pos)
        return self.pos + self.dirVec * gfxLength
    def forward(self):
        return self.dirVec
    def right(self):
        return v2(-self.dirVec[1], self.dirVec[0])
        
    def createGfx(self):
        endPos = self.posEnd()
        self.gfxTri = self.window.canvas.create_polygon([ (0, 0), (0, 0), (0, 0) ], fill = 'orange', outline = 'black', width = 3)
        self.gfxCircle = self.window.canvas.create_oval(self.window.toPixelsX(endPos[0] - self.radius), self.window.toPixelsY(endPos[1] - self.radius), 
                                                        self.window.toPixelsX(endPos[0] + self.radius), self.window.toPixelsY(endPos[1] + self.radius), 
                                                        fill = self.color, outline = "black", width = 2)
        self.updateGfx()
    def destroyGfx(self):
        if self.gfxTri != None:
            self.window.canvas.delete(self.gfxTri)
            self.gfxTri = None
        if self.gfxCircle != None:
            self.window.canvas.delete(self.gfxCircle)
            self.gfxCircle = None
    def updateGfx(self):
        # if tail node, no graphics to draw
        hideGfx = True if self.child is None else False        
        if self.gfxTri != None:
            p0 = self.window.toPixels( self.pos + self.right() * (self.width/2) )
            p1 = self.window.toPixels( self.pos - self.right() * (self.width/2) )
            p2 = self.window.toPixels( self.posEndGfx() )
            self.window.canvas.coords( self.gfxTri, [ (p0[0], p0[1]), (p2[0], p2[1]), (p1[0], p1[1]) ] )
            self.window.canvas.itemconfigure( self.gfxTri, state = 'hidden' if hideGfx else 'normal' )
        if self.gfxCircle != None:
            startPos = self.posStart()
            self.window.canvas.coords(self.gfxCircle, self.window.toPixelsX(startPos[0] - self.radius), self.window.toPixelsY(startPos[1] - self.radius), 
                                                      self.window.toPixelsX(startPos[0] + self.radius), self.window.toPixelsY(startPos[1] + self.radius))
            self.window.canvas.tag_raise(self.gfxCircle)
            
    def calcConstrainedPos(self):
        if self.child is None:
            # no child case, just a singular constraint (keep direction vector, just inforce length constraint, no solve required)
            pos = self.parent.pos + self.parent.forward() * self.parent.length
        else:
            #  equation is possible solutions given the length constrains for self.pos given parent and child positions
            dstParentChild = length(self.parent.pos - self.child.pos)
            if dstParentChild >= (self.parent.length + self.length):
                # two sln circles do not intersect, no sln, lock back to parent's circle
                parentToChildUnit = (self.child.pos - self.parent.pos) / dstParentChild
                pos = self.parent.pos + parentToChildUnit * self.parent.length
            else:
                # two sln circles intersect, so two slns (found using perpendicular bisector of parent -> child, then solving for right tri height)
                a = (self.parent.length * self.parent.length - self.length * self.length + dstParentChild * dstParentChild) / (2 * dstParentChild)
                h = math.sqrt(max(self.parent.length * self.parent.length - a * a, 0))
                pos0 = v2(self.parent.pos[0] + a * (self.child.pos[0] - self.parent.pos[0]) / dstParentChild + h * (self.child.pos[1] - self.parent.pos[1]) / dstParentChild,
                          self.parent.pos[1] + a * (self.child.pos[1] - self.parent.pos[1]) / dstParentChild - h * (self.child.pos[0] - self.parent.pos[0]) / dstParentChild)
                pos1 = v2(self.parent.pos[0] + a * (self.child.pos[0] - self.parent.pos[0]) / dstParentChild - h * (self.child.pos[1] - self.parent.pos[1]) / dstParentChild,
                          self.parent.pos[1] + a * (self.child.pos[1] - self.parent.pos[1]) / dstParentChild + h * (self.child.pos[0] - self.parent.pos[0]) / dstParentChild)
                pos = pos0 if lengthSqr(pos0 - self.pos) < lengthSqr(pos1 - self.pos) else pos1
        return pos
            
    def update(self, deltaTime):
        super().update(deltaTime)
