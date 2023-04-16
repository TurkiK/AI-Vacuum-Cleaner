import numpy as np
import time

#Menu interaction variable.
choice = 5
stepByStep = False

#Agent variable. 1 = Simple Reflex Agent, 2 = Table-Driven Agent.
agent = 0

#Number of times the agent has moved.
iterations = 0

#World matrix.
world = []

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

        #Generates the dirt one by one through row and column.
        while(dirt > 0):
            location = list(map(int,input("Enter the desired location of the dirt, row and column seperated by space: ").split(' ')))
            if location[0] >= 0 and location[0] < 10 and location[1] >= 0 and location[1] < 10:
                world[location[0]][location[1]] = '*'
                print(world)
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
            print(world)
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
            print(world)
            print("World generated.\n")
            return

#A function to move the agent up.
def moveUp():
    #Finds the agent's position.
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]
    #Checks if the agent is not at the top of the world and if the space above the agent is not a wall.
    if row != 0 and world[row - 1][col] != '#':
        if isDirty(row - 1, col):
            world[row][col] = ' '
            suck(row - 1, col)
        else:
            world[row][col] = ' '
            world[row - 1][col] = 'A'

#A function to move the agent down.
def moveDown():
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]
    #Checks if the agent is not at the bottom of the world and if the space below the agent is not a wall.
    if row != 9 and world[row + 1][col] != '#':
        if isDirty(row + 1, col):
            world[row][col] = ' '
            suck(row + 1, col)
        else:
            world[row][col] = ' '
            world[row + 1][col] = 'A'

#A function to move the agent left.
def moveLeft():
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]
    #Checks if the agent is not at the left of the world and if the space to the left of the agent is not a wall.
    if col != 0 and world[row][col - 1] != '#':
        if isDirty(row, col - 1):
            world[row][col] = ' '
            suck(row, col - 1)
        else:
            world[row][col] = ' '
            world[row][col - 1] = 'A'

#A function to move the agent right.
def moveRight():
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]
    #Checks if the agent is not at the right of the world and if the space to the right of the agent is not a wall.
    if col != 9 and world[row][col + 1] != '#':
        if isDirty(row, col + 1):
            world[row][col] = ' '
            suck(row, col + 1)
        else:
            world[row][col] = ' '
            world[row][col + 1] = 'A'

#A function to check if the space is dirty.
def isDirty(row, col):
    if world[row][col] == '*':
        return True
    else:
        return False

#A function to suck the dirt.
def suck(row, col):
    world[row][col] = 'A'
    if stepByStep == False:
        print(world)
    print("Sucking dirt at (" + str(row) + ", " + str(col) + ")" + "..." + " Iteration: " + str(iterations) + "\n")

def move(row, col):
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

#A function to generate a random action for the Simple Reflex Agent.
def SimpleReflexAgent():
    row, col = np.where(world == 'A')
    row, col = row[0], col[0]

    move(row, col)

while choice != 4:
    print("1: Start sucking dirt.\n2: Generate the world.\n3: Pick an agent.\n4: Quit")
    choice = int(input("Enter a number: "))
    print("\n")
    #Starts the agent.
    if choice == 1:
        #Asks the user if they want to see each step of the process.
        choice = int(input("Do you wish to show steps? (1: Yes, 2: No): "))
        if choice == 1:
            stepByStep = True
        else:
            stepByStep = False

        #Checks if the agent is the Simple Reflex Agent.
        if agent == 1:
            while np.count_nonzero(world == '*') > 0:
                SimpleReflexAgent()
                iterations += 1
                if stepByStep == True:
                    print(world)
                    print("\n")
                    time.sleep(0.125)
            print(world)
            print("All dirt has been cleaned, in ", iterations ," iterations!\n")
            iterations = 0
        #Checks if the agent is the Table-Driven Agent.
        elif agent == 2:
            print("Table-Driven Agent\n")
        else:
            print("No agent selected.\n")
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
    #Picks an agent.
    elif choice == 3:
        agent = int(input("1: Simple Reflex Agent\n2: Table-Driven Agent\nEnter a number: "))
        print("\n")
    elif choice == 4:
        print("Goodbye!\n")
    