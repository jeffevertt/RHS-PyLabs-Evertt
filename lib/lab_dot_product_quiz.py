import numpy as np
import time
import random
import asyncio

from lib.canvas import Canvas
from lib.utils import *

# one decimal place at least
def compareDotProducts(a, b):
    return int(a * 10) == int(b * 10)

async def runLab_dotProductQuiz():
    # create the canvas
    canvas = Canvas("Determine the dot product of the two vectors.", 
                    width = 400, height = 400,
                    gridPixelsPerUnit = 50,
                    textBoxConfig = { 'placeholder': 'dot product value', 
                                      'prompt': 'Dot Product: ' } )
    canvas.display()
    
    # consts
    numberOfQuestions = 10
    timePerQuestion = 5
    
    # locals
    v0 = v2(1, 0)
    v1 = v2(0, 1)
    
    # pick vector values
    def pickVectors(levelIndex):
        if levelIndex == 0:
            v0 = v2(1,0) * random.randint(-2, 2)
            v1 = v2(1,0) * random.randint(-1, 1)
            while length(v0) == 0 or length(v1) == 0 or np.array_equal(v0, v1):
                v1 = v2(1,0) * random.randint(-1, 1)
        elif levelIndex <= 3:
            v0 = random.choice([v2_left(), v2_right(), v2_up(), v2_down()])
            v1 = random.choice([v2_left(), v2_right(), v2_up(), v2_down()])
            while np.array_equal(v0, v1):
                v1 = random.choice([v2_left(), v2_right(), v2_up(), v2_down()])
        elif levelIndex <= 6:
            v0 = random.choice([v2_left(), v2_right(), v2_up(), v2_down(), v2(0.707,0.707), v2(0.707,-0.707)]) * 2
            v1 = random.choice([v2_left(), v2_right(), v2_up(), v2_down()]) * random.randint(1, 2)
            while np.array_equal(v0, v1):
                v1 = random.choice([v2_left(), v2_right(), v2_up(), v2_down()]) * random.randint(1, 2)
        else:
            v0 = random.choice([v2(0.707,0.707), v2(0.707,-0.707), v2(-0.707,-0.707), v2(-0.707,0.707)]) * random.randint(1, 2)
            v1 = random.choice([v2_left(), v2_right(), v2_up(), v2_down()]) * random.randint(1, 2)
            while np.array_equal(v0, v1):
                v1 = random.choice([v2_left(), v2_right(), v2_up(), v2_down()]) * random.randint(1, 2)
        return ( v0, v1 )
    
    # render CB
    def drawExtras():
        canvas.drawVector(v2_zero(), v0, 'red', 6)
        canvas.drawVector(v2_zero(), v1, 'blue', 4)
    canvas.setPreObjCB(drawExtras)
    
    # loop through all the questions
    for levelIndex in range(numberOfQuestions):
        # update title
        canvas.setTitle(f"Question: {levelIndex + 1} of {numberOfQuestions}")
        
        # pick values for the vectors
        v0, v1 = pickVectors(levelIndex)
        
        # kick off the question & countdown timer
        startTime = time.time()
        endTime = startTime + timePerQuestion
        curTime = time.time()
        while curTime < endTime:
            # update subtitle
            canvas.setSubTitle(f"Time remaining: {endTime - curTime:.2f}")
            
            # update
            canvas.update()
            canvas.drawWorld()
            
            # new time
            await asyncio.sleep(0.01)
            curTime = time.time()
        
        # glab the guess & clear the input text
        guess = toFloat(canvas.inputTextBox.value, -1000)
        canvas.inputTextBox.value = ''
        
        # check for incorrect
        if not compareDotProducts(guess, v0 @ v1):
            canvas.setResult(False)
            canvas.log(f"Sorry, that's not right. The correct answer was  {v0 @ v1:0.2f}")
            return
        
        # log it
        canvas.log(f"Question {levelIndex+1} correct: {guess}!")
            
    # message
    canvas.log("Well done - you win!!!")
    
    # if we made it this far, then we win!
    canvas.setResult(True)