import numpy as np
import random
from colorama import Fore, Back, Style #for colours of discs

class Game:
    mat = None # this represents the board matrix
    rows = 0 # this represents the number of rows of the board
    cols = 0 # this represents the number of columns of the board
    turn = 0 # this represents whose turn it is (1 for player 1, 2 for player 2)
    wins = 0 # this represents the number of consecutive discs in order to win

my_game = Game()

def check_victory(game):
    #use dictionary to detect if there are 2 opposing sets of consecutive discs winning in the same round
    victory = {'one_win':["1",False], 'two_win':["2",False]}
    
    #1st iteration: check if there is set of consecutive disc 1 winning
    #2nd iteration: check if there is set of consecutive disc 2 winning
    for value in victory.values():
        
        #check horizontal wins
        for i in range(game.rows):
            hor_check = ''.join([str(int(n)) for n in game.mat[i,:]])
            if value[0]*game.wins in hor_check: 
                value[1] = True
                break
        if value[1]: #if set of consecutive disc 1 already detected, move on to check disc 2
            continue
            
        #check vertical wins  
        for j in range(game.cols):
            ver_check = ''.join([str(int(n)) for n in game.mat[:,j]])
            if value[0]*game.wins in ver_check:
                value[1] = True
                break
        if value[1]: #if set of consecutive disc 1 already detected, move on to check disc 2
            continue
            
        #check diagonal wins
        for n in range(max((game.cols*2)-1,(game.rows*2)-1)):
            
            #check y = -x wins
            diag_list = game.mat.diagonal(n+1-max(game.cols,game.rows))
            diag_check = ''.join([str(int(n)) for n in diag_list])
            if value[0]*game.wins in diag_check:
                value[1] = True
                break

            #check y = x wins
            game_mat_flip = np.fliplr(game.mat)
            diag_flip_list = game_mat_flip.diagonal(n+1-max(game.cols,game.rows))
            diag_flip_check = ''.join([str(int(n)) for n in diag_flip_list])
            if value[0]*game.wins in diag_flip_check:
                value[1] = True
                break
    
    #2 sets of consecutive discs winning in the same round
    if victory['one_win'][1] and victory['two_win'][1]:
        if game.turn == 2: #before turn changed to 2, player 1 applied winning move
            return 1
        else: #before turn changed to 1, player 2 applied winning move
            return 2
    #only 1 set of consecutive discs detected
    else:
        if victory['one_win'][1]: #if set of disc 1 (player 1 wins)
            return 1
        elif victory['two_win'][1]: #if set of disc 2 (player 2 wins)
            return 2
        
    #if board is full, then there is no winner; draw
    if 0 not in game.mat: 
        return 3
    #no victory detected (did not fulfil any if statement conditions)
    return 0 


def apply_move(game,col,pop):
    #add discs
    if not pop:
        #looks for next empty space of column 
        for i in range(game.rows):
            if game.mat[i,col] == 0: 
                #player 1's turn: disc becomes 1
                if game.turn == 1:
                    game.mat[i,col] = 1 
                    game.turn = 2 #switch to player 2's turn after player 1's move applied 
                    break
                #player 2's turn: disc becomes 2
                else:
                    game.mat[i,col] = 2
                    game.turn = 1 #switch to player 1's turn after player 2's move applied
                    break
    #pop discs
    else:
        #shift 1 row down by reassignment and fill last row with zero
        game.mat[0:game.rows-1,col] = game.mat[1:game.rows,col] 
        game.mat[game.rows-1,col] = 0
        #switch to player 2's turn after player 1's move applied 
        if game.turn == 1:
            game.turn = 2
        #switch to player 1's turn after player 2's move applied
        else:
            game.turn = 1 
    return game

def check_move(game,col,pop): 
    #pop check
    if pop: 
        #check whether the column is empty first, cannot pop if there are no discs 
        if game.mat[0,col] == 0:
            return False 
        #check whether the disc belongs to player 1 
        elif game.turn == 1:
            if game.mat[0,col] != 1:
                return False
        #check whether the disc belongs to player 2
        elif game.turn == 2:
            if game.mat[0,col] != 2:
                return False

    #add check
    else:
        #check whether column is full
        if not 0 in list(game.mat[:,col]):
            return False
    #if col chosen is valid (did not fulfil any nested if statement condition)
    return True
    
