import numpy as np
import math
from lib.utils import *

def clipLineAgainstNearPlaneNDC(p1, p2):
    # Cohen-Sutherland algorithm (points in normalized device coordinates, -1 to 1)
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
def clipTriAgainstNearPlaneNDC(p1, p2, p3):
    # returns one or two triangles (each an array of three points...or None)
    p1a, p2a = clipLineAgainstNearPlaneNDC(p1, p2)
    p1b, p3b = clipLineAgainstNearPlaneNDC(p1, p3)
    p2c, p3c = clipLineAgainstNearPlaneNDC(p2, p3)
    if p1a is None and p1b is None:                                     # fully clipped
        return None
    elif vecEqual(p1a, p1) and vecEqual(p2a, p2) and vecEqual(p3b, p3): # no clipping
        return [ p1, p2, p3 ]
    elif p1a is None and p2a is None:                                   # single triangle cases
        return [ p1b, p2c, p3 ]
    elif p1b is None and p3b is None:
        return [ p3c, p1a, p2 ]
    elif p2c is None and p3c is None:
        return [ p2a, p3b, p1 ]
    elif vecEqual(p1a, p1) and vecEqual(p2a, p2):                       # clip to quad cases
        return [ p1, p2, p3c, p3b ]
    elif vecEqual(p1b, p1) and vecEqual(p3b, p3):
        return [ p3, p1, p2a, p2c ]
    elif vecEqual(p2c, p2) and vecEqual(p3c, p3):
        return [ p2, p3, p1b, p1a ]
    return [ p1, p2, p3 ]                                               # should never happen, but just in case...no clipping again
