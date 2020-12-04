# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pygame
import random
import numpy as np
import Q_learn as Q



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
pygame.init()  # Initialize everything at the start

# Original values for both is 600 by 400
dis_width = 100  # Width and height of the screen
dis_height = 100

dis = pygame.display.set_mode((dis_width, dis_height))  # Set setting for the display
pygame.display.set_caption('Snake Game RL')  # Caption for window

blue = (0, 0, 255)  # RGB value for blue
red = (255, 0, 0)  # RGB value for red
white = (255, 255, 255)  # RGB value for white
green = (0, 255, 0)  # RGB value for green
black = (0, 0, 0)  # RGB value for black

x1 = 50  # inital value for x
y1 = 50  # initial value for y

x1_change = 0
y1_change = 0
snake_block = 10  # Size of the snake
snake_speed = 10  # Amount of frames per second (original is 15)

font_style = pygame.font.SysFont(None, 50)


def check_food(obstacle_array):
    obstacles = obstacle_array.shape
    num_obstacles = (obstacles[0] / 2)

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # print("FOOD X ", foodx)
    # print("FOOD Y ", foody)

    while (True):
        temp = []
        for a in range(int(num_obstacles)):
            if (int(obstacle_array[a * 2]) == foodx and int(obstacle_array[a * 2 + 1]) == foody):
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                temp = [foodx, foody]
        temp.append(foodx)
        temp.append(foody)
        # print("TEMP", temp)
        # print("FOOD X ", foodx)
        # print("FOOD Y ", foody)
        return temp


def our_snake(snake_block, snake_list_np):  # Extend the snake

    row = snake_list_np.shape
    a = (row[0] / 2)

    for b in range(int(a)):
        # print("B values", snake_list_np[b*2], " ", snake_list_np[b*2+1])
        pygame.draw.rect(dis, black, [snake_list_np[b * 2], snake_list_np[b * 2 + 1], snake_block, snake_block])
    # for a in snake_list:
    #    print("A value in our_snake",a)
    #    pygame.draw.rect(dis,black,[a[0],a[1],snake_block,snake_block])


def message(msg):  # Function for the display output of game over
    mesg = font_style.render(msg, True, red)
    dis.blit(mesg, [0, 100])


pygame.display.update()  # Update used to update any parameters passed onto the screen
game_over = False  # Bool value that indicates if game should end
game_close = False
clock = pygame.time.Clock()