def computer_move(game,level): 
    #easy (level 1) for computer 
    if level == 1:
        col = random.randint(0,game.cols-1)
        pop = random.choice([True, False])
        while not check_move(game,col,pop): #choose random col,pop until it is a valid move
            col = random.randint(0,game.cols-1)
            pop = random.choice([True, False])
        return (col,pop) #returns random col and pop
    
    #medium (level 2) for computer
    else:
        #create temporary game for computer to test out potential moves
        temp_game = Game()
        temp_game.mat = game.mat.copy() #copy game.mat for testing so that original is unchanged
        temp_game.rows = game.rows
        temp_game.cols = game.cols
        temp_game.wins = game.wins
        
        #initialise temp_game.turns so that computer can be either player 1 or 2
        if game.turn == 1: #if computer is player 1
            a = 1
            b = 2
        else: #if computer is player 2
            a = 2
            b = 1
            
        #pop column, if computer wins when that column is popped
        pop = True
        for j in range(game.cols): #try popping every column and see if computer wins
            temp_game.turn = a
            if check_move(temp_game,j,pop): #only pop computer's own disc
                if check_victory(apply_move(temp_game,j,pop)) == a:
                    return j,pop #returns the column and pop that computer will win
            temp_game.mat = game.mat.copy() #reinitialise temp_game.mat for next iteration when if loop not fulfilled
        
        #add to column, if computer wins by adding to that column
        pop = False
        for j in range(game.cols): #try adding to every column and see if computer wins
            temp_game.turn = a
            if check_move(temp_game,j,pop): #only add when column is not full
                if check_victory(apply_move(temp_game,j,pop)) == a:
                    return j,pop #returns the column and pop that computer will win
            temp_game.mat = game.mat.copy() #reinitialise temp_game.mat for next iteration when if loops not fulfilled
        
        #computer applies a move that does not allow human to win when human applies the next move
        random_order = list(range(game.cols*2))
        random.shuffle(random_order) #create random order to prevent computer from adding discs systematically onto ascending columns
        #computer tries adding/popping a disc in every column
        for j in random_order:
            temp_game.mat = game.mat.copy() #reinitialise temp_game.mat for next iteration
            col = j % game.cols #go through the columns 2 times
            pop = j >= game.cols #1st time adding, 2nd time popping
            temp_game.turn = a
            if check_move(temp_game,col,pop): #add only when column not full, pop only when row 0 is computer's own disc
                apply_move(temp_game,col,pop) #computer applies move
                #simulate human move after above computer move (tries every column by iteration)
                #check if human wins next if computer makes above particular move
                human_win_next = False 
                for n in range(game.cols*2):
                    temp_board = temp_game.mat.copy() #reinitialise temp_board for next human iteration
                    col = n % game.cols #same rationale as above computer move 
                    pop = n >= game.cols
                    temp_game.turn = b
                    if check_move(temp_game,col,pop):
                        if check_victory(apply_move(temp_game,col,pop)) == b:
                            human_win_next = True #if human wins
                            temp_game.mat = temp_board #reinitialise temp_game.mat for next computer iteration
                            break #stop trying current human simulation, continue to next computer iteration
                        temp_game.mat = temp_board #reinitialise temp_game.mat for next computer iteration
                if not human_win_next:
                    return (j % game.cols,j >= game.cols) #return col,pop if after computer applies move, human applies move and human does not win
        temp_game.mat = game.mat.copy()
        
        #if above codes did not return, means already lost
        #1: if human has more than 1 way to win in the same round, block 1 of them
        pop = False
        for j in range(game.cols):
            temp_game.turn = b
            if check_move(temp_game,j,pop): #only add when column is not full
                if check_victory(apply_move(temp_game,j,pop)) == b:
                    return j,pop
            temp_game.mat = game.mat.copy() #reinitialise temp_game.mat for next iteration when if loops not fulfilled
        #2: else, human wins by popping next time, unable to stop him from popping, add random col
        for j in range(game.cols):
            temp_game.turn = a
            if check_move(temp_game,j,pop): #add only when column not full
                return j,pop
            
def display_board(game):
    for i in range(game.rows-1,-1,-1):
        for j in range(game.cols):
            #cyan disc for player 1
            if int(game.mat[i,j]) == 1:  
                print(Back.CYAN + Fore.WHITE + Style.BRIGHT + str(int(game.mat[i,j])) + Style.RESET_ALL, end = " ")
            #red disc for player 2 
            elif int(game.mat[i,j]) == 2: 
                print(Back.RED + Fore.WHITE + Style.BRIGHT + str(int(game.mat[i,j])) + Style.RESET_ALL, end = " ")
            #empty space 
            else:
                print(int(game.mat[i,j]), end = " ") 
        print()
        
