""" EPR1 - Übungsblatt 4 - "Vier gewinnt" 

Implementation of "Connect Four" for two players human players
or one human player agains the computer.
    
    The following are winning patterns:
    +------------------------------------------+
    | 1.   X X   2. X X      3.  X      4.   X |
    |  X X          X X        X X       X X   |
    |                            X       X     |
    +------------------------------------------+

The game is finished as soon as one player reaches one of the patterns above.
"""

from os import system, name
from random import randint


# ____________________________________________________________________________
clear = lambda: system('cls' if name == 'nt' else 'clear')

# ____________________________________________________________________________
# Graphical output:

def show_board(board, row, col):
    """ 
    Graphical output of the board.
    """
    print("\n" + 3 * " ", " ".join([str(x) for x in range(0,col)]), end="")
    print("\n" + 3 * " " + col * " v", end="")
    for j in range(0, row):
        print("\n" + str(j) + " |", end=" ")
        for i in range(0, col): 
            print(board[j][i], end=" ")
        print("|", end=" ")
    print("\n" + 3 * " " + col * " -", end="")
    print("\n")

def show_winning_patterns():
    """
    Displays the possible winning patterns to the players.
    """
    print("\nThese are the winning patterns:")
    print("+------------------------------------------+")
    print("| 1.   X X   2. X X      3.  X      4.   X |")
    print("|    X X          X X        X X       X X |")
    print("|                              X       X   |")
    print("+------------------------------------------+") 

def show_header(symbols):
    print("=== Welcome to Connect Four ===")
    show_winning_patterns()
    print("Player 1:", symbols[0], end="   ")
    print("Player 2:", symbols[1])

# ____________________________________________________________________________
# Setup game subroutines:

def setup_board(row, col):
    """ 
    Implements the board for a given number of rows and columns.
    """
    board = [["." for x in range(0, col)] for y in range(0, row)]
    return board

def insert(board, col_num, symbol, row):
    """ 
    Asks the user for a column number and puts his symbol in
    the highest row available.
    """
    for i in range(row-1, -1, -1):
        if board[i][col_num] != ".":
            pass
        else: 
            board[i][col_num] = symbol
            break
    return board

def remove(board, col_num, row):
    """ 
    Removes the symbol from the column col_num.
    """
    for i in range(row):
        if board[i][col_num] == ".":
            pass
        else: 
            board[i][col_num] = "."
            break
    return board

# ____________________________________________________________________________
# Check patterns and winner:

def check_pattern_1(board, symbol, row, col):
    """ 
    Checks the board for the following pattern:
    1.   X X
       X X
    """
    winner = False
    for i in range(0, row-1):
        for j in range (1, col-1):
            if board[i][j] == symbol and \
               board[i][j+1] == symbol and \
               board[i+1][j] == symbol and \
               board[i+1][j-1] == symbol:
                winner = True
    return winner

def check_pattern_2(board, symbol, row, col):
    """ 
    Checks the board for the following pattern:
    2. X X
         X X
    """
    winner = False
    for i in range(0, row-1):
        for j in range (1, col-2):
            if board[i][j] == symbol and \
               board[i][j+1] == symbol and \
               board[i+1][j+1] == symbol and \
               board[i+1][j+2] == symbol:
                winner = True
    return winner

def check_pattern_3(board, symbol, row, col):
    """ 
    Checks the board for the following pattern:
    3.  X
        X X
          X
    """
    winner = False
    for i in range(0, row-2):
        for j in range (0, col-1):
            if board[i][j] == symbol and \
               board[i+1][j] == symbol and \
               board[i+1][j+1] == symbol and \
               board[i+2][j+1] == symbol:
                winner = True
    return winner

def check_pattern_4(board, symbol, row, col):
    """ 
    Checks the board for the following pattern:
    4.    X
        X X
        X  
    """
    winner = False
    for i in range(0, row-2):
        for j in range (1, col):
            if board[i][j] == symbol and \
               board[i+1][j] == symbol and \
               board[i+1][j-1] == symbol and \
               board[i+2][j-1] == symbol:
                winner = True
    return winner

