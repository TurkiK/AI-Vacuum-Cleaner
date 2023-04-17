import numpy as np
import time

#Menu interaction variables.
choice = 5
stepByStep = False

#Agent variable. 1 = Simple Reflex Agent, 2 = Table-Driven Agent.
agent = 0
state = ""

#Performance measure variables.
iterations = 0 #Cells checked + walls avoided. or the number of times the SimpleReflexAgent function was called.
wallsEncountered = 0 #Number of times the agent has avoided a wall; Wall may be # obstacle or matrix boundary.
cellsChecked = 0 #Number of times the agent has checked a cell.
cellsCleaned = 0 #Number of times the agent has cleaned a cell.
stepsMade = 0 #Number of steps the agent has made.
stepsTaken = [] #List of steps taken to clean each cell.

#World matrix.
world = []
prevWorld = []

#Look up table for the table-driven agent containing the actions for each state.
lookup_table = {
    '0000FFFF': ['up', 'right', 'down', 'left'],
    '0000FFFT': ['left'],
    '0000FFTF': ['down'],
    '0000FTFF': ['right'],
    '0000TFFF': ['up'],
    '0000TTFF': ['up', 'right'],
    '0000FFTT': ['down', 'left'],
    '0000FTTF': ['right', 'down'],
    '0000FTFT': ['right', 'left'],
    '0000TFFT': ['up', 'left'],
    '0000TFTF': ['up', 'down'],
    '0000TTTF': ['up', 'right', 'down'],
    '0000TTFT': ['up', 'right', 'left'],
    '0000TFTT': ['up', 'down', 'left'],
    '0000FTTT': ['right', 'down', 'left'],
    '0001FFFF': ['up', 'right', 'down'],
    '0001FFTF': ['down'],
    '0001FTFF': ['right'],
    '0001TFFF': ['up'],
    '0001FTTF': ['right', 'down'],
    '0001TTFF': ['up', 'right'],
    '0001TFTF': ['up', 'down'],
    '0001TTTF': ['up', 'right', 'down'],
    '0010FFFF': ['up', 'right', 'left'],
    '0010FFFT': ['left'],
    '0010FTFF': ['right'],
    '0010TFFF': ['up'],
    '0010TFFT': ['up', 'left'],
    '0010TTFF': ['up', 'right'],
    '0010FTFT': ['right', 'left'],
    '0010TTFT': ['up', 'right', 'left'],
    '0011FFFF': ['up', 'right'],
    '0011TFFF': ['up'],
    '0011FTFF': ['right'],
    '0011TTFF': ['up', 'right'],
    '0100FFFF': ['up', 'down', 'left'],
    '0100TFFF': ['up'],
    '0100FFTF': ['down'],
    '0100FFFT': ['left'],
    '0100TFFT': ['up', 'left'],
    '0100TFTF': ['up', 'down'],
    '0100FFTT': ['down', 'left'],
    '0100TFTT': ['up', 'down', 'left'],
    '0101FFFF': ['up', 'down'],
    '0101TFFF': ['up'],
    '0101FFTF': ['down'],
    '0101TFTF': ['up', 'down'],
    '0110FFFF': ['up', 'left'],
    '0110TFFF': ['up'],
    '0110FFFT': ['left'],
    '0110TFFT': ['up', 'left'],
    '0111FFFF': ['up'],
    '0111TFFF': ['up'],
    '1000FFFF': ['right', 'down', 'left'],
    '1000FTFF': ['right'],
    '1000FFTF': ['down'],
    '1000FFFT': ['left'],
    '1000FTTF': ['right', 'down'],
    '1000FTFT': ['right', 'left'],
    '1000FFTT': ['down', 'left'],
    '1000FTTT': ['right', 'down', 'left'],
    '1001FFFF': ['right', 'down'],
    '1001FTFF': ['right'],
    '1001FFTF': ['down'],
    '1001FTTF': ['right', 'down'],
    '1010FFFF': ['right', 'left'],
    '1010FTFF': ['right'],
    '1010FFFT': ['left'],
    '1010FTFT': ['right', 'left'],
    '1011FFFF': ['right'],
    '1011FTFF': ['right'],
    '1100FFFF': ['down', 'left'],
    '1100FFTF': ['down'],
    '1100FFFT': ['left'],
    '1100FFTT': ['down', 'left'],
    '1101FFFF': ['down'],
    '1101FFTF': ['down'],
    '1110FFFF': ['left'],
    '1110FFFT': ['left'],
    '1111FFFF': []
}

