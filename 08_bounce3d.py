from lib.window_bounce3d import *
from lib.winobj_sphere import *

def updateBall(ball, deltaTime, boxPlanes):
    # TODO: Update the balls position based on its velocity
    # ball.pos, ball.vel
    
    # TODO: Collision and reflection with the boxPlanes
    for i in range(6):
        # get the plane (a point on the plane & the plane's normal vector)
        pt, norm = boxPlanes[i]
        # TODO

####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
WindowBounce3D(updateBallFn = updateBall).runGameLoop()