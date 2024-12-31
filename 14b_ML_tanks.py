from lib.window_arena import *
from lib.winobj_tank import *
from typing import List
from sklearn.ensemble import RandomForestRegressor
import pickle

# training input data (the length of the two data lists should match)
featureData = [] # list of lists, where each inner list represents the training feature inputs
commandData = [] # list of lists, where each inner list represents the training desired command outputs

# model data
model = None # trained model

# when in INTERACTIVE mode, use this to capture game state and commands & train your ML model
def onExecCmd(cmd: TankCmd, levelTime: int, tank: Tank, powerUps: List[PowerUp], targets: List[Target]):
    global featureData, commandData
    
    # gather the training features (relavent game state) and append to featureData and append command values to commandData
    #TODO
    #featureData.append( np.array(calcFeatureInput(levelTime, tank, powerUps, targets)) )
    #commandData.append( np.array([ cmd.typeAsInt(), ... ]) )
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
    #TODO
    features = [ ]
    #...
    return features


# update tank (this is where your code goes once your ML model is trained)
def updateTank1(tank: Tank, powerUps: List[PowerUp], targets: List[Target]):
    global model
    
    #TODO: once you have your ML model trained, switch the gameConfig to ADVANCED & hook it up here to drive the tank
    # load your model (if not already loaded)
    if model is None:
        with open('14b_ML_tanks - model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)

    # use the model to determine the next move (note that you may need to do some cleanup afterwards)
    features = calcFeatureInput( tank.window.levelTime, tank, powerUps, targets )
    modelDecision = model.predict( np.array(features).reshape(1, -1) )
    #TODO


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
########################## EXCEPT TO REMOVE TUTORIAL GAME CONFIG ARGUMENT  #########################
####################################################################################################
WindowArena(playerCount = 1, 
            userCode1 = updateTank1,
            interactExecCmd = onExecCmd,
            interactGameDone = onGameDone,
            gameConfig = WindowArenaConfig.TANKS_INTERACTIVE, #WindowArenaConfig.TANKS_INTERACTIVE, #WindowArenaConfig.TANKS_ADVANCED,
            windowTitle = "Lab 14b: Tanks! (ML)").runGameLoop()