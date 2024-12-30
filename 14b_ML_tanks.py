from lib.window_arena import *
from lib.winobj_tank import *
from typing import List

# when in INTERACTIVE mode, use this to capture game state and commands & train your ML model
def onExecCmd(cmd: TankCmd, levelTime: int, tank: Tank, powerUps: List[PowerUp], targets: List[Target]):
    # TODO: keep track of the data to be used during training
    pass
def onGameDone():
    # TODO: train your model
    pass


# update tank (this is where your code goes once your ML model is trained)
def updateTank1(tank: Tank, powerUps: List[PowerUp], targets: List[Target]):
    # TODO: once you have your ML model trained, switch the gameConfig to ADVANCED & hook it up here to drive the tank
    pass

####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
########################## EXCEPT TO REMOVE TUTORIAL GAME CONFIG ARGUMENT  #########################
####################################################################################################
WindowArena(playerCount = 1, 
            userCode1 = updateTank1,
            interactExecCmd = onExecCmd,
            interactGameDone = onGameDone,
            gameConfig = WindowArenaConfig.TANKS_INTERACTIVE,
            windowTitle = "Lab 14b: Tanks! (ML)").runGameLoop()