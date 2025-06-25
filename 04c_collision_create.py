from lib.window import Window
from lib.simulation import Simulation
from lib.utils import *
from lib.winobj_wall import Wall
from lib.winobj_circle import Circle

############# IT IS YOUR JOB TO IMPLEMENT THESE FUNCTION IN THIS LAB #############
def createWorld(window):
    # create up your world objects, get creative...
    pass
    
def updateBallFunction(circle, deltaTime):
    # setup (get all the objects in the scene)
    sim: Simulation = window.sim
    walls = sim.objectsOfType(Wall)
    balls = sim.objectsOfType(Circle)
    
    # update pos/vel
    ...

    # deal with collisions with this object (circle)
    ...


####################################################################################################
def clickReleaseFn(pos, vel):
    vel = limitMag(vel, 30)
    circle = Circle(window, pos, 2.0, vel = vel, color = "steelblue", updateFn = updateBallFunction)
    circle.dynamic = True
    
window = Window("Lab 4c: Collision Create", subTitle = "Goal: Create a fun physics lab...", clickReleaseFn = clickReleaseFn)
createWorld(window)
window.runGameLoop()
