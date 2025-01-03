from lib.window_alien_invasion import *

# update functions (this is where your code goes)
#   determine which direction to shoot, then use the cannon shoot method to do so.
#  useful method...
#   cannon.shoot(dir)   - rotate and shoot in the direction specified
#   aliens              - the list of aliens
#   aliens[0].pos       - position of the first alien in the list
#   aliens[0].vel       - velocity of the first alien in the list
def updateCannon(cannon, aliens, deltaTime):
    # TODO: your code goes here
    pass


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
####################################################################################################
WindowAlienInvasion(updateCannonFn = updateCannon).runGameLoop()