#A function to display the performance of the agent during the last world clean up.
def getScore():
    global iterations, wallsEncountered, cellsChecked, cellsCleaned, stepsTaken, stepsMade
    print("All dirt has been cleaned!\n")
    print("Performance Measures: ")
    if agent == 1:
        print("Agent: Simple Reflex Agent")
    else:
        print("Agent: Table-Driven Agent")
    print("Total Iterations: ", iterations)
    print("Steps Made: ", stepsMade) 
    print("Cells Checked: ", cellsChecked) 
    print("Walls Encountered: ", wallsEncountered) 
    print("Cells Cleaned: ", cellsCleaned) 
    print("Steps dirt was found at: ", stepsTaken) 
    print("Average steps to clean dirt: ", sum(stepsTaken) / len(stepsTaken), "\n") #Average steps taken to clean each cell.

    #Resets the performance measure variables.
    iterations = 0
    cellsChecked = 0
    cellsCleaned = 0
    wallsEncountered = 0
    stepsMade = 0
    stepsTaken = []


#A function to display the world with the row and column numbers.
def displayWorld(world):
    for i in range(len(world)+1):
        if i != 0:
            print(' ',i-1 ,end = ' ')
        else :
            print(' ', end = ' ')
    print()
    for rowNumber , row in enumerate(world):
        print(rowNumber ,row)


#A function to generate random dirt and walls. Entity is either '*' dirt or '#' wall.
def RandGen(max, entity):
    #Checks if the max number of dirt or walls has been reached.
    if max == 0:
        return
    
    #Generates a random row and column.
    row, col = np.random.randint(0, 10, 2)
    
    #Checks if the space is empty and if it is, it places the dirt or wall.
    if world[row][col] == ' ':
        world[row][col] = entity
        max -= 1

    #Recursively calls the function again until the max number of dirt or walls has been reached.
    RandGen(max, entity) 


#A function to selectively generate dirt in the world.
def SelectGen():
        global prevWorld
        #Pick the number of dirt the user wants.
        dirt = int(input("(?) Enter the number of dirt: "))
        
        displayWorld(world)
        #Generates the dirt one by one through row and column.
        while(dirt > 0):
            location = list(map(int,input("(?) Enter the desired location of the dirt, row and column seperated by space: ").split(' ')))
            if location[0] >= 0 and location[0] < 10 and location[1] >= 0 and location[1] < 10:
                world[location[0]][location[1]] = '*'
                displayWorld(world)
            else:
                print("(!) Empty space placed.")
                continue
            dirt -= 1

        #Randomly generate the walls.
        walls = int(input("(?) Enter the number of walls: "))
        RandGen(walls, '#')

        #Places the agent at the top left corner.
        world[0][0] = 'A'

        #Checks if there is more dirt than empty space.
        if np.count_nonzero(world == '*') > np.count_nonzero(world == ' '):
            print("\n(!) Dirt is more than empty space. Try again.\n")
            return
        else:
            prevWorld = world.copy()
            displayWorld(world)
            print("World generated!\n")
            return

#A function that randomly generates a world given the number of dirt and walls.
def RandWorld():
        global prevWorld
        dirt = int(input("(?) Enter the number of dirt: "))
        RandGen(dirt, '*')
        walls = int(input("(?) Enter the number of walls: "))
        RandGen(walls, '#')

        #Places the agent at the top left corner.
        world[0][0] = 'A'

        #Checks if there is more dirt than empty space.
        if np.count_nonzero(world == '*') > np.count_nonzero(world == ' '):
            print("\n(!) Dirt is more than empty space. Try again.\n")
            return
        else:
            prevWorld = world.copy()
            displayWorld(world)
            print("World generated!\n")
            return