def check_winner(board, symbol, row, col):
    """ 
    Checks if a winning pattern is on the grid.
    If so, changes the winner-variable to True.
    """
    winner = False
    if check_pattern_1(board, symbol, row, col) or \
       check_pattern_2(board, symbol, row, col) or \
       check_pattern_3(board, symbol, row, col) or \
       check_pattern_4(board, symbol, row, col):
        winner = True
    return winner

# ____________________________________________________________________________
# Player modes:

def ai_player(board, symbols, valid_columns, row, col):
    # AI is always Player 2
    move_made = False
    for c in valid_columns:
        # AI to check if it can win in this round.
        if not move_made:
            c = int(c)
            board = insert(board, c, symbols[1], row)
            #show_board(board, row, col)
            winner = check_winner(board, symbols[1], row, col)
            if winner:
                move_made = True
                #input("Want to win move")
                break
            else:
                board = remove(board, c, row)
        # AI checks if opponent can win in next round
        if not move_made:
            c = int(c)
            board = insert(board, c, symbols[0], row)
            winner = check_winner(board, symbols[0], row, col)
            #show_board(board, row, col)
            board = remove(board, c, row)
            if winner:
                board = insert(board, c, symbols[1], row)
                move_made = True
                #input("Opponent won't win move")
                winner = False
                break     
    # If AI can neither win, nor can the opponent, AI puts in the symbol
    # in a random column.
    if not move_made:
        n = len(valid_columns)
        m = randint(0, n-1)
        k = int(valid_columns[m])
        board = insert(board, k, symbols[1], row)       
        #show_board(board, row, col)
        move_made = True
        #input("Random Move")
        #show_board(board, row, col)
        #print(winner)
    return board

def one_player_mode(board, symbols, row, col):
    """
    Play mode for one human player against the AI.
    """
    winner = False
    while not winner:
        for i in [0,1]:
            if i == 0:
                clear()
                show_header(symbols)
                show_board(board, row, col)
                print("Player", i+1, "it's your turn.")
                
                valid_columns = [str(i) for i in range(0, col)\
                                if (board[0][i] == ".")]
                other_input = ["q", "r"]
                valid_input = valid_columns + other_input
                print("\nThese are your options:")
                if len(valid_columns) == 0:
                    print("Game Over. Press q to quit or r to restart.")
                else:
                    for x in valid_input:
                        print(x, end=" ")
                    col_num = input("\nChoose a column number to play," +
                                    " q to quit or r to restart the game:" +
                                    "\n--> ")
                    while col_num not in valid_input:
                        col_num = input("\nInvalid input. Try again:\n" +
                                        "Choose a column number to play, " +
                                        "q to quit or r to restart the game:"+
                                        "\n--> ")               
                if col_num == "q":
                    input("You quit the game. THank you! Come again!")
                    winner = True
                    clear()
                    break
                elif col_num == "r":
                    main()
                else:
                    col_num = int(col_num)
                    symbol = symbols[i]
                    board = insert(board, col_num, symbol, row)
                    
                    clear()
                    show_header(symbols)
                    show_board(board, row, col)
                    winner = check_winner(board, symbol, row, col)
                    if winner:
                        print("\nPlayer", i+1, "has won the game!")
                        break
            else:
                valid_columns = [str(i) for i in range(0, col)\
                                 if (board[0][i] == ".")]
                if len(valid_columns) == 0:
                    print("Game Over. Press q to quit or r to restart.")
                    winner = True
                    break                   
                else:
                    input("Press enter to see the Computer's move!")
                    clear()
                    show_header(symbols)
                    board = ai_player(board, symbols, valid_columns, row, col)
                    winner = check_winner(board, symbols[1], row, col)
                    if winner:

                        show_header(symbols)

                        show_board(board, row, col)

                        print("\nThe computer has won the game!")

                        break

