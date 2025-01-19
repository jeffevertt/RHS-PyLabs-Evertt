import numpy as np
from lib.utils import *

# Cohen-Sutherland algorithm (points in normalized device coordinates, -1 to 1)
def clipLineAgainstNearPlaneNDC(p1, p2):
    def outcode(p):
        code = 0
        if p[2] < -1 or p[2] > 1:
            code |= 1
        return code
    x1, y1, z1 = p1[0], p1[1], p1[2]
    x2, y2, z2 = p2[0], p2[1], p2[2]
    outcode1 = outcode(p1)
    outcode2 = outcode(p2)
    while True:
        if (outcode1 | outcode2) == 0:
            # both endpoints are inside the clipping region
            return p1, p2
        elif (outcode1 & outcode2) != 0:
            # both endpoints are outside the clipping region on the same side
            return None, None
        # at least one endpoint is outside the clipping region
        outcode_out = outcode1 if outcode1 else outcode2
        if outcode_out & 1:  # Behind near plane
            x = x1 + (x2 - x1) * (-1 - z1) / (z2 - z1)
            y = y1 + (y2 - y1) * (-1 - z1) / (z2 - z1)
            z = -1
            if outcode_out == outcode1:
                p1 = v3(x, y, z)
                outcode1 = outcode(p1)
            else:
                p2 = v3(x, y, z)
                outcode2 = outcode(p2)

# checks tri winding order (assumes right handed coordinate system, points in clip space)
def isTriWindingCCW(p1, p2, p3):
    # need to do the perspective divide before checking facing
    ndc1 = p1 / (p1[3] if p1[3] != 0 else 0.0000001)
    ndc2 = p2 / (p2[3] if p2[3] != 0 else 0.0000001)
    ndc3 = p3 / (p3[3] if p3[3] != 0 else 0.0000001)
    
    # get the tri normal and compare to camera fwd (which is always [0,0,1] in cam, clip, & NDC space)
    perp = cross(v3_from_v4(ndc2 - ndc1), v3_from_v4(ndc3 - ndc1))
    return perp[2] > 0 # this is effectively a dot with the camera vector

# Sutherland-Hodgman clipping algorithm
#  verts should be in clip space (i.e. like NDC, but before the perspective divide)
#  clips against all 6 planes in NDC, returns a polygon.
#  returns a single polygon (or None in the case of fully clipped)
def clipTri(p1, p2, p3):
    # clip plane (constants)
    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8
    NEAR = 16
    FAR = 32
    
    # clip against a single clip plane, returns clipped polygon (list of verts)
    def clipAgainstPlane(vertices, plane):
        outVerts = []
        if len(vertices) == 0:
            return outVerts
        S = vertices[-1]
        for V in vertices:
            if inside(V, plane):
                if not inside(S, plane):
                    I = intersect(S, V, plane)
                    outVerts.append(I)
                outVerts.append(V)
            elif inside(S, plane):
                I = intersect(S, V, plane)
                outVerts.append(I)
            S = V
        return outVerts

    # returns True/False for inside/outside of plane
    def inside(v, plane):
        x, y, z, w = v
        if plane == LEFT:
            return x >= -w
        elif plane == RIGHT:
            return x <= w
        elif plane == BOTTOM:
            return y >= -w
        elif plane == TOP:
            return y <= w
        elif plane == NEAR:
            return z >= -w
        elif plane == FAR:
            return z <= w

    # calc intersect point of line segment and the given plane, returns point
    def intersect(v1, v2, plane):
        x1, y1, z1, w1 = v1
        x2, y2, z2, w2 = v2
        if plane == LEFT:
            t = (-w1 - x1) / ((x2 - x1) - (w2 - w1)) 
        elif plane == RIGHT:
            t = (w1 - x1) / ((x2 - x1) - (w2 - w1))
        elif plane == BOTTOM:
            t = (-w1 - y1) / ((y2 - y1) - (w2 - w1))
        elif plane == TOP:
            t = (w1 - y1) / ((y2 - y1) - (w2 - w1))
        elif plane == NEAR:
            t = (-w1 - z1) / ((z2 - z1) - (w2 - w1))
        elif plane == FAR:
            t = (w1 - z1) / ((z2 - z1) - (w2 - w1))
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        z = z1 + t * (z2 - z1)
        w = w1 + t * (w2 - w1)
        return v4(x, y, z, w)

    # list (and order) of clipping planes
    planes = [LEFT, RIGHT, BOTTOM, TOP, NEAR, FAR]
    outVerts = [p1, p2, p3]
    
    # our clip space is inverted left <-> right & near <-> far
    for vert in outVerts:
        vert[0] *= -1
        #vert[2] *= -1
        vert[3] *= -1

    # clip against planes
    for plane in planes:
        outVerts = clipAgainstPlane(outVerts, plane)

    # if the triangle is completely clipped away, return an empty list
    if len(outVerts) < 3:
        return None

    # our clip space is inverted left <-> right & near <-> far
    for vert in outVerts:
        vert[0] *= -1
        #vert[2] *= -1
        vert[3] *= -1

    return outVerts