#A function to move the agent up.
def moveUp():
    global wallsEncountered, stepsMade
    #Finds the agent's position.
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]
    #Checks if the agent is not at the top of the world and if the space above the agent is not a wall.
    if world[row - 1][col] != '#':
        if isDirty(row - 1, col):
            world[row][col] = ' '
            suck(row - 1, col)
        else:
            world[row][col] = ' '
            world[row - 1][col] = 'A'
        stepsMade += 1
    else:
        wallsEncountered += 1


#A function to move the agent down.
def moveDown():
    global wallsEncountered, stepsMade
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]
    #Checks if the agent is not at the bottom of the world and if the space below the agent is not a wall.
    if world[row + 1][col] != '#':
        if isDirty(row + 1, col):
            world[row][col] = ' '
            suck(row + 1, col)
        else:
            world[row][col] = ' '
            world[row + 1][col] = 'A'
        stepsMade += 1
    else:
        wallsEncountered += 1


#A function to move the agent left.
def moveLeft():
    global wallsEncountered, stepsMade
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]
    #Checks if the agent is not at the left of the world and if the space to the left of the agent is not a wall.
    if world[row][col - 1] != '#':
        if isDirty(row, col - 1):
            world[row][col] = ' '
            suck(row, col - 1)
        else:
            world[row][col] = ' '
            world[row][col - 1] = 'A'
        stepsMade += 1
    else:
        wallsEncountered += 1


#A function to move the agent right.
def moveRight():
    global wallsEncountered, stepsMade
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]
    #Checks if the agent is not at the right of the world and if the space to the right of the agent is not a wall.
    if world[row][col + 1] != '#':
        if isDirty(row, col + 1):
            world[row][col] = ' '
            suck(row, col + 1)
        else:
            world[row][col] = ' '
            world[row][col + 1] = 'A'
        stepsMade += 1
    else:
        wallsEncountered += 1


#A function to check if the space is dirty.
def isDirty(row, col):
    global cellsChecked
    cellsChecked += 1
    if row < 0 or row > 9 or col < 0 or col > 9:
        return False
    
    if world[row][col] == '*':
        return True
    else:
        return False

#Asks the user if they want to see each step of the process.
def showSteps():
    global stepByStep
    choice = int(input("(?) Do you wish to show steps? (1: Yes, 2: No): "))
    if choice == 1:
        stepByStep = True
    elif choice == 2:
        stepByStep = False
    else:
        print("(!) Invalid choice. Please try again.\n")
        choice = 0


#A function to suck the dirt.
def suck(row, col):
    global cellsCleaned
    cellsCleaned += 1
    stepsTaken.append(stepsMade)
    world[row][col] = 'A'
    if stepByStep == False:
        displayWorld(world)
    print("Sucking dirt at (" + str(row) + ", " + str(col) + ")" + "..." + " Iteration: " + str(iterations) + "\n")


def move(row, col):
    global wallsEncountered
    #Generates a random number between 0 and 3.
    movement = np.random.randint(0, 4)
    if movement == 0 and row != 0:   #Checks if the agent is at the top of the world and if the action is to move up.
        moveUp()
    elif movement == 1 and row != 9: #Checks if the agent is at the bottom of the world and if the action is to move down.
        moveDown()
    elif movement == 2 and col != 0: #Checks if the agent is at the left of the world and if the action is to move left.
        moveLeft()
    elif movement == 3 and col != 9: #Checks if the agent is at the right of the world and if the action is to move right.
        moveRight()
    else:
        wallsEncountered += 1 

