import random
import copy
import sys
#format used from Al Sweigert's fourinarow_text.py
BOARDWIDTH = int (input("Choose the number of columns"))
BOARDHEIGHT = int (input("Choose the number of rows"))
r = int (input("Choose the number of tiles to connect to win"))
play = input("choose who to play against")

def main():
    """
    b = getNewBoard()
    b[6][5] = 'X'
    b[5][4] = 'X'
    b[4][3] = 'X'
    b[3][2] = 'X'
    drawBoard(b)
    print(isWinner(b, 'X'))

    sys.exit()
    """

    print('R-In-A-Row')
    print()

    while True:
        if play == 'human vs human':
            human1Tile, human2Tile = enterHuman1Tile()

            turn = whoGoesFirst()
            print('The %s player will got first.' % (turn))
            mainBoard = getNewBoard()
        elif play == 'human vs computer':
            human1Tile, computer1Tile = enterHuman1Tile()
            turn = whoGoesFirst()
            print('The %s player will go first.' % (turn))
            mainBoard = getNewBoard()
        elif play == 'computer vs computer':
            computer1Tile, computer2Tile = enterHuman1Tile()
            turn = whoGoesFirst()
            print('The %s player will go first.' % (turn))


        while True:
            if play == 'human vs human':
                if turn == 'human1':
                    drawBoard(mainBoard)
                    move = getHuman1Move(mainBoard)

                    makeMove(mainBoard, human1Tile, move)

                    if isWinner(mainBoard, human1Tile):
                        winner = 'human1'

                        break
                    turn = 'human2'
                if turn == 'human2':
                    drawBoard(mainBoard)
                    move2 = getHuman2Move(mainBoard)
                    makeMove(mainBoard, human2Tile, move2)
                    if isWinner(mainBoard, human2Tile):
                        winner = 'human2'
                        break
                    turn = 'human1'

            elif play == 'human vs computer' :
                if turn == 'human':
                    drawBoard(mainBoard)
                    move = getHuman1Move(mainBoard)
                    makeMove(mainBoard, human1Tile, move)
                    if isWinner(mainBoard, human1Tile):
                        winner = 'human'

                        break
                    turn ='computer'

                elif turn == 'computer':
                   drawBoard(mainBoard)
                   print('The computer is thinking...')
                   move = getComputer1Move(mainBoard, computer1Tile)
                   makeMove(mainBoard, computer1Tile, move)
                   if isWinner(mainBoard, computer1Tile):
                     winner = 'computer'
                     break
                   turn = 'human'
            elif play == 'computer vs computer':
                if turn == 'computer1':
                   drawBoard(mainBoard)
                   print('computer1 is thinking...')
                   move = getComputer1Move(mainBoard, computer1Tile)
                   makeMove(mainBoard, computer1Tile, move)
                   if isWinner(mainBoard, computer1Tile):
                       winner = 'computer1'
                       break
                   turn = 'computer2'
                elif turn == 'computer2':
                   drawBoard(mainBoard)
                   print('computer2 is thinking...')
                   move = getComputer2Move(mainBoard, computer2Tile)
                   makeMove(mainBoard, computer2Tile, move)
                   if isWinner(mainBoard, computer2Tile):
                         winner = 'computer2'
                         break
                   turn = 'computer1'


            if isBoardFull(mainBoard):
                winner = 'tie'
                break

        drawBoard(mainBoard)
        print('Winner is: %s' % winner)
        if not playAgain():
            break


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def enterHuman1Tile():
    # Let's the human player type which tile they want to be.
    # Returns a list with the human player's tile as the first item, and the computer's tile as the second.
    tile = ''
    while not (tile == 'B' or tile == 'R'):
        print('Do you want to be B or R?')
        tile = input().upper()

    # the first element in the tuple is the human player's tile, the second is the computer's tile.
    if tile == 'B':
        return ['B', 'R']
    else:
        return ['R', 'B']

def enterHuman2Tile():
    # Let's the human player type which tile they want to be.
    # Returns a list with the human player's tile as the first item, and the computer's tile as the second.
    tile = ''
    while not (tile == 'B' or tile == 'R'):
        print('Do you want to be B or R?')
        tile = input().upper()

    # the first element in the tuple is the human player's tile, the second is the computer's tile.
    if tile == 'B':
        return ['B', 'R']
    else:
        return ['R', 'B']


def drawBoard(board):
    print()
    print(' ', end='')
    for x in range(1, BOARDWIDTH + 1):
        print(' %s  ' % x, end='')
    print()

    print('+---+' + ('---+' * (BOARDWIDTH - 1)))

    for y in range(BOARDHEIGHT):
        print('|   |' + ('   |' * (BOARDWIDTH - 1)))

        print('|', end='')
        for x in range(BOARDWIDTH):
            print(' %s |' % board[x][y], end='')
        print()

        print('|   |' + ('   |' * (BOARDWIDTH - 1)))

        print('+---+' + ('---+' * (BOARDWIDTH - 1)))


