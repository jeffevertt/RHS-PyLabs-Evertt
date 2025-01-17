from lib.winobj import WinObj
from lib.winobj_tri3d import Tri3D
from lib.winobj_line import Line
from lib.winobj_plane import Plane
from lib.utils import *

class Cuboid(WinObj):
    def __init__(self, window, pos, halfDims, mass = 100, vel = v3_zero(), velAng = v3_zero(), orient = m3x3Identity(), color = "darkseagreen"):
        super().__init__(window, pos, vel = vel)
        self.halfDims = halfDims
        self.orient = orient
        self.color = color
        self.window.sim.onCreated(self)
        
        # physics
        self.mass = mass
        self.inertiaTensor = self.calcInertiaTensor()
        self.velAng = velAng    # radians per second
        self.collisionPlane = None

        # geo        
        self.tris = []
        self.lines = []
        self.createGeo()
            
    def destroy(self):
        super().destroy()
        
    def shouldBeCulled(self):
        # don't do auto-culling
        return False
    
    def basisX(self):
        return self.orient[0, :]
    def basisY(self):
        return self.orient[1, :]
    def basisZ(self):
        return self.orient[2, :]
    def modelToWorld(self):
        return m4x4ModelToWorld(self.orient, self.pos)
    
    def calcInertiaTensor(self):
        fullDims = self.halfDims * 2
        return m3x3Diag( v3(1/12.0 * self.mass * (fullDims[1]**2 + fullDims[2]**2),
                            1/12.0 * self.mass * (fullDims[0]**2 + fullDims[2]**2),
                            1/12.0 * self.mass * (fullDims[0]**2 + fullDims[1]**2)) )
    def calcSkewSymMatrix(self): # this is basically the angular veocity, in matrix form
        return np.array([[              0, -self.velAng[2],  self.velAng[1]],
                         [ self.velAng[2],               0, -self.velAng[0]],
                         [-self.velAng[1],  self.velAng[0],              0]])
    def setCollisionPlane(self, plane: Plane):
        self.collisionPlane = plane
    
    def calcVerts_modelSpace(self):
        return [ v3( self.halfDims[0], -self.halfDims[1], -self.halfDims[2]),
                 v3( self.halfDims[0], -self.halfDims[1],  self.halfDims[2]),
                 v3(-self.halfDims[0], -self.halfDims[1],  self.halfDims[2]),
                 v3(-self.halfDims[0], -self.halfDims[1], -self.halfDims[2]),
                 v3( self.halfDims[0],  self.halfDims[1], -self.halfDims[2]),
                 v3( self.halfDims[0],  self.halfDims[1],  self.halfDims[2]),
                 v3(-self.halfDims[0],  self.halfDims[1],  self.halfDims[2]),
                 v3(-self.halfDims[0],  self.halfDims[1], -self.halfDims[2]) ]
    def calcVerts_worldSpace(self):
        verts = self.calcVerts_modelSpace()
        modelToWorld = self.modelToWorld()
        for i, vert in enumerate(verts):
            verts[i] = v3_from_v4( modelToWorld @ v4(vert) )
        return verts
    
    def createGeo(self):
        verts = self.calcVerts_modelSpace()
        
        self.tris.append( (Tri3D(self.window, verts[0], verts[1], verts[2], self.color),0,1,2) ) # bottom
        self.tris.append( (Tri3D(self.window, verts[0], verts[2], verts[3], self.color),0,2,3) )
        
        self.tris.append( (Tri3D(self.window, verts[6], verts[5], verts[4], self.color),6,5,4) ) # top
        self.tris.append( (Tri3D(self.window, verts[7], verts[6], verts[4], self.color),7,6,4) )

        self.tris.append( (Tri3D(self.window, verts[7], verts[4], verts[0], self.color),7,4,0) ) # front
        self.tris.append( (Tri3D(self.window, verts[7], verts[0], verts[3], self.color),7,0,3) )

        self.tris.append( (Tri3D(self.window, verts[1], verts[5], verts[6], self.color),1,5,6) ) # back
        self.tris.append( (Tri3D(self.window, verts[1], verts[6], verts[2], self.color),1,6,2) )

        self.tris.append( (Tri3D(self.window, verts[6], verts[7], verts[3], self.color),6,7,3) ) # right
        self.tris.append( (Tri3D(self.window, verts[6], verts[3], verts[2], self.color),6,3,2) )

        self.tris.append( (Tri3D(self.window, verts[4], verts[5], verts[1], self.color),4,5,1) ) # left
        self.tris.append( (Tri3D(self.window, verts[4], verts[1], verts[0], self.color),4,1,0) )
        
        self.lines.append( (Line(self.window, verts[0], verts[1], "black"),0,1) ) # bottom
        self.lines.append( (Line(self.window, verts[1], verts[2], "black"),1,2) )
        self.lines.append( (Line(self.window, verts[2], verts[3], "black"),2,3) )
        self.lines.append( (Line(self.window, verts[3], verts[0], "black"),3,0) )
        
        self.lines.append( (Line(self.window, verts[4], verts[5], "black"),4,5) ) # top
        self.lines.append( (Line(self.window, verts[5], verts[6], "black"),5,6) )
        self.lines.append( (Line(self.window, verts[6], verts[7], "black"),6,7) )
        self.lines.append( (Line(self.window, verts[7], verts[4], "black"),7,4) )

        self.lines.append( (Line(self.window, verts[0], verts[4], "black"),0,4) ) # vert sides
        self.lines.append( (Line(self.window, verts[1], verts[5], "black"),1,5) )
        self.lines.append( (Line(self.window, verts[2], verts[6], "black"),2,6) )
        self.lines.append( (Line(self.window, verts[3], verts[7], "black"),3,7) )
        
    def updateGeo(self):
        # called when one of the transforms changed (like the camera) or pos change...update 3d -> 2d (pass on to tris & lines)
        verts = self.calcVerts_modelSpace()
        modelToWorld = self.modelToWorld()
        for tri in self.tris:
            tri[0].updateTriPositions( modelToWorld @ v4(verts[tri[1]]), modelToWorld @ v4(verts[tri[2]]), modelToWorld @ v4(verts[tri[3]]) )
        for line in self.lines:
            line[0].updateLinePositions( *self.window.transformAndClipLine(verts[line[1]], verts[line[2]], modelToWorld) )
    
    def applyTorque(self, force, atPt, deltaTime):
        # figure out the torque when the force is applied at the specified point
        r = atPt - self.pos
        torque = cross(r, force)
        modelToWorld = self.modelToWorld()
        
        # angular acceleration is torque transformed by the inverse of the world space inertia tensor
        inertiaTensorWorldSpace = self.orient @ self.inertiaTensor @ m3x3Transpose(self.orient)
        accAng = m3x3Inverse(inertiaTensorWorldSpace) @ torque
        self.velAng += accAng # * deltaTime
    def updateCollisionWithPlane(self, plane :Plane, deltaTime):
        # setup
        planePos = plane.pos
        planeNormal = plane.basisY()

        # verts in WS
        verts = self.calcVerts_worldSpace()
        
        # per vert distance & response
        maxPen = 0
        for vert in verts:
            dst = dot(vert - planePos, planeNormal)
            if dst >= 0:
                continue
            
            # figure how far we need to push it out
            maxPen = max(maxPen, -dst)
            
            # Calculate relative velocity at contact point
            relVel = self.vel + cross(self.velAng, vert - self.pos)

            # Calculate normal impulse
            restitution = 0.5
            impulse = -(1 + restitution) * dot(relVel, plane.normal) * plane.normal 

            # apply torque at the point
            self.applyTorque(impulse, vert, deltaTime)

        # push it out along the plane normal
        self.pos += planeNormal * maxPen

    def updatePhysics(self, deltaTime):
        # linear motion
        self.vel += self.window.gravity * deltaTime
        self.pos += self.vel * deltaTime
        
        # angular motion
        skewSymMatrix = self.calcSkewSymMatrix()
        dRdt = skewSymMatrix @ self.orient
        self.orient += dRdt * deltaTime
        
        # maintain ortho-normal orient (errors can accumulate)
        self.orient = m3x3OrthoNormalize(self.orient)
        
        # collision (with plane)
        if self.collisionPlane is not None:
            self.updateCollisionWithPlane(self.collisionPlane, deltaTime)
        
        return True # indicate that we need to update geo
    
    def update(self, deltaTime):
        super().update(deltaTime)
        
        # physic update
        if self.updatePhysics(deltaTime):
            self.updateGeo()
