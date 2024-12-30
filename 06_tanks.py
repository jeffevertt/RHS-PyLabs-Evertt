from lib.window_arena import *
from lib.winobj_tank import *

# update tank (this is where your code goes)
def updateTank1(tank: Tank, powerUp: PowerUp, target: Target):
    #tank.queueCommand( TankCmd_Move(v2(1,0)) )
    pass



####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
########################## EXCEPT TO REMOVE TUTORIAL GAME CONFIG ARGUMENT  #########################
####################################################################################################
WindowArena(playerCount = 1, 
            userCode1 = updateTank1,
            gameConfig = WindowArenaConfig.TANKS_TUTORIAL).runGameLoop()   # WindowTanksConfig.TANKS_DEFAULT