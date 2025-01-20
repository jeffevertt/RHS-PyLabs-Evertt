import numpy as np
from lib.utils import *

# checks tri winding order (assumes right handed coordinate system, points in NDC)
def isBackfaceCulledNDC(poly):
    # use the first three verts for this
    p1 = poly[0]
    p2 = poly[1]
    p3 = poly[2]
    
    # get the tri normal and compare to camera fwd (which is always [0,0,1] in cam, clip, & NDC space)
    triNormal = cross((v3_from_v4(p2) - v3_from_v4(p1)), (v3_from_v4(p3) - v3_from_v4(p1)))
    return triNormal[2] > 0

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

# Cohen-Sutherland again, this is in screen space (this is for (0,0) in the UL and (width,height) in the LR)
def clipPolyScreenSpace(polygon, width, height):
    def clip_line_to_bounds(p1, p2, min_x, max_x, min_y, max_y):
        def code(x, y):
            code = 0
            if y < min_y:    # Top (below the screen)
                code |= 0x8
            elif y > max_y:  # bottom (above the screen)
                code |= 0x4
            if x > max_x:    # right
                code |= 0x2
            elif x < min_x:  # left
                code |= 0x1
            return code

        code1 = code(p1[0], p1[1])
        code2 = code(p2[0], p2[1])
        accept = False
        while True:
            if (code1 | code2) == 0:
                accept = True
                break
            elif (code1 & code2) != 0:
                break
            else:
                # Find the outcode that is not zero
                outcode_out = code1 if code1 != 0 else code2

                # Calculate the intersection point
                x, y = 0, 0
                if outcode_out & 0x8:   # Top (Below the screen)
                    x = p1[0] + (p2[0] - p1[0]) * (min_y - p1[1]) / (p2[1] - p1[1])
                    y = min_y
                elif outcode_out & 0x4:  # Bottom (Above the screen)
                    x = p1[0] + (p2[0] - p1[0]) * (max_y - p1[1]) / (p2[1] - p1[1])
                    y = max_y
                elif outcode_out & 0x2:  # Right
                    y = p1[1] + (p2[1] - p1[1]) * (max_x - p1[0]) / (p2[0] - p1[0])
                    x = max_x
                elif outcode_out & 0x1:  # Left
                    y = p1[1] + (p2[1] - p1[1]) * (min_x - p1[0]) / (p2[0] - p1[0])
                    x = min_x

                # Replace the endpoint with the intersection point
                if outcode_out == code1:
                    p1 = (x, y)
                    code1 = code(p1[0], p1[1])
                else:
                    p2 = (x, y)
                    code2 = code(p2[0], p2[1])

        return accept, p1, p2

    clipped_polygon = []
    num_vertices = len(polygon)
    for i in range(num_vertices):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % num_vertices]  # Wrap around to the first vertex

        # clip the line segment to the screen bounds
        #  note: kind of an ugly hack here, some issues with precise clipping, so extending region and letting tk deal exact clipping
        is_intersecting, clipped_p1, clipped_p2 = clip_line_to_bounds(p1, p2, -10*width, 10*width, -10*height, 10*height) #0, width, 0, height)
        if is_intersecting:
            # avoid duplicate vertices
            if len(clipped_polygon) == 0 or not vecEqual(clipped_polygon[-1], clipped_p1):
                clipped_polygon.append(clipped_p1)
            if not vecEqual(clipped_p1, clipped_p2):
                clipped_polygon.append(clipped_p2)
        # else:
        #     # was working on a fix for the hack mentioned above, but not quite there
        #     clipped_polygon.append( ( min(max(clipped_p1[0], 0), width), min(max(clipped_p1[1], 0), height) ))

    return clipped_polygon

# version of clipping code that uses line clip and only attempts to clip vs near clip plane
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