def two_player_mode(board, symbols, row, col):
    """
    Play mode for two human players.
    """
    winner = False
    while not winner:
        for i in [0,1]:
            clear()
            show_header(symbols)
            show_board(board, row, col)
            
            valid_columns = [str(i) for i in range(0, col)\
                            if (board[0][i] == ".")]
            other_input = ["q", "r"]
            valid_input = valid_columns + other_input
            if len(valid_columns) == 0:
                    print("Game Over. No winner.")
                    winner = True
                    break
            else:
                print("Player", i+1, "it's your turn.")
                print("\nThese are your options:")
                for x in valid_input:
                    print(x, end=" ")
                col_num = input("\nChoose a column number to place a coin,"+
                                " q to quit or r to restart the game:" +
                                "\n--> ")
                while col_num not in valid_input:
                    col_num = input("\nInvalid input. Try again:\n" +
                                    "Choose a column number to place a coin,"+
                                    " q to quit or r to restart the game:"+
                                    "\n--> ")
            if col_num == "q":
                input("You quit the game. Thank you! Come again!")
                winner = True
                clear()
                break
            elif col_num == "r":
                main()
            else:
                col_num = int(col_num)
                symbol = symbols[i]
                board = insert(board, col_num, symbol, row)               
                clear()
                show_header(symbols)
                show_board(board, row, col)
                winner = check_winner(board, symbol, row, col)
                if winner:
                    print("\nPlayer", i+1, "has won the game!")
                    break
        
# ____________________________________________________________________________
# Main program:

def main():
    """ Implementation of "Connect Four" for two players human players
    or one human player agains the computer.
    
    The following are winning patterns:
    +------------------------------------------+
    | 1.   X X   2. X X      3.  X      4.   X |
    |  X X          X X        X X       X X   |
    |                            X       X     |
    +------------------------------------------+

    The game is finished as soon as one player reaches one of the above.
    """
    # Pre-defined number of rows and columns for settin up the board
    row = 9
    col = 10
    symbols = ["X", "O"]
    board = setup_board(row, col)

    # To determine the mode (one or two player)
    clear()
    print("=== Welcome to Connect Four ===")
    player_mode = input("\nDo you want to play with 1 or 2 players?\n"
                      + "Enter 1 for one player) or 2 (for two players)"
                      + "\n--> ")

    valid_mode = ["1", "2"]

    while player_mode not in valid_mode:
        player_mode = input("Do you want to play with 1 or 2 players? "
                       + "\n--> ")

    # Runs the game in the selected mode
    if player_mode == "1":
        input("\nYou've chosen to fight against the AI. Good luck!" 
              + "\n--> Press enter to start!")
        one_player_mode(board, symbols, row, col)
    else:
        input("\nYou've chosen to play with two players! Have fun!"
              + "\n--> Press enter to start!")
        two_player_mode(board, symbols, row, col)

    # End statement before the console window is closed
    game_end = input("\nPress Enter to close the window or \"r\" to restart!")
    if game_end == "r":
        main()


if __name__ == "__main__":
     main()



# #_____________________________________________________________________________
# # AI Testfälle: siehe pdf Document.
# # 1. Beendet die AI das Spiel, wenn möglich:
# row = 4
# col = 5
# symbols = ["⬢", "⬡"]
# board = setup_board(row, col)
# valid_columns = [str(i) for i in range(0, col)\
#                             if (board[0][i] == ".")]
# board[3][1] = "⬡"
# board[3][2] = "⬡"
# board[2][3] = "⬡"
# board[3][3] = "⬢"
# show_board(board, row, col)
# board = ai_player(board, symbols, valid_columns, row, col)
# show_board(board, row, col)

# # 3. Verhindert die AI das Gewinnen des Gegners?:
# row = 4
# col = 5
# symbols = ["⬢", "⬡"]
# board = setup_board(row, col)
# valid_columns = [str(i) for i in range(0, col)\
#                             if (board[0][i] == ".")]
# board[3][1] = "⬢"
# board[3][2] = "⬢"
# board[2][3] = "⬢"
# board[3][3] = "⬡"
# show_board(board, row, col)
# board = ai_player(board, symbols, valid_columns, row, col)
# show_board(board, row, col)

# # 3. Randomisierter Spielzug, wenn weder AI noch Gegner im nächsten Zug
# # gewinnen kann:
# row = 4
# col = 5
# symbols = ["⬢", "⬡"]
# board = setup_board(row, col)
# valid_columns = [str(i) for i in range(0, col)\
#                             if (board[0][i] == ".")]
# board[3][1] = "⬢"
# board[3][2] = "⬡"
# board[2][3] = "⬢"
# board[3][3] = "⬡"
# show_board(board, row, col)
# board = ai_player(board, symbols, valid_columns, row, col)
# show_board(board, row, col)

# # 4. AI wirf in jedem Zug nur einen Stein ein.:
# # Kurz beschreiben