class GameState():
"""
This class contains information of the state of a Gomoku game.
Normally it is 5 in a row. We extend the game to N in a row.

Parameter:
     N:         N in a row.
     boardSize: the board will be boardSize x boardSize

There are two players: player 0 and 1. Player 0 goes first.
"""

    def __init__(self, N, boardSize):
        self.N = N
        self.boardSize = boardSize
        self.board = {}
        self.gameOver = False

    def gameEnded(self):
        """
        Return True if game has ended. False otherwise.
        """
        return 0

    def getWinner(self):
        """
        Returns the winner's number (0 or 1).
        If the game is a tie or hasn't ended, return -1
        """
        return -1

    def moveIsValid(self, player, move):
        """
        Check if a move is valid.
        """
        return True

    def makeMove(self, player, move):
        return
