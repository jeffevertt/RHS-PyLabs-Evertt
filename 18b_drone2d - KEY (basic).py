from lib.window import Window
from lib.simulation import Simulation
from lib.utils import *
from lib.winobj_drone2d import Drone2D
from lib.winobj_wall import Wall

############## IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB ############
######### ... ########
#################################################################################
def calcDroneThrust(drone:Drone2D, targetPos:v2, deltaTime):
    # setup
    sim: Simulation = window.sim
    thrustAngle = 0                 # local space, 0 indicates directly upwards (positive counter clockwise)
    thrustMag = 0                   # force vector mag
    
    # error Vector (target - current)
    errorVec:v2 = targetPos - drone.pos
    errorVec = min(length(errorVec), 5.0) * unit(errorVec)  # clamp it
    
    # proportional Gain (Kp) - determines 'stiffness'
    Kp = 8.0 
    
    # force proportional to the distance from target
    thrustMag = max(dot(errorVec, drone.up()), 0.0) * Kp
    
    # thrust Angle
    thrustAngle = atan2Deg(errorVec[1], errorVec[0]) - 90
    
    return (thrustAngle, thrustMag)


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
def onDoubleClick(window:Window): # reset
    drone = window.sim.objectsOfType(Drone2D)
    drone[0].pos, drone[0].angle, drone[0].vel, drone[0].angVel = v2_zero(), 0.0, v2_zero(), 0.0
window = Window("Lab 18b: Drone 2D", subTitle = "Goal: Control the drone's thrust vector to reach the target (the mouse position)", clickDoubleFn = onDoubleClick)
ground = Wall(window, v2(0,-8), v2(0,1))
drone = Drone2D(window, v2(0,0), ground = ground, calcThrustFn = calcDroneThrust)
window.runGameLoop()