def game_loop_Q():
    game_over = False
    game_close = False

    x1 = dis_width / 2  # inital value for x
    y1 = dis_height / 2  # initial value for y

    x1_change = 0  # x and y values to be added to x and y
    y1_change = 0

    # print("HIT1")

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    snake_list = []  # Contains the extended snake including head
    snake_length = 1  # Inital length of snake

    snake_list_np = np.array([])

    snake_Head = [x1, y1]

    moveSinceScore = 0

    while (not game_over):  # The game and display updates happen here


        for event in pygame.event.get():  # For input during game
            # print(event)  # For every input print it out
            if event.type == pygame.QUIT:  # In the case that anything input attempts to close window
                game_over = True  # Set game_over to true

            ############    AGENT ACTION SHOULD BE DETERMINED BY HERE   ############
            ############    OR BEFORE THE GAME_CLOSE LOOP IS ENTERED   ############
        params = {
            'food_posx': foodx,
            'food_posy': foody,
            'snake_pos': snake_Head,
            'snake_body': snake_list_np,
            'score': snake_length,

            'screenSizeX': dis_width,
            'screenSizeY': dis_height,
            'moveSinceScore': moveSinceScore
         }
        Q.env(params)
        shortestPath = Q.get_shortest_path(params, params['snake_pos'][0], params['snake_pos'][1])
        choosenDirection = ""
        change_to = ''

        if shortestPath == 0:
            choosenDirection == 'U'
        if shortestPath == 1:
            choosenDirection == 'D'
        if shortestPath == 2:
            choosenDirection == 'R'
        if shortestPath == 3:
            choosenDirection == 'L'



            # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN' and direction != 'LEFT' and direction != 'RIGHT':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP' and direction != 'LEFT' and direction != 'RIGHT':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT' and direction != 'UP' and direction != 'DOWN':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT' and direction != 'UP' and direction != 'DOWN':
            direction = 'RIGHT'

            # Moving the snake
        if direction == 'UP':
            snake_Head[1] += 10
        if direction == 'DOWN':
            snake_Head[1] -= 10
        if direction == 'LEFT':
            snake_list_np[0] -= 10
        if direction == 'RIGHT':
            snake_list_np[0] += 10

        ##############################################
        ######## MOVE HAS BEEN TAKEN INTO ACCOUNT FOR THE SNAKE ########################

        # if(next_move == "null") :

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:  # the case that the snake hits a border
            game_close = True

        x1 = x1 + x1_change  # Updated y and x positions of snake
        y1 = y1 + y1_change

        dis.fill(white)  # Fil display with white

        snake_Head = []  # will contains the head indexes
        snake_Head.append(x1)
        snake_Head.append(y1)

        snake_list_np = np.append(snake_list_np, snake_Head)
        row = snake_list_np.shape
        snake_len = (row[0] / 2)

        # if len(snake_list) > snake_length: #Deleting the snake that is no longer there
        if int(snake_len) > snake_length:
            # del snake_list[0]
            snake_list_np = np.delete(snake_list_np, [0, 1])

        row = snake_list_np.shape
        snake_len = (row[0] / 2)

        for a in range(int(snake_len - 1)):
            # print("For loop np ", snake_list_np[a*2], " ", snake_list_np[a*2+1])
            if (int(snake_list_np[a * 2]) == x1 and int(snake_list_np[a * 2 + 1]) == y1):
                game_close = True

        # for a in snake_list[:-1]: #Case that snake runs into itself
        #    print("For loop [:-1] ",a)
        #    #print("a in snake_list: ",a);
        #    if a == snake_Head:
        #        game_close = True

        # our_snake(snake_block,snake_list,snake_list_np)
        our_snake(snake_block, snake_list_np)

        pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block])  # Draw food pellet
        pygame.draw.rect(dis, black,
                         [x1, y1, snake_block, snake_block])  # position of rectangle 200,150 and then size 10,10

        pygame.display.update()  # Update what is in window
        ##snake Growth
        if x1 == foodx and y1 == foody:  # Case of head running into food
            # check_food(obstacle_array,foodx,foody)
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            snake_length = snake_length + 1  # Extend snake and replace old food pellet
            # print("Yummy")






    pygame.quit()
    quit()  # Uninitialize everything at the end

