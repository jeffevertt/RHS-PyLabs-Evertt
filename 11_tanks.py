from lib.window_arena import *
from lib.winobj_tank import *
from typing import List

# update tank (this is where your code goes)
def updateTank1(tank: Tank, powerUps: List[PowerUp], targets: List[Target]):
    tank.queueCommand( TankCmd_Move(v2(1,0)) )
    tank.queueCommand( TankCmd_Move(v2(0,1)) )



####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
########################## EXCEPT TO REMOVE TUTORIAL GAME CONFIG ARGUMENT  #########################
####################################################################################################
WindowArena(userCode1 = updateTank1,
            gameConfig = WindowArenaConfig.TANKS_ADVANCED,
            windowTitle = "Lab 11: Tanks! (advanced)").runGameLoop()