#A function to append the wall percepts of the table-driven agent to the state.
def AppendWalls(row, col):
    global state
    state = ""
    if row != 0 and world[row - 1, col] != '#': #Checks if the space above the agent is a wall and if the agent is not at the top of the world.
        state += '0'
    else:
        state += '1'
    if col != 9 and world[row, col + 1] != '#': #Checks if the space to the right of the agent is a wall and if the agent is not at the right of the world.
        state += '0'
    else:
        state += '1'
    if row != 9 and world[row + 1, col] != '#': #Checks if the space below the agent is a wall and if the agent is not at the bottom of the world.
        state += '0'
    else:
        state += '1'
    if col != 0 and world[row, col - 1] != '#': #Checks if the space to the left of the agent is a wall and if the agent is not at the left of the world.
        state += '0'
    else:
        state += '1'

#A function to append the dirt percepts of the table-driven agent to the state.
def AppendDirt(row, col):
    global state
    if isDirty(row - 1, col) and row != 0: #Checks if the space above the agent is dirty and if the agent is not at the top of the world.
        state += 'T'
    else:
        state += 'F'
    if isDirty(row, col+1) and col != 9: #Checks if the space to the right of the agent is dirty and if the agent is not at the right of the world.
        state += 'T'
    else:
        state += 'F'
    if isDirty(row + 1, col) and row != 9: #Checks if the space below the agent is dirty and if the agent is not at the bottom of the world.
        state += 'T'
    else:
        state += 'F'
    if isDirty(row, col-1) and col != 0: #Checks if the space to the left of the agent is dirty and if the agent is not at the left of the world.
        state += 'T'
    else:
        state += 'F'

#A function to generate a random action for the Simple Reflex Agent.
def SimpleReflexAgent():
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]

    move(row, col)


#A function that acts as a table driven agent.
def TableDrivenAgent():
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]
    AppendWalls(row, col)
    AppendDirt(row, col)
    if state in lookup_table:
        action = lookup_table[state][np.random.randint(0, len(lookup_table[state]))]
        if action == 'up':
            moveUp()
        elif action == 'down':
            moveDown()
        elif action == 'left':
            moveLeft()
        elif action == 'right':
            moveRight()
    else:
        print("(!) No action found for " + state)
        return


while choice != 3:
    print("\n1: Start simulation.\n2: Generate a world.\n3: Quit")
    choice = int(input("(?) Enter a number: "))
    print("\n")
    #Starts the agent.
    if choice == 1:
        #Picks an agent.
        agent = int(input("1: Simple Reflex Agent\n2: Table-Driven Agent\nEnter a number: "))
        print("\n")

        #Checks if the agent is the Simple Reflex Agent.
        if agent == 1 and world != []:
            showSteps()
            while np.count_nonzero(world == '*') > 0:
                SimpleReflexAgent()
                if stepByStep == True:
                    displayWorld(world)
                    print("\n")
                    time.sleep(0.125)
                iterations += 1
            if len(stepsTaken) == 0:
                print("(!) The agent did not clean any dirt.\n")
            else:
                displayWorld(world)
                getScore()
                world = []
        #Checks if the agent is the Table-Driven Agent.
        elif agent == 2 and world != []:
            showSteps()
            while np.count_nonzero(world == '*') > 0:
                TableDrivenAgent()
                if stepByStep == True:
                    displayWorld(world)
                    print("\n")
                    time.sleep(0.125)
                iterations += 1
            if len(stepsTaken) == 0:
                print("(!) The agent did not clean any dirt.\n")
            else:
                displayWorld(world)
                getScore()
                world = []
        else:
            print("(!) There seems to be an error, check your input and make sure a world has been generated first!\n")
    #Generates the world.
    elif choice == 2:
        #Initializes the world with empty spaces.
        world = np.full((10,10), ' ')

        choice = int(input("1: Randomly generate a world.\n2: Generate a world with select dirt locations.\n3: Previous world.\nEnter a number: "))
        if choice == 1:
            RandWorld()
        elif choice == 2:
            SelectGen()
        elif choice == 3:
            world = prevWorld.copy()
            choice = 0
        else:
            print("(!) Invalid input.\n")
            choice = 0
    elif choice == 3:
        print("Goodbye!\n")