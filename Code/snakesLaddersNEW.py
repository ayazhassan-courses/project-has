'''
This is the source code for the game of Snakes & Ladders.

Course: CS 102 - Data Structures & Algorithms (L2)
Instructor: Dr. Syeda Saleha Raza

Team Members:

Ahmad Feroz (06109)
Habib Shehzad (05888)
Synclair Samson (05901)

For information on the rules of the game and how the game is structured please refer to the Readme.md file.
'''


#----------Importing the important things to be used-------------#
import pygame
import random
from pygame import mixer
import math
import time

def game():
    #--------------Initializing Pygame and the screen---------------# 
    pygame.init()
    screen=pygame.display.set_mode((1000,667))
    pygame.display.set_caption("Snakes & Ladders - Space Eddition")
    background = pygame.image.load("board10.png")
    #----------Loading the images of the players-----------#
    player1 = pygame.image.load('ship1.png')
    player2 = pygame.image.load('ship2.png')
    player1 = pygame.image.load('ship3.png')
    player1 = pygame.image.load('ship4.png')
    player5 = pygame.image.load('ship5.png')
    player6 = pygame.image.load('ship6.png')


    def BatMusic():
        mixer.init()
        mixer.music.load("BatMus.wav")
        mixer.music.play()
        mixer.music.set_volume(0.7)
        
    def SupMusic():
        mixer.init()
        mixer.music.load("SupMus.wav")
        mixer.music.play()
        mixer.music.set_volume(0.7)

    #----------Loading all the possible dice roll images------------#
    one = pygame.image.load('dice1.png')
    two = pygame.image.load('dice2.png')
    three = pygame.image.load('dice3.png')
    four = pygame.image.load('dice4.png')
    five = pygame.image.load('dice5.png')
    six = pygame.image.load('dice6.png')

    snake_txt = [
    "A python bit you..",
    "Oops, you were bitten by a  deadly snake", "Dang it, another snake bite?",
    "oh no, Snake bite", "A deadly snake tried to devour you"
    "whoops", "darn",
    "snake bite", "oops", "tough luck"]

    #indicates a ladder climb!
    ladder_txt = [
    "This laddder will bring you closer to victory",
    "woww, reach for the stars",
    "nailed it, Go Go Go",
    "Congratulation, the ladder has jumped you forward ",
    "level up! (not really)", "you got it",
    "ladder aqquired", "yaayyy!!"]

    def is_empty(lst): return len(lst)==0
    def enQueue(lst,data): return lst.append(data)
    def front(lst): return lst[0]
    def deQueue(lst): return lst.pop(0)


    numbers=[] #--------This list stores numbers from 1 to 100.--------------#
    #------------Storing all numbers from 1 to 101 in a list------------------#
    for i in range(1,101): numbers.append(i)

    #--------Loading the snakes and ladder images-----------#
    snakeImg = pygame.image.load('portal.png')
    ladderImg = pygame.image.load('portal.png')

                #------------Go from Key to Value----------------#
    #----------Storing The loaction of snakes in a dictionary---------------------#
    #----------snake heads are keys and snake tails are values--------------------#
    snakes = {
    99: 78,
    95: 75,
    93: 73,
    87: 24,
    17: 7,
    62: 19,
    54: 34,
    64: 60
    }
    #----------Storing The loaction of Ladders in a dictionary---------------------#
    #----------Ladder tails are keys and Ladder heads are values--------------------#
    ladders = {
    63: 81,
    40: 59,
    20: 38,
    4: 14,
    9: 31,
    28: 84,
    71: 91,
    51: 67
    }

    #------This dictionary stores all the locations of the board-------#
    #------Key: Number-----Value: (x,y) co-ordinate--------------#
    location = {0:(0,600)}
    xx,yy,mm,nn = 0,10,19,9
    a,b = 60,600
    for i in range(10):
        if i%2==0:
            for j in range(xx,yy):
                location[numbers[j]] = (a,b) 
                a+=60
            xx,yy=xx+20,yy+20
        else:
            for j in range(mm,nn,-1):
                location[numbers[j]] = (a,b)
                a+=60
            mm,nn = mm+20,nn+20
        a,b=60,b-60

    def xy_location(number):
        return location[number]

    nums = {}
    for number in location: nums[location[number]] = number

    def num_location(x,y):
        return nums[(x,y)]

    # def wye(location): return location in wyes

    #-----------Keeping a track of those locations where player has to move in reverse-------------------#

    #----------Check if the player won or not----------#
    def win_check(location):
        if num_location(location[0],location[1]) == 100: return True
        else: return False


    #--------The initial Co-ordinates of the player----------#
    p1_X, p1_Y= 0, 600

    #--------The change in x and y co-ordinates is initally zero--------------#
    # p1_x_change = 0
    # p1_y_change = 0


    #--------The players are initially not moving--------------#
    moving = None
    #------------The previous and future values re initially zero as the dice has not been rolled------------------#

    #--------------The dice value is zero initially----------#


    #---------------The co-ordinates for the roll button to be displayed------------#
    roll_x = 868
    roll_y = 594.5

    #-------------The co-ordinates for the dice to be displayed==============#
    dice_x = 863
    dice_y = 144


    #-----------This funcation draws the roll button-------------------#
    charterPath = pygame.image.load('rollButton.png')
    def roll_button():
        # pygame.draw.rect(screen,(0,0,0),(roll_x,roll_y,100,100))
        # font = pygame.font.Font('freesansbold.ttf', 32)
        # text = font.render("ROLL", False,(255, 255, 255) )
        # textRect = text.get_rect()
        # textRect.center = (roll_x+50, roll_y+50) 
        # screen.blit(text, textRect) 
        screen.blit(charterPath, (roll_x, roll_y))

    def show_hand():
        screen.blit(handImg, (roll_x, roll_y-50))

    #------------This function decides which picture is to be loaded when a dice is rolled---------------#
    def which_dice(num): 
        if num==1: return one
        if num==2: return two
        if num==3: return three
        if num==4: return four
        if num==5: return five
        if num==6: return six


    #----------This function displays the dice----------------#
    #---------According to the dice rolled--------------------#
    def display_dice():
        dice1 = random.randint(1,6)
        img1 = which_dice(dice1)
        return img1, dice1

    #----------This function displays the player--------------#
    def p1(x,y): screen.blit(player1,(x,y))
    def p2(x,y): screen.blit(player2,(x,y))

    #----------------This function tells if the player is in a snake location---------#
    def snaked(location):
        if location in snakes: return snakes[location]
        else: return False            

    #---------------This function tells if the players is in a ladder location------#
    def laddered(location):
        if location in ladders: return ladders[location]    
        else: return False

    def show_snake_txt():
        x=500
        y=50
        msg = deQueue(snake_txt)
        enQueue(snake_txt,msg)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(msg, False,(255, 255, 255) )
        textRect = text.get_rect()
        textRect.center = (x, y) 
        screen.blit(text, textRect)

    def show_ladder_txt():
        x=500
        y=50
        msg = deQueue(ladder_txt)
        enQueue(ladder_txt,msg)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(msg, False,(255, 255, 255) )
        textRect = text.get_rect()
        textRect.center = (x, y) 
        screen.blit(text, textRect)

    #----------This function displays all the snake locations-----------------#
    def show_snakes():
        for snake in snakes:
            snake_x = xy_location(snake)[0]
            snake_y = xy_location(snake)[1]
            screen.blit(snakeImg,(snake_x+20,snake_y+20))

    #-------------This function displays all the ladder locations-------------#
    def show_ladders():
        for ladder in ladders:
            ladder_x = xy_location(ladder)[0]
            ladder_y = xy_location(ladder)[1]    
            screen.blit(ladderImg,(ladder_x+20,ladder_y+20))

    #------------This function grids a particular number in a particular x,y co-ordinate-------------#
    def board(x,y,number):
        pygame.draw.rect(screen,(255,255,255,0),(x,y,60,60),1,)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(str(number), False,(255, 255, 255) )
        textRect = text.get_rect()
        textRect.center = (x+30, y+30) 
        screen.blit(text, textRect)


    #--------------This function sends all the numbers in the above function------------#
    #--------------In such a way that we get classic snakes and ladder board------------#
    #--------------------Where every second line is reversed----------------------------#
    def getBoard():
        xx,yy,mm,nn = 0,10,19,9
        a,b = 60,600
        for i in range(10):
            if i%2==0:
                for j in range(xx,yy):
                    board(a,b,numbers[j])
                    a+=60
                xx,yy=xx+20,yy+20
            else:
                for j in range(mm,nn,-1):
                    board(a,b,numbers[j])
                    a+=60
                mm,nn = mm+20,nn+20
            a,b=60,b-60



    #-----Initially the dice is zero---------#
    dice = 0

    #-------The initial positions of the player--------#
    players = {"Batman": (0,600), "Superman":(0,600)}

    heroes = ["Batman","Superman"]

    img1 = pygame.image.load('portal10.png')
    #-----The game will be running unless the player presses the quit button----------#
    running=True
    while running: #------ Keep on running the game unless player presses quit--------#
        screen.fill((255,255,255)) #---------FIll the screen------------#
        screen.blit(background, (0, 0))
        for event in pygame.event.get():  #--------Looping over all the events in the game---------#
            if event.type==pygame.QUIT: #--------If the user quits the game------------#
                running=False #---------End the loop---------#
            if event.type == pygame.MOUSEBUTTONUP: #-----If user presses mouse button-----------#
                pos = pygame.mouse.get_pos() #---------Get the position of the mouse--------#
                if 675<=pos[0]<=775 and 500<=pos[1]<=600: #---If the player presses the roll button----------#
                    img1, dice=display_dice()
                    moving=True


        screen.blit(img1,(dice_x,dice_y))

        #--------If Players are moving------------#
        while moving:
            current_player = deQueue(heroes) #-------Whose turn is it?---------#
            if current_player=="Batman": 
                BatMusic() #-------Play Batman Music---------#
            elif current_player=="Superman":
                SupMusic() #----------Play Superman Music---------#
            enQueue(heroes,current_player)  
            xy_position = players[current_player] #------Cordinates of that player------# 
            XX = xy_position[0]
            YY = xy_position[1] 
            old=num_location(XX,YY) #------Previous Location------#
            new = dice+old    #-----------Updated Location-----#
            if win_check((XX,YY)) or new>100: #---------If a player won------#
                running=False
            elif new>0 and moving and not snaked(new)==False: #-----If the player lands on snake------#
                new = snaked(new)
                XX = xy_location(new)[0]  
                YY = xy_location(new)[1]
                players[current_player] = (XX,YY) #-----Update Location-------#
                moving=False
            elif new>0 and moving and not laddered(new)==False: #---------If the player lands on ladder-------#
                new = laddered(new)
                XX = xy_location(new)[0]
                YY = xy_location(new)[1]
                players[current_player] = (XX,YY) #-----Update Location-------#
                moving=False
            elif new>0 and moving:  #---------If neither snake nor ladder----------#
                XX = xy_location(new)[0]
                YY = xy_location(new)[1]
                players[current_player] = (XX,YY) #-----Update Location-------#
                moving=False


        bman_x = players["Batman"][0]  #----updated X-cordinate of Batman--------#
        bman_y = players["Batman"][1] #----updated Y-cordinate of Batman--------#
        sman_x = players["Superman"][0] #----updated X-cordinate of Superman--------#
        sman_y = players["Superman"][1] #----updated Y-cordinate of Superman--------#

        roll_button()  #------Display the roll button-------#
        getBoard()    #--------Display the Board---------#
        p1(bman_x,bman_y)  #-------Display the player------#
        p2(sman_x,sman_y)  #-------Display the player-----#
        show_ladders() #------Show all the ladders-------#
        show_snakes()  #--------Show all the snakes--------#
        pygame.display.update() #------Keep updating the display--------#


def start():  #------The Welcome Display-------#
    pygame.init()   #-------Initialize Window------#
    screen=pygame.display.set_mode((1000,667)) 
    pygame.display.set_caption("Snakes & Ladders - Space Eddition")
    intro=True
    background= pygame.image.load('screen-01.png')
    while intro:
        screen.fill((0,0,0))
        screen.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: intro = False
            elif event.type == pygame.KEYDOWN: #-----If user presses enter start game---------#
                if event.key == pygame.K_RETURN:
                    game()
                    intro=False
        pygame.display.update()


start() #-------This starts the game----------#