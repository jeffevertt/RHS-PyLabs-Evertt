from lib.window_arena import *
from lib.winobj_tank import *
from typing import List
from sklearn.ensemble import RandomForestRegressor
import pickle

# Note: The provided starting point only considers one target & ignores targets.
#       However, the training framework supports multiple powerups & targets.
#       Your task is to build on this starting point & improve the implementation.

# training input data (the length of the two data lists should match)
featureData = [] # list of lists, where each inner list represents the training feature inputs
commandData = [] # list of lists, where each inner list represents the training desired command outputs

# model data
model = None # trained model

# when in INTERACTIVE mode, use this to capture game state and commands & train your ML model
def onExecCmd(cmd: TankCmd, levelTime: int, tank: Tank, powerUps: List[PowerUp], targets: List[Target]):
    global featureData, commandData
    
    # tank position after the command (only changes for moves)
    tankPosAfterCmd = tank.pos.copy()
    if isinstance(cmd, TankCmd_Move):
        tankPosAfterCmd += cmd.dir
        
    # closest powerup to where the tank will be
    powerUpClosest = powerUps[0]
    for powerUp in powerUps:
        if length(powerUp.pos - tankPosAfterCmd) < length(powerUpClosest.pos - tankPosAfterCmd):
            powerUpClosest = powerUp
    
    # gather the training features (relavent game state) and append to featureData and append command values to commandData
    #TODO: Improve this to work with all powerups and to shoot targets
    featureData.append( np.array(calcFeatureInput(levelTime, tank, [powerUpClosest], [])) )
    commandData.append( np.array([ cmd.typeAsInt(), cmd.dir[0], cmd.dir[1] ]) )
def onGameDone():
    global featureData, commandData
    
    # train your model
    model = RandomForestRegressor(n_estimators = 100, random_state = 42) 
    model.fit(featureData, commandData)
    
    # save your model
    with open('14b_ML_tanks - model.pkl', 'wb') as modelFile:
        pickle.dump(model, modelFile)
def calcFeatureInput(levelTime: int, tank: Tank, powerUps: List[PowerUp], targets: List[Target]):
    # convert the game state to a list of feature inputs for the model to use (these features describe the world state)...this should be called by both onExecCmd & updateTank1)
    features = [ ]
    for powerUp in powerUps:
        relPos = powerUp.pos - tank.pos
        powerUpFeatures = [ relPos[0], relPos[1], length(relPos), powerUp.typeAsInt() ]
        appendElements( features, powerUpFeatures ) # just give it the closest, maybe?
    for target in targets:
        relPos = target.pos - tank.pos
        targetFeatures = [ relPos[0], relPos[1], length(relPos) ]
        appendElements( features, targetFeatures )
    return features


# update tank (this is where your code goes once your ML model is trained)
def updateTank1(tank: Tank, powerUps: List[PowerUp], targets: List[Target]):
    global model
    
    # load your model (if not already loaded)
    if model is None:
        with open('14b_ML_tanks - model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
            
    # closest powerup
    #TODO: Improve this to work with all powerups and to shoot targets
    powerUpClosest = powerUps[0]
    for powerUp in powerUps:
        if length(powerUp.pos - tank.pos) < length(powerUpClosest.pos - tank.pos):
            powerUpClosest = powerUp

    # use the model to determine the next move (note that you may need to do some cleanup afterwards)
    features = calcFeatureInput( tank.window.levelTime, tank, [powerUpClosest], [] )
    modelDecision = model.predict( np.array(features).reshape(1, -1) )
    cmd, dx, dy = modelDecision[0, 0], modelDecision[0, 1], modelDecision[0, 2]
    cmd = round(cmd)
    if cmd < 1:
        if abs(dx) > abs(dy):
            tank.queueCommand( TankCmd_Move(v2(dx, 0)) )
        else:
            tank.queueCommand( TankCmd_Move(v2(0, dy)) )
    else:
        tank.queueCommand( TankCmd_Shoot(v2(dx, dy)) )



####################################################################################################
#############################  DO NOT MODIFY  METHODS BELOW THIS LINE  #############################
##############################  EXCEPT TO CHANGE GAME CONFIG ARGUMENT ##############################
####################################################################################################
WindowArena(playerCount = 1, 
            userCode1 = updateTank1,
            interactExecCmd = onExecCmd,
            interactGameDone = onGameDone,
            gameConfig = WindowArenaConfig.TANKS_INTERACTIVE, #WindowArenaConfig.TANKS_INTERACTIVE, #WindowArenaConfig.TANKS_ADVANCED,
            windowTitle = "Lab 14b: Tanks! (ML)").runGameLoop()