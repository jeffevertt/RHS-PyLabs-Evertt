from lib.window import Window
from lib.simulation import Simulation
from lib.utils import *
from lib.winobj_drone2d import Drone2D
from lib.winobj_wall import Wall

############## IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB ############
########## This function computes the desired thrust (angle & magnitude) ########
##########       the drone itself limits the max magnitude & angle       ########
##########     the angle is in the drone's local space, where zero is    ########
##########    directly up, a positive value pivots the thrust to accel   ########
##########                 the drone up and to the left                  ########
######### The drone should move towards the cursor position & hover there #######
#################################################################################
def calcDroneThrust(drone:Drone2D, targetPos:v2, deltaTime):
    # setup
    sim: Simulation = window.sim
    thrustAngle = 0                 # local space, 0 indicates directly upwards (positive counter clockwise)
    thrustMag = 0                   # force vector mag
    
    # PID constants
    Kp_pos, Ki_pos, Kd_pos = 12.0, 0.5, 15.0
    Kp_rot, Ki_rot, Kd_rot = 10.0, 0.1, 2.0

    # (position) error vector & integrate
    errorVec = targetPos - drone.pos
    drone.accumPosError += errorVec * deltaTime
    drone.accumPosError = min(length(drone.accumPosError), 10.0) * unit(drone.accumPosError)

    # (position) force
    desiredForce = (errorVec * Kp_pos) + (drone.accumPosError * Ki_pos) + (-drone.vel * Kd_pos)
    thrustMag = min(length(desiredForce), Drone2D.MAX_THRUST_MAG)
    
    # (position) tweak - limit to only thrust when vertical
    thrustMag *= max(pow(dot(drone.up(), v2(0,1)), 1), 0)
    
    # (rotation) error vector & integrate
    targetWorldAngle = atan2Deg(desiredForce[1], desiredForce[0]) - 90
    angleError = targetWorldAngle - drone.angle
    angleError = (angleError + 180) % 360 - 180 
    drone.accumAngleError += angleError * deltaTime
    drone.accumAngleError = max(min(drone.accumAngleError, 45.0), -45.0)

    # (rotation) angle
    thrustAngle = (angleError * Kp_rot) + (drone.accumAngleError * Ki_rot) + (-drone.angVel * Kd_rot)
    
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
drone.accumPosError, drone.accumAngleError = v2_zero(), 0.0
window.runGameLoop()
