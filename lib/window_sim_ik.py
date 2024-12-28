import tkinter as tk
from lib.window import Window
from lib.winobj_link import *
from lib.utils import *

class WindowSimIK(Window):
    def __init__(self, setupFn = None, updateChainFn = None):
        super().__init__("Lab 15: Simulation!", gridPixelsPerUnit = 24)
        
        self.setupFn = setupFn
        self.updateChainFn = updateChainFn
        self.selectedLink = None
        self.selectedLinkForcePos = None
        
    def initApp(self):
        super().initApp()

        # kick off the simulation
        self.resetSimulation()
        
    def update(self, deltaTime):
        super().update(deltaTime)
        
        # level update
        self.updateLevel(deltaTime)
            
    def getChainHead(self):
        links = self.sim.objectsOfType(Link)
        for link in links:
            if link.parent is None:
                return link
    def getChainTail(self):
        links = self.sim.objectsOfType(Link)
        for link in links:
            if link.child is None:
                return link
    def getChainWithTail(self, tail : Link):
        chain = []
        node = tail if tail != None else self.getChainTail()
        while node != None:
            chain.insert(0, node)
            node = node.parent
        return chain
    def applyIkSolver(self, tail : Link, goalPos, iterations = 20):
        # build the chain
        chain = self.getChainWithTail(tail)
        headPos = chain[0].pos # this is the initial head position (the head node should stay locked here)
        # using FABRIK (Forward and Backward Reaching IK), this is a pretty good video tutorial: https://www.youtube.com/watch?v=UNoX65PRehA
        for _ in range(iterations):
            # back propogating: reverse up the chain
            for i in reversed(range(len(chain))):
                node = chain[i]
                if i < len(chain) - 1:
                    child = chain[i + 1]
                    childToNode = unit(node.pos - child.pos)
                    node.pos = child.pos + childToNode * node.length
                else:
                    node.pos = goalPos
                node = node.parent
            # forward propogating: forward down the chain
            for i in range(len(chain)):
                node = chain[i]
                if i > 0:
                    parent = chain[i - 1]
                    parentToNode = unit(node.pos - parent.pos)
                    node.pos = parent.pos + parentToNode * node.length
                else:
                    node.pos = headPos
        # update the nodes now that we're done
        node = chain[0]
        while node is not None:
            node.updateDirVec()
            node.updatePrevPos()
            node = node.child
            
    def isHeadOrParentOfLink(self, parent, child):
        if child.parent is None:
            return True
        while child.parent is not None:
            if child.parent == parent:
                return True
            child = child.parent
        return False
    
    def onMouseLeftPressed(self, event):
        super().onMouseLeftPressed(event)
        # maybe select a link
        mousePos = self.toCoordFrame(v2(event.x, event.y))
        links = self.sim.objectsOfType(Link)
        for link in links:
            if length(mousePos - link.posStart()) < link.radius:
                self.selectedLink = link
                self.selectedLinkForcePos = mousePos if self.selectedLink.parent is not None else v2_zero()
                break
    def onMouseLeftReleased(self, event):
        super().onMouseLeftReleased(event)
        self.selectedLink = None
        self.selectedLinkForcePos = None
    def onMouseMotion(self, event):
        mousePos = self.toCoordFrame(v2(event.x, event.y))
        if self.selectedLink is not None and self.lastMousePos is not None:
            if self.selectedLink.parent is not None:
                self.selectedLinkForcePos = mousePos
            else:
                self.selectedLinkForcePos += mousePos - self.lastMousePos[0]
        super().onMouseMotion(event)
    def onMouseLeftDoubleClick(self, event):
        self.resetSimulation()
    def applyMouseSelectedLink(self):
        # if mouse has one, ik to the position
        if self.selectedLink is not None and self.selectedLinkForcePos is not None:
            if self.selectedLink.parent is not None:
                self.applyIkSolver(self.selectedLink, self.selectedLinkForcePos)
            else:
                self.selectedLink.translate(self.selectedLinkForcePos)
                self.selectedLinkForcePos = v2_zero()
        
    def resetSimulation(self, fullReset = True):
        # maybe destroy all objects & do initial scene setup
        if fullReset:
            self.sim.destroyAll()

            # user code setup
            if self.setupFn != None:
                self.setupFn(self)
                self.sim.updateGfxAllObjects()
        
        # tell the simulation about it
        self.sim.update(0)

    def updateLevel(self, deltaTime, firstUpdate = False):
        # consts
        subSteps = 10
        timeScale = 5
        
        # call update on all the head nodes
        if self.updateChainFn != None:
            # update all chains (passing in the head)            
            links = self.sim.objectsOfType(Link)
            for link in links:
                # if no parent, then it's a head, need to update
                if link.parent is None and link.child is not None:
                    # if mouse has one, ik to the position
                    if self.selectedLink is not None and self.isHeadOrParentOfLink(link, self.selectedLink):
                        self.applyMouseSelectedLink()
                    
                    # substep support
                    subStepDeltaTime = deltaTime * timeScale / subSteps
                    for i in range(subSteps):
                        # let user code update this chain
                        subStepPerc = i / (subSteps - 1)
                        self.updateChainFn(subStepDeltaTime, link, subStepPerc)
            
                    # if mouse has one, ik to the position
                    if self.selectedLink is not None and self.isHeadOrParentOfLink(link, self.selectedLink):
                        self.applyMouseSelectedLink()

        # update link dirVecs & graphics objects
        for link in links:
            link.updateDirVec()
        self.sim.updateGfxAllObjects()