from lib.window_arena import *
from lib.winobj_tank import *

# update tank (this is where your code goes)
def updateTank1(tank: Tank, powerUp: PowerUp, target: Target):
    # set our name
    tank.setPlayerName("Teacher")
    
    # if the trg is in range, shoot at it & done
    if length(target.pos - tank.pos) < tank.ammoMaxRange:
        tank.queueCommand( TankCmd_Shoot(target.pos - tank.pos) )
        return

    # go after the closest powerup
    delta = powerUp.pos - tank.pos
    if abs(delta[0]) > 0: 
        tank.queueCommand( TankCmd_Move( v2(delta[0], 0) ) )
    if abs(delta[1]) > 0: 
        tank.queueCommand( TankCmd_Move( v2(0, delta[1]) ) )

####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
########################## EXCEPT TO REMOVE TUTORIAL GAME CONFIG ARGUMENT  #########################
####################################################################################################
WindowArena(playerCount = 1, 
            userCode1 = updateTank1,
            gameConfig = WindowArenaConfig.TANKS_DEFAULT).runGameLoop()   # WindowTanksConfig.DEFAULT