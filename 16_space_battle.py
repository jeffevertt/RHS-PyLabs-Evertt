from lib.window_arena import *
from lib.winobj_ship import *
from typing import List

# update ship (this is where your code goes)
def updateShip1(ship: Ship, powerUps: List[PowerUp], targets: List[Target]):
    #ship.queueCommand( ShipCmd_Thrust(1) )
    pass



####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
########################## EXCEPT TO REMOVE TUTORIAL GAME CONFIG ARGUMENT  #########################
####################################################################################################
WindowArena(userCode1 = updateShip1,
            gameConfig = WindowArenaConfig.SPACE_BATTLE,
            windowTitle = "Lab 16: Space Battle!").runGameLoop()