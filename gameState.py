import util

class GameState():
    """
    This class contains information of the state of a Gomoku game.
    Normally it is 5 in a row. We extend the game to N in a row.

    Parameter:
         N:         N in a row.
         boardSize: the board will be boardSize x boardSize
         numPlayers: How many total players in this game (including computers)

    There are N players.

    Features: (agentIndex, description) => number
    Ex. (agentIndex, 'open 3') => 2
    """

    def __init__(self, N, boardSize, numPlayers, prevState = None):
        self.N = N
        self.boardSize = boardSize
        self.numPlayers = numPlayers
        if prevState == None:
            self.board = {}
            self.gameOver = False
            self.winner = -1
            self.features = {} # Ex. (agentIndex, 'open 3') -> 2
        else:
            self.board = dict(prevState.board)
            self.gameOver = prevState.gameOver
            self.winner = prevState.winner
            self.features = dict(prevState.features)

    def getLegalActions(self):
        legalActions = []
        for y in range(self.boardSize):
            for x in range(self.boardSize):
                if (x, y) not in self.board:
                    legalActions.append((x,y))
        return legalActions

    def gameEnded(self):
        """
        Return True if game has ended. False otherwise.
        """
        return self.gameOver

    def getWinner(self):
        """
        Returns the winner's number.
        If the game is a tie or hasn't ended, return -1
        """
        if self.gameOver:
            return self.winner
        return -1

    def moveIsValid(self, playerIndex, move):
        """
        Check if a move is valid.
        """

        if playerIndex < 0 or playerIndex >= self.numPlayers:
            return False
        # Out of bounds or that position already has a piece
        if not self.withinBounds(move) or move in self.board:
            return False
        return True

    def generateSuccessor(self, player, move):
        """
        Make a copy of the current state, and simulate the move, and return that copy.
        """
        state = GameState(self.N, self.boardSize, self.numPlayers, self)
        state.makeMove(player, move)
        return state

    def makeMove(self, player, move):
        """
        Player makes a move.
        """
        if not self.moveIsValid(player, move):
            return
        
        self.board[move] = player
        self.updateFeaturesForMove(player, move)
        if self.checkTie():
            self.gameOver = True

    def __str__(self):
        s = ''
        for y in range(self.boardSize):
            for x in range(self.boardSize):
                if (x, y) not in self.board:
                    s += '   |'
                else:
                    s += ' ' + str(self.board[(x,y)]) + ' |'
            s += "\n" + (4 * self.boardSize * "-") +'\n'
        return s


    def withinBounds(self, move):
        return move[0] >= 0 and move[0] < self.boardSize and move[1] >= 0 and move[1] < self.boardSize

    def checkTie(self):
        if len(self.board.keys()) == self.boardSize**2 :
            return True
        else:
            return False


    def updateFeaturesForMove(self, player, move):
        """
        Update the features when a player makes a move.
        There are 4 directions (Horizontal, Vertical, Diagonal /, Diagonal \).
        """
        x, y = move

        ############ Horizontal ############
        neighbors1 = self.checkNeighboringRows(move, [(i, y) for i in range(x + 1, self.boardSize + 1)])
        neighbors2 = self.checkNeighboringRows(move, [(i, y) for i in range(x - 1, -2, -1)])
        self.updateFeature(player, move, neighbors1, neighbors2)

        ############ Vertical ############
        neighbors1 = self.checkNeighboringRows(move, [(x, j) for j in range(y + 1, self.boardSize + 1)])
        neighbors2 = self.checkNeighboringRows(move, [(x, j) for j in range(y - 1, -2, -1)])
        self.updateFeature(player, move, neighbors1, neighbors2)

        ############ Diagonal / ############
        neighbors1 = self.checkNeighboringRows(move, [(x + i, y + i) for i in range(1, self.boardSize + 1)])
        neighbors2 = self.checkNeighboringRows(move, [(x - i, y - i) for i in range(1, self.boardSize + 1)])
        self.updateFeature(player, move, neighbors1, neighbors2)

        ############ Diagonal \ ############
        neighbors1 = self.checkNeighboringRows(move, [(x + i, y - i) for i in range(1, self.boardSize + 1)])
        neighbors2 = self.checkNeighboringRows(move, [(x - i, y + i) for i in range(1, self.boardSize + 1)])
        self.updateFeature(player, move, neighbors1, neighbors2)

    def checkNeighboringRows(self, move, piecesRange):
        """
        Return (player, num in a row, blocked or not)
        This logic is complicated...
        """
        # Hit boundary (no neighbors)
        if len(piecesRange) == 0 or not self.withinBounds(piecesRange[0]):
            return (-1, 0, 1)
        # Open end (no neighbors)
        if piecesRange[0] not in self.board:
            return (-1, 0, 0)

        player = self.board[piecesRange[0]]
        num = 0
        blocked = 0
        for piece in piecesRange:
            if not self.withinBounds(piece) or (piece in self.board and self.board[piece] != player):
                blocked = 1
                break
            if piece not in self.board:
                break
            num += 1
        return (player, num, blocked)

    def updateFeature(self, player, move, neighbors1, neighbors2):
        """
        Delete/Update the features of the neighbors.
        For example, if neighbor is an open 3 from a different player,
        then update it to be a blocked 3.

        Then, add a new feature according to the given move and its neighbors.
        Parameters: neighbors: (playerIndex, num, blocked)
        """
        if neighbors1[1] == 0 and neighbors2[1] == 0:
            return

        # Delete/Update the features of the neighbors
        for neighbor in [neighbors1, neighbors2]:
            num = neighbor[1]
            if neighbor[0] == -1:
                # no neighbor
                continue
            if neighbor[0] != player:
                # neighbor is a different player, so delete or update the feature
                if num >= 2:
                    if neighbor[2] == 0: # not blocked
                        featureToDelete = (neighbor[0], 'open ' + str(num))
                        util.deleteItemFromDict(self.features, featureToDelete)
                        featureToAdd = (neighbor[0], 'blocked ' + str(num))
                        util.addItemToDict(self.features, featureToAdd)
                    else: # blocked
                        featureToDelete = (neighbor[0], 'blocked ' + str(num))
                        util.deleteItemFromDict(self.features, featureToDelete)
            else:
                # neighbor is the same player, so delete the feature
                if num >= 2:
                    if neighbor[2] == 0: # not blocked
                        featureToDelete = (neighbor[0], 'open ' + str(num))
                        util.deleteItemFromDict(self.features, featureToDelete)
                    else: # blocked
                        featureToDelete = (neighbor[0], 'blocked ' + str(num))
                        util.deleteItemFromDict(self.features, featureToDelete)

        # Add a new feature according to the given move and its neighbors.
        num = 1
        blocked = 0
        for neighbor in [neighbors1, neighbors2]:
            if neighbor[0] == -1:
                blocked += neighbor[2]
            elif neighbor[0] == player:
                num += neighbor[1]
                blocked += neighbor[2]
            else:
                blocked += 1

        # Game ends if num >= self.N
        if num >= self.N:
            self.gameOver = True
            self.winner = player

        s = ''
        if blocked >= 2 or num <= 1:
            return
        if blocked == 0:
            s = 'open ' + str(num)
        elif blocked == 1:
            s = 'blocked ' + str(num)

        feature = (player, s)
        util.addItemToDict(self.features, feature)
    
