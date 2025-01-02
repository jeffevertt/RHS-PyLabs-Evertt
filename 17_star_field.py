from lib.window_space3d import *
from lib.winobj_star import *
from lib.utils import *
from typing import List

# spawn stars in this method
#   - you are given the current number of stars in the scene (you'll want to spawn up to some number of them, maybe 200 or so)
#   - you should spawn them out in front of the camera (in the camera's FOV)
#   - you can use functions in WindowSpace3D to get information about the camera, some relevant ones...
#       window.getCameraPos(), window.getCameraForward(), window.getCameraRight(), window.getCameraUp()
#       window.getCameraNearClipPlaneRight(), window.getCameraNearClipPlaneUp(), window.getCameraNearClipDst()
#       window.toCameraSpace(...), window.toWorldSpaceFromCameraSpace(...)
#   - spawn a star with: Star(window, spawnPosition)
def spawnStars(window: WindowSpace3D, numStarsCurrent: int):
    #TODO
    pass

# update your camera in this method
#   - you are provided a subset of button state (either pressed on not pressed)
#       for example, wasdBtns[0] is True when 'w' is pressed and wasdBtns[1] is True when '2' is pressed.
#                    likewise, shiftCtrlBtns[0] is True when the shift key is pressed
#   - you can query the current camera state from window, and then set it using window.setCameraPos(...) & window.setCameraOrient(...)
#   - start with only the camera position, the mouse look with the right mouse button is hooked up
#   - camVel is probably useful to you, I've made a global velocity value for you here, feel free to use it...or not.
camVel = v3_zero()
def updateCamera(window: WindowSpace3D, wasdBtns: List[bool], shiftCtrlBtns: List[bool], deltaTime: float):
    global camVel
    #TODO
    pass

# todo: student adds stars out front of the camera
# todo: student culls stars behind the camera
# todo: student does camera rotation from mouse delta & camera position based on WASD

####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
########################## EXCEPT TO REMOVE TUTORIAL GAME CONFIG ARGUMENT  #########################
####################################################################################################
WindowSpace3D("Lab 17: Star Field 3D!", spawnStarsFn = spawnStars, updateCameraFn = updateCamera).runGameLoop()