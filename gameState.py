class GameState():
    """
    This class contains information of the state of a Gomoku game.
    Normally it is 5 in a row. We extend the game to N in a row.

    Parameter:
         N:         N in a row.
         boardSize: the board will be boardSize x boardSize

    There are two players: player 0 and 1. Player 0 goes first.
    """

    def __init__(self, N, boardSize, prevState = None):
        self.N = N
        self.boardSize = boardSize
        if prevState == None:
            self.board = {}
            self.gameOver = False
            self.winner = -1
        else:
            self.board = dict(prevState.board)
            self.gameOver = prevState.gameOver
            self.winner = prevState.winner

    def gameEnded(self):
        """
        Return True if game has ended. False otherwise.
        """
        return self.gameOver

    def getWinner(self):
        """
        Returns the winner's number (0 or 1).
        If the game is a tie or hasn't ended, return -1
        """
        if self.gameOver:
            return self.winner
        return -1

    def moveIsValid(self, player, move):
        """
        Check if a move is valid.
        """
        if player != 0 and player != 1:
            return False
        # Out of bounds or that position already has a piece
        if not self.withinBounds(move) or move in self.board:
            return False
        return True

    def generateSuccessor(self, player, move):
        """
        Make a copy of the current state, and simulate the move, and return that copy.
        """
        state = GameState(self.N, self.boardSize, self)
        state.makeMove(player, move)
        return state

    def makeMove(self, player, move):
        """
        Player makes a move.
        """
        if not self.moveIsValid(player, move):
            return
        
        self.board[move] = player
        if self.checkWinCondition(player, move):
            self.gameOver = True
            self.winner = player

    def __str__(self):
        s = ''
        for y in range(self.boardSize):
            for x in range(self.boardSize):
                if (x, y) not in self.board:
                    s += ' + |'
                elif self.board[(x, y)] == 0:
                    s += ' x |'
                else:
                    s += ' o |'
            s += "\n" + (4 * self.boardSize * "-") +'\n'
        return s


    def withinBounds(self, move):
        return move[0] >= 0 and move[0] < self.boardSize and move[1] >= 0 and move[1] < self.boardSize

    def checkWinCondition(self, player, move):
        """
        Return True if the player makes a move and wins the game.
        """
        x, y = move

        # Horizontal
        num = 1
        for i in range(x + 1, self.boardSize):
            if not (i, y) in self.board or self.board[(i, y)] != player:
                break
            num += 1
        for i in range(x - 1, -1, -1):
            if not (i, y) in self.board or self.board[(i, y)] != player:
                break
            num += 1
        if num >= self.N:
            return True

        # Vertical
        num = 1
        for j in range(y + 1, self.boardSize):
            if (x, j) not in self.board or self.board[(x, j)] != player:
                break
            num += 1
        for j in range(y - 1, -1, -1):
            if (x, j) not in self.board or self.board[(x, j)] != player:
                break
            num += 1
        if num >= self.N:
            return True

        # Diagonal /
        num = 1
        for i in range(1, self.boardSize):
            piece = (x + i, y + i)
            if not self.withinBounds(piece) or piece not in self.board or self.board[piece] != player:
                break
            num += 1
        for i in range(1, self.boardSize):
            piece = (x - i, y - i)
            if not self.withinBounds(piece) or piece not in self.board or self.board[piece] != player:
                break
            num += 1
        if num >= self.N:
            return True

        # Diagonal \
        num = 1
        for i in range(1, self.boardSize):
            piece = (x + i, y - i)
            if not self.withinBounds(piece) or piece not in self.board or self.board[piece] != player:
                break
            num += 1
        for i in range(1, self.boardSize):
            piece = (x - i, y + i)
            if not self.withinBounds(piece) or piece not in self.board or self.board[piece] != player:
                break
            num += 1
        if num >= self.N:
            return True

        return False