def integer_check(var,low,high):
    max_try = 50
    for tries in range(max_try):
        #only allowed to try 49 times before game terminates upon reaching 50th iteration
        if tries == max_try-1: 
            print(Back.BLACK + Fore.WHITE + Style.BRIGHT + "You have exceeded the number of tries. Goodbye!" + Style.RESET_ALL)
            return "exit"
        #check that input is an integer
        elif var.isdigit(): 
            #if input is an integer and within range, break loop
            if low<=int(var)<=high: 
                break            
            #if input not within range, prompt user to enter again
            else:
                var = input("Not within range. Please enter within {} and {} inclusive: ".format(low,high))        
        #if input not integer, prompt user to enter again
        else:
            var = input("Not an integer. Please enter integer: ")
    #return valid input by user
    return var

def alphabet_check(var,letter1,letter2):
    max_try = 50 
    for tries in range(max_try):
        #only allowed to try 49 times before game terminates upon reaching 50th iteration
        if tries == max_try-1: 
            print(Back.BLACK + Fore.WHITE + Style.BRIGHT + "You have exceeded the number of tries. Goodbye!" + Style.RESET_ALL)
            return "exit"
        #if input not letter1 or letter2, prompt user to enter again
        elif var.lower() != letter1 and var.lower() != letter2:
            var = input("Please enter {} or {}: ".format(letter1,letter2)) 
        #if input valid, break loop
        else:
            break
    #return valid input by user
    return var.lower()
    