def getNewBoard():
    board = []
    for x in range(BOARDWIDTH):
        board.append([' '] * BOARDHEIGHT)
    return board


def getHuman1Move(board):
    while True:
        print('Which column do you want to move on? (1-%s, or "quit" to quit game)' % (BOARDWIDTH))
        move = input()
        if move.lower().startswith('q'):
            sys.exit()
        if not move.isdigit():
            continue
        move = int(move) - 1
        if isValidMove(board, move):
            return move
def getHuman2Move(board):
    while True:
        print('Which column do you want to move on? (1-%s, or "quit" to quit game)' % (BOARDWIDTH))
        move = input()
        if move.lower().startswith('q'):
            sys.exit()
        if not move.isdigit():
            continue
        move = int(move) - 1
        if isValidMove(board, move):
            return move

def getComputer1Move(board, computer1Tile):
    potentialMoves = getPotentialMoves(board, computer1Tile, 2)
    bestMoveScore = max([potentialMoves[i] for i in range(BOARDWIDTH) if isValidMove(board, i)])
    bestMoves = []
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveScore:
            bestMoves.append(i)
    return random.choice(bestMoves)

def getComputer2Move(board, computer2Tile):
    potentialMoves = getPotentialMoves(board, computer2Tile, 2)
    bestMoveScore = max([potentialMoves[i] for i in range(BOARDWIDTH) if isValidMove(board, i)])
    bestMoves = []
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveScore:
            bestMoves.append(i)
    return random.choice(bestMoves)

def getPotentialMoves(board, playerTile, lookAhead):
    if lookAhead == 0:
        return [0] * BOARDWIDTH

    potentialMoves = []

    if playerTile == 'B':
        enemyTile = 'R'
    else:
        enemyTile = 'B'

    # Returns (best move, average condition of this state)
    if isBoardFull(board):
        return [0] * BOARDWIDTH

    # Figure out the best move to make.
    potentialMoves = [0] * BOARDWIDTH
    for playerMove in range(BOARDWIDTH):
        dupeBoard = copy.deepcopy(board)
        if not isValidMove(dupeBoard, playerMove):
            continue
        makeMove(dupeBoard, playerTile, playerMove)
        if isWinner(dupeBoard, playerTile):
            potentialMoves[playerMove] = 1
            break
        else:
            # do other player's moves and determine best one
            if isBoardFull(dupeBoard):
                potentialMoves[playerMove] = 0
            else:
                for enemyMove in range(BOARDWIDTH):
                    dupeBoard2 = copy.deepcopy(dupeBoard)
                    if not isValidMove(dupeBoard2, enemyMove):
                        continue
                    makeMove(dupeBoard2, enemyTile, enemyMove)
                    if isWinner(dupeBoard2, enemyTile):
                        potentialMoves[playerMove] = -1
                        break
                    else:
                        results = getPotentialMoves(dupeBoard2, playerTile, lookAhead - 1)
                        potentialMoves[playerMove] += (sum(results) / BOARDWIDTH) / BOARDWIDTH
    return potentialMoves

def whoGoesFirst():
    # Randomly choose the player who goes first.
    if play == 'human vs computer':
        if random.randint(0, 1) == 0:
            return 'computer'
        else:
            return 'human'
    if play == 'human vs human':
        if random.randint(0, 1) == 0:
            return 'human1'
        else:
            return 'human2'
    if play == 'computer vs computer':
        if random.randint(0, 1) == 0:
            return 'computer1'
        else:
            return 'computer2'

def makeMove(board, player, column):
    for y in range(BOARDHEIGHT-1, -1, -1):
        if board[column][y] == ' ':
            board[column][y] = player
            return


def isValidMove(board, move):
    if move < 0 or move >= (BOARDWIDTH):
        return False

    if board[move][0] != ' ':
        return False

    return True


def isBoardFull(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == ' ':
                return False
    return True


def isWinner(board,tile):
    # check horizontal spaces

    winner = True
    for x in range(BOARDWIDTH - r+1):
         for y in range(BOARDHEIGHT):
            for i in range(r):
                 winner = winner and (board[x+i][y] == tile)
                 if winner:
                   return True


    winner = True
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - r+1):
            for i in range(r):
                 winner = winner and (board[x][y+i])
                 if winner:
                   return True

    winner = True
    # check / diagonal spaces
    for x in range(BOARDWIDTH - r+1):
        for y in range(r+1, BOARDHEIGHT):
            for i in range(r):
                    winner = winner and (board[x+i][y-i])
                    if winner:
                       return True

    winner = True
    # check \ diagonal spaces
    for x in range(BOARDWIDTH - r+1):
        for y in range(BOARDHEIGHT - r+1):
            for i in range(r):
                winner = winner and (board[x+i][y+i])
                if winner:
                    return True

    return False


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')




if __name__ == '__main__':
    main()
