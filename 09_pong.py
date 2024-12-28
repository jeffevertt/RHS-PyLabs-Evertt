from lib.window_pong import *
from lib.winobj_circle import *

# update functions (this is where your code goes)
def updateBall(ball, deltaTime):
    #TODO: Update the ball based on its velocity (ball.vel)
    pass
def collideBallWall(ball, wallPoint, wallNormal):
    #TODO: Check for & respond to collision with ball & wall
    pass
def collideBallPaddle(ball, paddleCenter, paddleWidth, paddleHeight):
    #TODO: Check for & respond to collision with ball & paddle
    pass



####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
def updateFn(deltaTime, ball, walls, paddles):
    updateBall(ball, deltaTime)
    for wall in walls:
        collideBallWall(ball, wall.pos, wall.normal)
    for paddle in paddles:
        collideBallPaddle(ball, paddle.pos, paddle.width, paddle.height)
WindowPong(updateBallFn = updateFn).runGameLoop()