import numpy as np
import time

#Menu interaction variables.
choice = 5
stepByStep = False

#Agent variable. 1 = Simple Reflex Agent, 2 = Table-Driven Agent.
agent = 0

#Performance measure variables.
iterations = 0 #Cells checked + walls avoided. or the number of times the SimpleReflexAgent function was called.
wallAvoided = 0 #Number of times the agent has avoided a wall; Wall may be # obstacle or matrix boundary.
cellsChecked = 0 #Number of times the agent has checked a cell.
cellsCleaned = 0 #Number of times the agent has cleaned a cell.
stepsTaken = [] #List of steps taken to clean each cell.

#World matrix.
world = []

#A function to display the performance of the agent during the last world clean up.
def performanceMeasure():
    global iterations, wallAvoided, cellsChecked, cellsCleaned, stepsTaken
    print("All dirt has been cleaned!\n")
    print("Performance Measures: ")
    if agent == 1:
        print("Agent: Simple Reflex Agent")
    else:
        print("Agent: Table-Driven Agent")
    print("Total Iterations: ", iterations) 
    print("Cells Checked: ", cellsChecked) 
    print("Walls Avoided: ", wallAvoided) 
    print("Cells Cleaned: ", cellsCleaned) 
    print("Steps dirt was found at: ", stepsTaken) 
    print("Average steps to clean dirt: ", sum(stepsTaken) / len(stepsTaken), "\n") #Average steps taken to clean each cell.

    #Resets the performance measure variables.
    iterations = 0
    cellsChecked = 0
    cellsCleaned = 0
    wallAvoided = 0
    stepsTaken = []


lookup_table = {

    '00000101': ['up','left'],

    '00000000': ['up', 'right', 'down', 'left'],
    '00000001': ['left'],
    '00000010': ['down'],
    '00000100': ['right'],
    '00001000': ['up'],

    '00010000': ['up', 'right', 'down'],
    '00010010': ['down'],
    '00010100': ['right'],
    '00011000': ['up'],

    '00100000': ['up', 'right', 'left'],
    '00100001': ['left'],
    '00100100': ['right'],
    '00101000': ['up'],

    '00110000': ['up', 'right'],
    '00111000': ['up'],
    '00110100': ['right'],

    '01000000': ['up', 'down', 'left'],
    '01001000': ['up'],
    '01000010': ['down'],
    '01000001': ['left'],

    '01010000': ['up', 'down'],
    '01011000': ['up'],
    '01010010': ['down'],
    
    '01100000': ['up', 'left'],
    '01101000': ['up'],
    '01100001': ['left'],

    '01110000': ['up'],
    '01111000': ['up'],

    '10000000': ['right', 'down', 'left'],
    '10000100': ['right'],
    '10000010': ['down'],
    '10000001': ['left'],

    '10010000': ['right', 'down'],
    '10010100': ['right'],
    '10010010': ['down'],

    '10100000': ['right', 'left'],
    '10100100': ['right'],
    '10100001': ['left'],

    '10110000': ['right'],
    '10110100': ['right'],

    '11000000': ['down', 'left'],
    '11000010': ['down'],
    '11000001': ['left'],

    '11010000': ['down'],
    '11010010': ['down'],

    '11100000': ['left'],
    '11100001': ['left'],

    '11110000': []

}

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


def SelectGen():
        #Pick the number of dirt the user wants.
        dirt = int(input("How many dirt do you want?"))
        
        displayWorld(world)
        #Generates the dirt one by one through row and column.
        while(dirt > 0):
            location = list(map(int,input("Enter the desired location of the dirt, row and column seperated by space: ").split(' ')))
            if location[0] >= 0 and location[0] < 10 and location[1] >= 0 and location[1] < 10:
                world[location[0]][location[1]] = '*'
                displayWorld(world)
            else:
                print("Empty space placed.")
                continue
            dirt -= 1

        #Randomly generate the walls.
        walls = int(input("Enter the number of walls: "))
        RandGen(walls, '#')

        #Places the agent at the top left corner.
        world[0][0] = 'A'

        #Checks if there is more dirt than empty space.
        if np.count_nonzero(world == '*') > np.count_nonzero(world == ' '):
            print("\nDirt is more than empty space. Try again.\n")
            return
        else:
            displayWorld(world)
            print("World generated.\n")
            return


def RandWorld():
        #Generates the dirt and walls.
        dirt = int(input("Enter the number of dirt: "))
        RandGen(dirt, '*')
        walls = int(input("Enter the number of walls: "))
        RandGen(walls, '#')

        #Places the agent at the top left corner.
        world[0][0] = 'A'

        #Checks if there is more dirt than empty space.
        if np.count_nonzero(world == '*') > np.count_nonzero(world == ' '):
            print("\nDirt is more than empty space. Try again.\n")
            return
        else:
            displayWorld(world)
            print("World generated.\n")
            return


