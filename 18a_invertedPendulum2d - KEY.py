from lib.window import Window
from lib.simulation import Simulation
from lib.utils import *
from lib.window_sim_invPend import WindowSimInvPend


############## IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB ############
##########   This function computes the desired thrust - positive moves  ########
##########       the base/pivot right and negative moves it left.        ########
##########   While you can manually control the pivot with the keyboard  ########
########## arrow keys, the real goal is to write an automatic controller ########
##########    inside this function. You decide how. You are given the    ########
##########   base/pivot's position and the angle of the rod (90 degrees  ########
##########     is perfectly vertical, 0 is flat right). You will know    ########
##########  that it is working when the bases motion not only keeps the  ########
######## the rod upright, but it also settles quickly to no motion at all #######
#################################################################################
def calcPivotThrust(pivotPos:v2, rodAngle, deltaTime):
    # config
    const_P = 18.0
    const_I = 0.5
    const_D = 8.0

    # setup
    sim: Simulation = window.sim
    error = 90 - rodAngle
    
    # proportional
    p = const_P * error
    
    # integral
    sim.errorSum += error * deltaTime
    i = const_I * sim.errorSum
    
    # derivative
    errorDiff = (error - sim.errorLast) / deltaTime
    d = const_D * errorDiff
    sim.errorLast = error
    
    return p + i + d
def onReset():
    sim: Simulation = window.sim
    sim.errorLast = 0
    sim.errorSum = 0

####################################################################################################
############################## DO NOT MODIFY METHODS BELOW THIS LINE ###############################
####################################################################################################
window = WindowSimInvPend("Lab 18a: Inverted Pendulum", "Goal: Control the pivot's linear thrust to keep the rod balanced.", calcPivotThrust=calcPivotThrust, onReset=onReset)
window.runGameLoop()