def menu():
    #explain game rules
    print(Back.BLACK + Fore.WHITE + Style.BRIGHT + "Welcome to Connect4 (Pop-out version)!" + Style.RESET_ALL)
    print("Take turns adding coloured discs from the top into a board.")
    print("They fall straight down and occupy the next empty space of the column.")
    print("In this Pop-out version, you can choose to pop out your own disc on the bottom row instead of adding discs.")
    print("It will drop every disc above it down by 1 space.")
    print()
    print("Objective: Connect 4 consecutive discs of your own vertically, horizontally or diagonally before your opponent does to win.")
    print("If the board is full before anyone wins, it is a draw.")
    print()

    start_game = 'y' 
    while start_game == 'y': #while game is ongoing
        #set default settings
        my_game.rows = 6
        my_game.cols = 7
        my_game.wins = 4
        #choosing whether to change default game settings
        print(Back.BLACK + Fore.WHITE + Style.BRIGHT + "Default game settings: 6X7 board. Connect 4 discs to win." + Style.RESET_ALL)
        change_default = input("Do you wish to change the default game settings? (Enter y or n): ")
        change_default = alphabet_check(change_default,'y','n') #check that input is y/n
        if change_default == "exit": #exit game if user gives invalid input too many times
            return
        
        #choosing number of rows, columns and discs to win if changing default settings
        if change_default == 'y':
            my_game.rows = input("Enter size of row (4 to 30): ")
            my_game.rows = integer_check(my_game.rows,4,30) #check that input is integer within 4 to 30 inclusive
            if my_game.rows == "exit": #exit game if user gives invalid input too many times
                return
            my_game.rows = int(my_game.rows)
            
            my_game.cols = input("Enter size of column (4 to 30): ")
            my_game.cols = integer_check(my_game.cols,4,30) #check that input is integer within 4 to 30 inclusive
            if my_game.cols == "exit": #exit game if user gives invalid input too many times
                return
            my_game.cols = int(my_game.cols)
            
            my_game.wins = input("Enter number of consecutive discs to win (4 to {}): ".format(max(my_game.cols,my_game.rows)))
            my_game.wins = integer_check(my_game.wins,4,max(my_game.cols,my_game.rows)) #check that input is integer within 4 to number of game columns inclusive
            if my_game.wins == "exit": #exit game if user gives invalid input too many times
                return
            my_game.wins = int(my_game.wins)
        
        #create board
        my_game.mat = np.zeros((my_game.rows, my_game.cols)) 
        
        #choosing Human-Human play or Computer-Human mode
        choose_mode = input("Do you wish to play with another Human or with a Computer (Enter h or c): ")
        choose_mode = alphabet_check(choose_mode,'h','c') #check that input is h or c
        if choose_mode == "exit": #exit game if user gives invalid input too many times
            return
        #choosing Computer-level for Computer-Human mode
        if choose_mode == 'c':
            choose_level_str = input("Do you wish to play with a Easy-level Computer (Level 1) or Medium-level Computer (Level 2) (Enter 1 or 2): ")
            choose_level = integer_check(choose_level_str,1,2) #check that input is integer 1 or 2
            if choose_level == "exit": #exit game if user gives invalid input too many times
                return
            choose_level = int(choose_level)
        print()
        
        #The first player is chosen at random
        my_game.turn = random.randint(1,2)
        if choose_mode == 'h':
            print("The first player is chosen at random. Player", my_game.turn, "will start first.")
        else:
            if my_game.turn == 1: #Computer is Player 1, Human is Player 2
                print("The first player is chosen at random. Computer will start first.")
            else:
                print("The first player is chosen at random. Human will start first.")
        print()
        print("This is your chosen board.")
        print()
        display_board(my_game)
    
        while check_victory(my_game) == 0:  #while victory checked and nobody wins
            print()
            
            #if Computer-Human mode when my_game.turn == 1
            #Computer plays
            if choose_mode == 'c' and my_game.turn == 1:
                print("Level", choose_level, "Computer's turn. (Player 1)")
                print()
                
                #computer makes move according to level
                col,pop = computer_move(my_game,choose_level)
                display_board(apply_move(my_game,col,pop))
                print("Level", choose_level, "Computer has played.")
            else:
                
            #if Human-Human mode or Computer-Human mode when my_game.turn == 2,
            #Human plays
                if choose_mode == 'c' and my_game.turn == 2:
                    print("Human's turn. (Player 2)")
                else:
                    print("Player", my_game.turn, "'s turn.")
                
                #choosing to add or pop a disc
                pop_str = input("Do you want to add or pop disc? (Enter a or p): ")
                pop_str = alphabet_check(pop_str,'a','p') #check that input is a/p
                if pop_str == "exit": #exit game if user gives invalid input too many times
                    return
                elif pop_str == "p":
                    pop = True #user wants to pop
                else:
                    pop = False #user wants to add
                
                #choosing column to apply add/pop
                col_str = input("Choose column (1 to {}): ".format(my_game.cols))
                col_str = integer_check(col_str,1,my_game.cols) #check that input is an integer
                if col_str == "exit": #exit game if user gives invalid input too many times
                    return
                col_str = int(col_str)
                print()
                
                #prompt user to enter column until it is a valid move
                while not check_move(my_game,int(col_str)-1,pop): 
                    print("Invalid move. Please try again.")
                    pop_str = input("Do you want to add or pop disc? (Enter a or p): ")
                    pop_str = alphabet_check(pop_str,'a','p') #check that input is a/p
                    if pop_str == "exit": #exit game if user gives invalid input too many times
                        return
                    elif pop_str == "p":
                        pop = True #user wants to pop
                    else:
                        pop = False #user wants to add
                    col_str = input("Choose column (1 to {}): ".format(my_game.cols))
                    col_str = integer_check(col_str,1,my_game.cols) #check that input is an integer
                    if col_str == "exit": #exit game if user gives invalid input too many times
                        return

                #apply move
                col = int(col_str) - 1 #convert into column index
                display_board(apply_move(my_game,col,pop))
        print()
        
        #victory checked player 1/computer wins
        if check_victory(my_game) == 1:
            if choose_mode == 'h': 
                print(Back.CYAN + Fore.WHITE + Style.BRIGHT + "Player 1 wins!" + Style.RESET_ALL)
            else:
                print(Back.CYAN + Fore.WHITE + Style.BRIGHT + "Computer wins!" + Style.RESET_ALL)
        #victory checked player 2/human wins
        elif check_victory(my_game) == 2: 
            if choose_mode == 'h': 
                print(Back.RED + Fore.WHITE + Style.BRIGHT + "Player 2 wins!" + Style.RESET_ALL)
            else:
                print(Back.RED + Fore.WHITE + Style.BRIGHT + "Human wins!" + Style.RESET_ALL)
        #victory checked, board is full; game is a draw
        else:
            print(Back.BLACK + Fore.WHITE + Style.BRIGHT + "This game is a draw!" + Style.RESET_ALL) 
            
        #check if user wants to continue playing after current game ends
        start_game = input("Do you want to play again?(y or n): ")
        start_game = alphabet_check(start_game,'y','n') #check that input is y/n
        if start_game == "exit": #exit game if user gives invalid input too many times
            return
        print()

    #terminate program if user does not want to continue playing
    print(Back.BLACK + Fore.WHITE + Style.BRIGHT + "You have exited the game. Goodbye!" + Style.RESET_ALL)
    return

#game play
menu()


