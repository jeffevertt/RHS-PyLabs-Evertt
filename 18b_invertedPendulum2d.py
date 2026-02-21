from lib.window import Window
from lib.simulation import Simulation
from lib.utils import *
from lib.window_sim_invPend import WindowSimInvPend


############## IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB ############
########## ... ########
#################################################################################
def calcPivotThrust(pivotPos:v2, rodAngle, deltaTime):
    # setup
    sim: Simulation = window.sim
    
    # TODO
    
    return 0


####################################################################################################
############################## DO NOT MODIFY METHODS BELOW THIS LINE ###############################
####################################################################################################
window = WindowSimInvPend("Lab 18b: Inverted Pendulum", "Goal: Control the pivot's linear thrust to keep the rod balanced.")
window.runGameLoop()