def game_loop_Train():
    game_over = False
    game_close = False
     # will contains the head indexes
    x1 = dis_width / 2  # initial value for x
    y1 = dis_height / 2 # initial value for y
    snake_Head = [x1, y1]
    moveCounter = 0
    moves = []
    moveSinceScore = 0
    snake_list_np = np.array([])
    snake_list_np = np.append(snake_list_np, snake_Head)
    snake_length = 1

    # print("HIT1")
    ##[120, 100]
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0


    snake_list = []  # Contains the extended snake including head



    while (not game_over):  # The game and display updates happen here

        while game_close == True:
            dis.fill(white)
            pygame.display.update()


        for event in pygame.event.get():  # For input during game
            # print(event)  # For every input print it out
            if event.type == pygame.QUIT:  # In the case that anything input attempts to close window
                game_over = True  # Set game_over to true

            ############    AGENT ACTION SHOULD BE DETERMINED BY HERE   ############
            ############    OR BEFORE THE GAME_CLOSE LOOP IS ENTERED   ############


        # if(next_move == "null") :

        #diff = [snake_Head[0] - food_x_y[0], snake_Head[1] - food_x_y[1]]
        #diff = abs(diff[0] + diff[1])
        ##############Emulation of moves#############################################################
        params = {
            'food_posx': foodx,
            'food_posy': foody,
            'snake_pos': snake_Head,
            'snake_body': snake_list_np,
            'score': snake_length,
            #'diff':diff,
            'screenSizeX': dis_width,
            'screenSizeY': dis_height,
            'moveSinceScore': moveSinceScore
            }
        Q.env(params)


        change_to = ''
        learning_rate = 0.1
        gamma = 0.2
        epsilon = 0.4



        Q.Q_train(params, epsilon, gamma, learning_rate)
        shortestPath = 0
        #shortestPath = Q.get_shortest_path(params, params['snake_pos'][0], params['snake_pos'][1])
        #print(shortestPath)
        #print(1)
    ###########################################################################################################################

        if x1 >= dis_width and x1 < 0 and y1 >= dis_height and y1 < 0:  # the case that the snake hits a border
            game_close = True

        row = snake_list_np.shape
        snake_len = (row[0] / 2)
        dis.fill(white)  # Fil display with white


        # if len(snake_list) > snake_length: #Deleting the snake that is no longer there
        if int(snake_len) > snake_length:
            # del snake_list[0]
            snake_list_np = np.delete(snake_list_np, [0, 1])

        row = snake_list_np.shape
        snake_len = (row[0] / 2)

        for a in range(int(snake_len - 1)):
            # print("For loop np ", snake_list_np[a*2], " ", snake_list_np[a*2+1])
            if (int(snake_list_np[a * 2]) == x1 and int(snake_list_np[a * 2 + 1]) == y1):
                game_close = True

        # for a in snake_list[:-1]: #Case that snake runs into itself
        #    print("For loop [:-1] ",a)
        #    #print("a in snake_list: ",a);
        #    if a == snake_Head:
        #        game_close = True

        # our_snake(snake_block,snake_list,snake_list_np)
        our_snake(snake_block, snake_list_np)

        pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block])  # Draw food pellet
        pygame.draw.rect(dis, black,
                         [x1, y1, snake_block, snake_block])  # position of rectangle 200,150 and then size 10,10

        pygame.display.update()  # Update what is in window

        if x1 == foodx and y1 == foody:  # Case of head running into food
            # check_food(obstacle_array,foodx,foody)
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            snake_length = snake_length + 1  # Extend snake and replace old food pellet
            # print("Yummy")



    pygame.quit()
    quit()  # Uninitialize everything at the end


currState = None
currAction = None
gameCounter = 0
gameScores = []



lastMoves = ""




