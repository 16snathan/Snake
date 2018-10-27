# Shiva Nathan (svnathan)
#15-112 G 
#3 March 2017
#snake modified from events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
import random

####################################
# customize these functions
####################################

def init(data):
    data.rows = 10
    data.cols = 10
    data.margins = 5
    data.snake = [(data.rows//2,data.cols//2)]
    data.direction = (0,1) #rows, cols
    data.timerDelay = 250
    data.gameOver = False
    data.paused = True
    placeFood(data)

def mousePressed(event, data):
    data.paused = False

def keyPressed(event, data):
    if event.keysym == 'r': init(data)
    if event.keysym == 'p':
        data.paused = not data.paused
    
    if data.gameOver == True: return
    if event.keysym == "Up": data.direction = (-1,0)
    elif event.keysym == "Down": data.direction = (1,0)
    elif event.keysym == "Right": data.direction = (0,1)
    elif event.keysym == "Left": data.direction = (0,-1)

def timerFired(data):
    if (data.paused or data.gameOver): return
    takeStep(data)

def redrawAll(canvas, data):
    drawBoard(canvas,data)
    drawFood(canvas,data)
    drawSnake(canvas,data)
    drawGameOver(canvas,data)
    pass
    
def takeStep(data):
    (dRow,dCol) = data.direction
    (headRow,headCol) = data.snake[0]
    (newRow,newCol) = (headRow + dRow, headCol + dCol)
    if((newRow < 0) or (newRow >= data.rows)
    or (newCol < 0) or (newCol >= data.cols)
    or ((newRow,newCol) in data.snake)):
        data.gameOver = True
    else:
        data.snake.insert(0,(newRow,newCol))
        if data.snake[0] == data.foodPosition:
            placeFood(data)
        else:
            data.snake.pop()

def placeFood(data):
    data.foodPosition = None
    row = random.randint(0,data.rows-1)
    col = random.randint(0,data.cols-1)
    while (row,col) in data.snake:
        row = random.randint(0,data.rows-1)
        col = random.randint(0,data.cols-1)
    data.foodPosition = (row,col)

def drawBoard(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            (left,top,right,bottom) = getCellBounds(row,col,data)
            canvas.create_rectangle(left,top,right,bottom)
            
def drawFood(canvas,data):
    (row,col) = data.foodPosition
    (left,top,right,bottom) = getCellBounds(row,col,data)
    canvas.create_oval(left,top,right,bottom,fill = "green")
    
def drawSnake(canvas,data):
    for (row,col) in data.snake:
        (left,top,right,bottom) = getCellBounds(row,col,data)
        canvas.create_oval(left,top,right,bottom,fill = "blue")
        
def drawGameOver(canvas,data):
    if (data.gameOver == True):
        canvas.create_text(data.width//2, data.height//2, text = "GAME OVER",
            fill = "black", font = "Arial 20 bold")
        

def getCellBounds(row,col,data):
    width = data.width - 2*data.margins
    height = data.height - 2*data.margins
    cellWidth = width // data.cols
    cellHeight = width // data.rows
    left = data.margins + col*cellWidth
    top = data.margins + row*cellHeight
    right = left + cellWidth
    bottom = top + cellWidth
    return (left, top, right, bottom)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(300, 300)