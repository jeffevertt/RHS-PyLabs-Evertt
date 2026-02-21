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
    ...
    
    # setup
    sim: Simulation = window.sim
    
    # TODO: implement the controller
    
    return 0
def onReset():
    sim: Simulation = window.sim
    ...

####################################################################################################
############################## DO NOT MODIFY METHODS BELOW THIS LINE ###############################
####################################################################################################
window = WindowSimInvPend("Lab 18b: Inverted Pendulum", "Goal: Control the pivot's linear thrust to keep the rod balanced.", calcPivotThrust=calcPivotThrust, onReset=onReset)
window.runGameLoop()