def states(params):





    '''
    global oldMoves
    relaFoodPosition = [0,0,0,0,0,0]#np.zeros(6)
    screenBorder = [0,0,0,0,0,0]#np.zeros(6)
    bodyProx = [0,0,0,0]#np.zeros(4)
    snakeBody = []

    RelaState = ""
    ScreenState = ""
    BodyState = ""


    if ((params["food_pos"][0] - params["snake_pos"][0]) > 0):
        relaFoodPosition[0] = 1
    if((params["food_pos"][0] - params["snake_pos"][0])< 0):
        relaFoodPosition[1] = 1
    if ((params["food_pos"][0] - params["snake_pos"][0]) == 0):
        relaFoodPosition[2] = 1
    if (params["food_pos"][1] - params["snake_pos"][1]) > 0:
        relaFoodPosition[3] = 1
    if (params["food_pos"][1] - params["snake_pos"][1]) < 0:
        relaFoodPosition[4] = 1
    if ((params["food_pos"][1] - params["snake_pos"][1]) == 0):
        relaFoodPosition[5] = 1

    for i in relaFoodPosition:
        RelaState += str(i)

    if (params["screenSizeX"] - params["snake_pos"][0] == 0):
        screenBorder[0] = 1
    if (params["screenSizeX"] - params["snake_pos"][0] == params["screenSizeX"]) -10:
        screenBorder[1] = 1
    if (params["screenSizeY"] - params["snake_pos"][1] == -10):
        screenBorder[2] = 1
    if (params["screenSizeY"] - params["snake_pos"][1] < params["screenSizeY"]) - 10:
        screenBorder[3] = 1
    borderx = str(params["screenSizeX"] - params["snake_pos"][0])
    borderx2 = str(params["screenSizeX"] - params["snake_pos"][0])
    bordery = str(params["screenSizeY"] - params["snake_pos"][1])
    bordery2 = str(params["screenSizeY"] - params["snake_pos"][1])

    print("borderx:" +borderx )
    print("borderx:" +borderx2)
    print("bordery:" +bordery)
    print("bordery:" +bordery2)

    for i in screenBorder:
        ScreenState += str(i)

    next = 0
    for i in params["snake_body"]:
        if(next > 3):
            snakeBody.append(i)
        next+=1

    for bodyProx_ in snakeBody:
        if (params["snake_pos"][0] - bodyProx_[0] == 0 and params["snake_pos"][1] - bodyProx_[1] == 10):
            bodyProx[0] = 1
        if (params["snake_pos"][0] - bodyProx_[0] == 0 and params["snake_pos"][1] - bodyProx_[1] == -10):
            bodyProx[1] = 1
        if (params["snake_pos"][0] - bodyProx_[0] == 10 and params["snake_pos"][1] - bodyProx_[1] == 0):
            bodyProx[2] = 1
        if (params["snake_pos"][0] - bodyProx_[0] == -10 and params["snake_pos"][1] - bodyProx_[1] == 0):
            bodyProx[3] = 1

    for i in bodyProx:
        BodyState += str(i)
    print(params["snake_pos"])


    direct = [params["snake_pos"][0],
              params["snake_pos"][1]]
                ##(x,y)

    if (direct[0] == 10 and direct[1] == 0):
        direction = "RI"
    if (direct[0] == -10 and direct[1] == 0):
        direction = "LE"
    if(direct[0] == 0 and direct[1] == 10):
        direction = "UP"
    if (direct[0] == 0 and direct[1] == -10):
        direction = "DO"


    state = RelaState + "_" + ScreenState + "_" + BodyState + "_"
    print(state)
    return state

'''


def ValueIteration(dis_height, dis_width, snake_list_np, foodx, foody):
    rows = 2 + (dis_height / 10)
    columns = 2 + (dis_width / 10)
    num_cells = rows * columns

    # grid = np.arange(num_cells).reshape(int(rows),int(columns))
    grid = np.zeros([int(rows), int(columns)], dtype=int)

    for i in range(int(columns)):
        grid[0][int(i) - 1] = -1
        grid[int(rows) - 1][int(i) - 1] = -1

    for i in range(int(rows)):
        grid[int(i)][0] = -1
        grid[int(i)][int(columns) - 1] = -1

    row = snake_list_np.shape
    snake_len = (row[0] / 2)

    snake_headx = x1 / 10
    # snake_headx = int(snake_headx)/10
    snake_heady = y1 / 10
    # snake_heady = int(snake_heady) / 10

    # print("HEAD X : ", snake_headx, " HEAD Y : ", snake_heady)

    if (snake_heady == rows or snake_headx == columns):
        return "null"

    grid[int(snake_heady) + 1][int(snake_headx) + 1] = 9

    foodx = foodx / 10
    foody = foody / 10
    grid[int(foody) + 1][int(foodx) + 1] = 100

    for a in range(int(snake_len) - 1):
        x = int(snake_list_np[a * 2]) / 10
        y = int(snake_list_np[a * 2 + 1]) / 10
        grid[int(y) + 1][int(x) + 1] = 8
        print("X and Y coordinates: ", x, " ", y)

    print(grid)

    if (snake_headx < foodx):
        return "right"
    elif (snake_headx > foodx):
        return "left"
    elif (snake_heady > foody):
        return "up"
    elif (snake_heady < foody):
        return "down"
    else:
        return "null"