#A function to move the agent up.
def moveUp():
    global wallAvoided
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
    else:
        wallAvoided += 1


#A function to move the agent down.
def moveDown():
    global wallAvoided
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
    else:
        wallAvoided += 1


#A function to move the agent left.
def moveLeft():
    global wallAvoided
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
    else:
        wallAvoided += 1


#A function to move the agent right.
def moveRight():
    global wallAvoided
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
    else:
        wallAvoided += 1


#A function to check if the space is dirty.
def isDirty(row, col):
    global cellsChecked
    cellsChecked += 1
    if world[row][col] == '*':
        return True
    else:
        return False


#A function to suck the dirt.
def suck(row, col):
    global cellsCleaned, cellsChecked
    cellsCleaned += 1
    stepsTaken.append(cellsChecked)
    world[row][col] = 'A'
    if stepByStep == False:
        displayWorld(world)
    print("Sucking dirt at (" + str(row) + ", " + str(col) + ")" + "..." + " Iteration: " + str(iterations) + "\n")


def move(row, col):
    global wallAvoided
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
        wallAvoided += 1


def AppendToA():
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]
    a = ''
    if row - 1 != world[row - 1, col] or row != 0:
        a += '0'
    else:
        a += '1'
    if row + 1 != '#' or row != 9:
        a += '0'
    else:
        a += '1'
    if col - 1 != world[row, col - 1] or col != 0:
        a += '0'
    else:
        a += '1'
    if col + 1 != '#' or col != 9:
        a += '0'
    else:
        a += '1'
    return a


def AppendToB():
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]
    b = ''
    if row - 1 != world[row - 1, col] or row != 0:
        b += '0'
    else:
        b += '1'
    if row + 1 == '*' or row != 9:
        b += '0'
    else:
        b += '1'
    if col - 1 != world[row, col - 1] or col != 0:
        b += '0'
    else:
        b += '1'
    if col + 1 == '*' or col != 9:
        b += '0'
    else:
        b += '1'
    return b


#A function to generate a random action for the Simple Reflex Agent.
def SimpleReflexAgent():
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]

    move(row, col)


#A function that acts as a table driven agent.
def TableDrivenAgent():
    a = AppendToA()
    b = AppendToB()
    a+=b
    if a in lookup_table:
        action = lookup_table[a][np.random.randint(0, len(lookup_table[a]))]
        if action == 'up':
            moveUp()
        elif action == 'down':
            moveDown()
        elif action == 'left':
            moveLeft()
        elif action == 'right':
            moveRight()
    else:
        print("Error: No action found for " + a)
        return



while choice != 3:
    print("1: Start sucking dirt.\n2: Generate the world.\n3: Quit")
    choice = int(input("Enter a number: "))
    print("\n")
    #Starts the agent.
    if choice == 1:
        #Picks an agent.
        agent = int(input("1: Simple Reflex Agent\n2: Table-Driven Agent\nEnter a number: "))
        print("\n")

        #Asks the user if they want to see each step of the process.
        choice = int(input("Do you wish to show steps? (1: Yes, 2: No): "))
        if choice == 1:
            stepByStep = True
        else:
            stepByStep = False

        #Checks if the agent is the Simple Reflex Agent.
        if agent == 1 and world != []:
            while np.count_nonzero(world == '*') > 0:
                SimpleReflexAgent()
                if stepByStep == True:
                    displayWorld(world)
                    print("\n")
                    time.sleep(0.125)
                iterations += 1
            displayWorld(world)
            performanceMeasure()
        #Checks if the agent is the Table-Driven Agent.
        elif agent == 2:
            while np.count_nonzero(world == '*') > 0:
                TableDrivenAgent()
                if stepByStep == True:
                    displayWorld(world)
                    print("\n")
                    time.sleep(0.125)
                iterations += 1
            displayWorld(world)
            performanceMeasure()
        else:
            print("You must generate a world first.\n")
    #Generates the world.
    elif choice == 2:
        #Initializes the world with empty spaces.
        world = np.full((10,10), ' ')

        choice = int(input("1: Generate a random world.\n2: Generate a custom world.\nEnter a number: "))
        if choice == 1:
            RandWorld()
        elif choice == 2:
            SelectGen()
        else:
            print("Invalid input.\n")
    elif choice == 3:
        print("Goodbye!\n")
    