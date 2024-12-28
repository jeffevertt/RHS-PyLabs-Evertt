from lib.window_sim_ik import *
from lib.winobj_link import *

def setupScene(window):
    #TODO: create a chain of links, you can use something like this to do it...
    # head = Link(window, v2(0,10), angle = -90)
    # next = Link(window, head.posEnd(), angle = -90, parent = head)
    pass

def updateChain(deltaTime, chainHead, subStepPerc):
    # consts
    gravity = v2(0,-9.8)
    # TODO: your other constants (spring constant, damp factor)
    
    # walk the chain applying forces to each node (skip head, it should stay static)
    node = chainHead.child
    while node is not None:
        # TODO: apply spring constant and gravity forces/acceleration
        
        # TODO: update node.vel & node.pos
        
        # next
        node = node.child



####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
WindowSimIK(setupFn = setupScene, updateChainFn = updateChain).runGameLoop()