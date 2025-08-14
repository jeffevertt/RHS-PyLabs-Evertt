from lib.window import Window
from lib.simulation import Simulation
from lib.utils import *
from lib.winobj_wall import Wall
from lib.winobj_circle import Circle

############## IT IS YOUR JOB TO IMPLEMENT THIS FUNCTION IN THIS LAB ############
######### The circle/ball should bounce off of the floor, implement this ########
#### There are three types of balls (hold SHIFT, then CONTROL when dropping) ####
######### Your implementation should try to conserve energy in the system #######
#################################################################################
def updateFunction(circle:Circle, deltaTime):
    # setup
    sim: Simulation = window.sim
    walls = sim.objectsOfType(Wall)
    
    # setup: save starting pos and vel
    posBefore = circle.pos.copy()
    velBefore = circle.vel.copy()

    # TODO: update ball's pos & vel for this time step
    ...
    
    # TODO: collide with walls
    ...


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
def clickReleaseFn(pos, vel):
    vel = limitMag(vel, 0)
    (text, color) = ("B", "green") if window.isKeyPressed('Shift_L') else ("A", "orange")
    (text, color) = ("C", "steelblue") if window.isKeyPressed('Control_L') else (text, color)
    ball = Circle(window, pos, 0.5, vel = vel, text = text, color = color, updateFn = updateFunction)
    
window = Window("Lab 4a: Ball Collision", subTitle = "Goal: Bounce your ball off the red ball...", clickReleaseFn = clickReleaseFn)
wall = Wall(window, v2(0,-8), v2(0,1))
window.runGameLoop()
