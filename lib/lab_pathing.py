import numpy as np
from scipy.interpolate import splprep, splev
import time
import math
from enum import Enum

from lib.canvas import Canvas
from lib.canvas_object import CanvasObject
from lib.canvas_object_circle import CanvasObjectCircle
from lib.canvas_object_rectangle import CanvasObjectRectangle
from lib.utils import *

def runLab(labTitle, circle, goal, rects, path, animTime):
    canvas = Canvas(labTitle)
    goal.setCanvas(canvas)
    circle.setCanvas(canvas)
    for rect in rects:
        rect.setCanvas(canvas)
    canvas.display()
    
    # locals
    p0 = circle.pos.copy()
    curSegIdx = 0
    
    # render CB
    def drawExtras():
        pos = p0.copy()
        for i, seg in enumerate(path):
            if i < curSegIdx:
                canvas.drawLine(pos, pos + seg, 'green', 4)
                pos += seg
            elif i == curSegIdx:
                canvas.drawLine(pos, pos + seg, 'red', 4)
    canvas.setPreObjCB(drawExtras)
    
    # animate
    startTime = time.time()
    endTime = startTime + animTime
    while time.time() < endTime:
        # figure out where we are in the path
        pathLen = 0
        for seg in path:
            pathLen += length(seg)
        linVel = pathLen / animTime
        dstTrav = min(linVel * (time.time() - startTime), pathLen)
        
        # and figure out where we are now and update the circle pos
        pos = p0.copy()
        dstRem = dstTrav
        for i, seg in enumerate(path):
            if dstRem > length(seg):
                dstRem -= length(seg)
                pos += seg
                continue
            pos += seg * (dstRem / length(seg))
            curSegIdx = i
            break
        circle.pos = pos

        # check for intersection
        quitAfterThis = False
        for rect in rects:
            if intersectRectCircle(pos, circle.radius, rect.pos, rect.halfDims, rect.angleDeg):
                canvas.setResult(False)
                quitAfterThis = True                
        
        # check if made it to the goal
        dstFromGoal = length(goal.pos - circle.pos)
        if not quitAfterThis and dstFromGoal < circle.radius:
            canvas.log("Well done!\n\nGo on to the next challenge...")
            canvas.setResult(True)
            quitAfterThis = True
        
        # update
        canvas.update()
        canvas.drawWorld()
        
        # keep on going
        if not quitAfterThis:
            time.sleep(0.01)
        else:
            break
    
    # if we didn't succeed yet, then we're cooked
    if canvas.result == None:
        canvas.setResult(False)
    
def runLab_pathing1(path, animTime = 5):
    circle = CanvasObjectCircle( v2(0,0), 0.5, "", "blue" )
    goal = CanvasObjectCircle( v2(-5,8), 0.6, "G", "green" )
    rects = [ CanvasObjectRectangle( v2(-7.5, 0), v2(6, 6), 0, "#404040") ]
    runLab("Provide a safe path (list of vectors) for the ball to its goal.",
           circle, goal, rects, path, animTime)

def runLab_pathing2(path, animTime = 5):
    circle = CanvasObjectCircle( v2(0,0), 0.5, "", "blue" )
    goal = CanvasObjectCircle( v2(6.5, 9), 0.6, "G", "green" )
    rects = [ CanvasObjectRectangle( v2(-7.5, 0), v2(6, 3), 0, "#404040"),
              CanvasObjectRectangle( v2( 8, 0), v2(6, 3), 0, "#404040"),
              CanvasObjectRectangle( v2( 0, 7), v2(2, 5), -45, "#404040"),
              CanvasObjectRectangle( v2( 7, 5), v2(2, 5), -45, "#404040") ]
    runLab("Provide a safe path (list of vectors) for the ball to its goal.",
           circle, goal, rects, path, animTime)
    
def runLab_pathing3(path, animTime = 5):
    circle = CanvasObjectCircle( v2(-12,-7), 0.5, "", "blue" )
    goal = CanvasObjectCircle( v2(5, 5), 0.6, "G", "green" )
    rects = [ CanvasObjectRectangle( v2(0, 0), v2(10, 3), 0, "#404040", angVelDeg = -48) ]
    runLab("Provide a safe path (list of vectors) for the ball to its goal.",
           circle, goal, rects, path, animTime)

def runLab_pathing4(path, animTime = 5):
    circle = CanvasObjectCircle( v2(-5,-5), 0.5, "", "blue" )
    goal = CanvasObjectCircle( v2(-12, 4), 0.6, "G", "green" )
    rects = [ CanvasObjectRectangle( v2(-6, 1), v2(12, 2), 20, "#404040"),
              CanvasObjectRectangle( v2(10, 0), v2(2, 20), 0, "#404040"),
              CanvasObjectRectangle( v2(-10, 8), v2(8, 2), 10, "#404040") ]
    runLab("Provide a safe path (list of vectors) for the ball to its goal.",
           circle, goal, rects, path, animTime)
    
def runLab_pathing5(path, animTime = 5):
    circle = CanvasObjectCircle( v2(-12,-8), 0.5, "", "blue" )
    goal = CanvasObjectCircle( v2(-5, 9), 0.6, "G", "green" )
    rects = [ CanvasObjectRectangle( v2(-7, 0), v2(8, 2), 0, "#404040", angVelDeg = -20),
              CanvasObjectRectangle( v2( 7, 0), v2(8, 2), 0, "#404040", angVelDeg = -20) ]
    runLab("Provide a safe path (list of vectors) for the ball to its goal.",
           circle, goal, rects, path, animTime)
    
def runLab_pathing6(path, animTime = 5):
    circle = CanvasObjectCircle( v2(-7,-8), 0.5, "", "blue" )
    goal = CanvasObjectCircle( v2(11, 9), 0.6, "G", "green" )
    rects = [ CanvasObjectRectangle( v2(-10, -6), v2(1, 5), 0, "#404040"),
              CanvasObjectRectangle( v2( 0, -8), v2(6, 2), 0, "#404040"),
              CanvasObjectRectangle( v2(-4, -2), v2(5, 1), 0, "#404040"),
              CanvasObjectRectangle( v2( 5, 0), v2(1, 4), 0, "#404040"),
              CanvasObjectRectangle( v2(12, -1), v2(4, 1), 0, "#404040"),
              CanvasObjectRectangle( v2( 9, 8), v2(1, 2), 0, "#404040"),
              CanvasObjectRectangle( v2(11, 7), v2(2, 1), 0, "#404040"),
              CanvasObjectRectangle( v2(-5, 5), v2(6, 2), 45, "#404040") ]
    runLab("Provide a safe path (list of vectors) for the ball to its goal.",
           circle, goal, rects, path, animTime)