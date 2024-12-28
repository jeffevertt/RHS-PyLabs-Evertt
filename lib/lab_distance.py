import numpy as np
from scipy.interpolate import splprep, splev
import time
import math
from enum import Enum

from lib.canvas import Canvas
from lib.canvas_object import CanvasObject
from lib.canvas_object_circle import CanvasObjectCircle
from lib.utils import *

class LabType(Enum):
    DISTANCE = 1
    ANGLE = 2

def runLab(labType, labTitle, a, aPts, b, bPts, calcValueFn, animTime, interpK = 1):
    canvas = Canvas(labTitle)
    a.setCanvas(canvas)
    if b != None:
        b.setCanvas(canvas)
    canvas.display()
    
    # create a splines (linear: k = 1)
    xA, yA = zip(*aPts)
    tckA, uA = splprep([xA, yA], s = 0, k = interpK)
    uAllA = np.linspace(0, 1, 500)
    xAllA, yAllA = splev(uAllA, tckA)

    xB, yB = zip(*bPts)
    tckB, uB = splprep([xB, yB], s = 0, k = interpK)
    uAllB = np.linspace(0, 1, 500)
    xAllB, yAllB = splev(uAllB, tckB)
    
    # render CB
    def drawExtras():
        # line B to A
        startPt = a.pos if b != None else [0, 0]
        endPt = b.pos if b != None else a.pos
        canvas.drawLine(startPt, endPt, 'green', 5)
        
        # angle arc (maybe)
        if labType == LabType.ANGLE:
            lineLen = 5
            lineAngle = math.degrees(math.atan2((endPt[1]-startPt[1]),(endPt[0]-startPt[0])))
            canvas.drawLine(startPt, [startPt[0] + lineLen, startPt[1]], 'red', 2)
            canvas.drawArcAngle(startPt, min(3, lineLen * 0.9), 0, lineAngle, 'blue', 3)
    canvas.setPreObjCB(drawExtras)
    
    # animate
    for (xA, yA), (xB, yB) in zip(zip(xAllA, yAllA), zip(xAllB, yAllB)):
        a.pos = [xA, yA]
        if b != None:
            b.pos = [xB, yB] if bPts != None else [0, 0]
        
        # check if their distance function works
        if labType == LabType.DISTANCE:
            dst = calcValueFn(a, b) if b != None else calcValueFn(a)
            ap = a.pos
            bp = b.pos if b != None else [0, 0]
            expected = math.sqrt((ap[0]-bp[0])**2+(ap[1]-bp[1])**2)
            if not (compareDst(dst, expected)):
                canvas.log(f"incorrect distance: {dst:.3f} (expected: {expected:.2f})")
                canvas.setSubTitle(f"dst = {dst:.3f}", "red")
                canvas.setResult(False)
                return
            canvas.setSubTitle(f"dst = {dst:.3f}", "green")
        elif labType == LabType.ANGLE:
            angle = calcValueFn(a, b) if b != None else calcValueFn(a)
            ap = a.pos
            bp = b.pos if b != None else [0, 0]
            expected = math.degrees(math.atan2((bp[1]-ap[1]),(bp[0]-ap[0]))) if b != None else math.degrees(math.atan2(ap[1],ap[0]))
            if not (compareAngle(angle, expected)):
                canvas.log(f"incorrect angle: {posAngleDeg(angle):.2f}° (expected: {posAngleDeg(expected):.2f})")
                canvas.setSubTitle(f"angle = {posAngleDeg(angle):.2f}°", "red")
                canvas.setResult(False)
                return
            canvas.setSubTitle(f"angle = {posAngleDeg(angle):.2f}°", "green")
        
        # update
        canvas.update()
        canvas.drawWorld()
        
        # keep on going
        time.sleep(animTime / len(uAllA))
        
    # we get here, then success
    canvas.log("Well done!\n\nGo on to the next challenge...")
    canvas.setResult(True)
    
def runLab_distance1(a, calcDst, animTime = 5):
    eps = 0.0000000001
    runLab(LabType.DISTANCE, 
           "Calculate the distance from the origin to the center of point A",
           a, [(10, 0), (-10, 0), (0, 0), (0, 5), (0, -5)],
           None, [(0, 0), (eps, eps), (0, 0), (eps, eps), (0, 0)],
           calcDst, animTime)

def runLab_distance2(a, b, calcDst, animTime = 5):
    runLab(LabType.DISTANCE, 
           "Calculate the distance from the centers of point A and point B",
           a, [(5, 0), (8, 8), (0, 0), (-3, 5), (-10, -5)],
           b, [(-5, 0), (5, -6), (-8, 0), (0, 7), (3, -2), (-6, 2)],
           calcDst, animTime, interpK = 3)
    
def runLab_distance3(a, calcAngle, animTime = 5):
    eps = 0.0000000001
    runLab(LabType.ANGLE, 
           "Calculate the angle from the x-axis to the line from the origin to A",
           a, [(5, 0), (3.7, 3.7), (0, 5), (-3.7, 3.7), (-5, 0)],
           None, [(0, 0), (eps, eps), (0, 0), (eps, eps), (0, 0)],
           calcAngle, animTime, interpK = 3)

def runLab_distance4(a, b, calcAngle, animTime = 8):
    eps = 0.0000000001
    runLab(LabType.ANGLE, 
           "Calculate the angle of rotation for point B around A",
           a, [(0, 0), (eps, 0), (0, 0), (5, 0), (5, -5)],
           b, [(5, 0), (5, 5), (8, 0), (-5, -8), (-8, -5), (0, 5)],
           calcAngle, animTime, interpK = 1)