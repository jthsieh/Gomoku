import util
import copy

class GameState():
    """
    This class contains information of the state of a Gomoku game.
    Normally it is 5 in a row. We extend the game to N in a row.

    Parameter:
        N:          N in a row
        boardSize:  The board will be boardSize x boardSize
        numPlayers: How many total players in this game (including computers)

    Instance variables:
        N:             N in a row
        boardSize:     The board will be boardSize x boardSize
        numPlayers:    How many total players in this game (including computers)
        board:         A dictionary of (position => player index)
        gameOver:      Whether the game is over or not
        winner:        The index of the winner, -1 if the game is not over
        features:      A dictionary of ((agentIndex, description) => number)
                       Ex. (agentIndex, 'open 3') => 2
                           (agentIndex, 'blocked 4') => 1
    """

    def __init__(self, N, boardSize, numPlayers, prevState = None):
        self.N = N
        self.boardSize = boardSize
        self.numPlayers = numPlayers

        if prevState == None:
            self.board = {}
            self.legalActions = set()
            self.currentPlayer = 0
            self.gameOver = False
            self.winner = -1
            self.features = {}
            self.positionToFeatures = dict()
            self.previousAction = None #(player, action)
        else:
            self.board = dict(prevState.board)
            self.legalActions = set(prevState.legalActions)
            self.currentPlayer = prevState.currentPlayer
            self.gameOver = prevState.gameOver
            self.winner = prevState.winner
            self.features = dict(prevState.features)
            self.positionToFeatures = copy.deepcopy(prevState.positionToFeatures)
            self.previousAction = prevState.previousAction

    def getLegalActions(self):
        """
        If there are no pieces on the board, legal action is the middle of the board.
        Otherwise, the legal actions are the positions around the current pieces
        """
        if len(self.board) == 0:
            return [((self.boardSize + 1) / 2, (self.boardSize + 1) / 2)]

        return list(self.legalActions)

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
            print "Agent index " + str(playerIndex) + " is invalid."
            return False
        # Out of bounds or that position already has a piece
        if not self.withinBounds(move) or move in self.board:
            return False
        return True

    def generateSuccessor(self, player, move):
        """
        Make a copy of the current state, and simulate the move, and return that copy.
        """
        state = GameState(self.N, self.boardSize, self.numPlayers, prevState = self)
        state.previousAction = (player, move)
        state.makeMove(player, move)
        return state

    def makeMove(self, player, move):
        """
        Player makes a move.
        """
        if not self.moveIsValid(player, move):
            return
        
        # Update self.features
        self.board[move] = player
        self.updateFeaturesForMove(player, move)
        if self.checkTie():
            self.gameOver = True

        self.currentPlayer = (self.currentPlayer + 1) % self.numPlayers

        # Update self.legalActions
        x, y = move
        if move in self.legalActions:
            self.legalActions.remove(move)
        for i in range(x - 1, x + 1 + 1):
            for j in range(y - 1, y + 1 + 1):
                if self.withinBounds((i, j)) and (i, j) not in self.board:
                    self.legalActions.add((i, j))

    def getFeatures(self, index):
        # Return the features that we need for evaluationFunction
        # (not the features in state.features)
        result = []
        for feature in self.features:
            num = self.features[feature]
            agentIndex = feature[0]
            description = feature[1]
            newFeature = (description, num, index == agentIndex, self.currentPlayer == index)
            result.append(newFeature)

        return result


    def __str__(self):
        s = '   |'
        for i in range(self.boardSize):
            if i < 10:
                s += ' ' + str(i) + ' |'
            else:
                s += ' ' + str(i) + '|'
        s += "\n" + (4 * (self.boardSize + 1) * "-") +'\n'
        for y in range(self.boardSize):
            if y < 10:
                s += '  ' + str(y) + '|'
            else:
                s += ' ' + str(y) + '|'
            for x in range(self.boardSize):
                if (x, y) not in self.board:
                    s += '   |'
                else:
                    s += ' ' + str(self.board[(x,y)]) + ' |'
            s += "\n" + (4 * (self.boardSize + 1) * "-") +'\n'
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
        # import pdb; pdb.set_trace();

        x, y = move
        # print move
        # print str(self)


        ############ Horizontal ############
        neighbors1 = self.checkNeighboringRows(move, [(i, y) for i in range(x + 1, self.boardSize + 1)])
        # print neighbors1
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
            return (-1, 0, 1, set())
        # Open end (no neighbors)
        if piecesRange[0] not in self.board:
            return (-1, 0, 0, set())

        piecesInFeature = set()
        player = self.board[piecesRange[0]]
        num = 0
        blocked = 0
        for piece in piecesRange:

            if not self.withinBounds(piece) or (piece in self.board and self.board[piece] != player):
                blocked = 1
                break

            if piece not in self.board:
                break
            # print piece
            piecesInFeature.add(piece)
            # print piecesInFeature
            num += 1
        return (player, num, blocked, piecesInFeature)

    #Delete an instance of a feature from a set of pieces
    def deleteFeatureFromDict(self, dict, featureToDelete, move, setOfPiecesToDeleteFeatureFrom):

        for piece in setOfPiecesToDeleteFeatureFrom:

            if not piece in self.positionToFeatures:
                # self.positionToFeatures[move] = {featureToDelete:set()}
                continue
            if not featureToDelete in self.positionToFeatures[piece]:
                # self.positionToFeatures[move][featureToDelete] = set()
                continue
            # print piece
            self.positionToFeatures[piece][featureToDelete].discard(frozenset(setOfPiecesToDeleteFeatureFrom))
            if len(self.positionToFeatures[piece][featureToDelete]) == 0:
                del self.positionToFeatures[piece][featureToDelete]
            if len(self.positionToFeatures[piece]) == 0:
                del self.positionToFeatures[piece]

    #Add an instance of a feature for a set of pieces
    #The structure of the positionToFeatures is:
    #positionToFeatures - Dict of move : Dict(player index,feature) key,value pairs
    #Dict(player index, feature) is a dict of (player index, feature) : Set of frozen sets
    #The set contains frozen sets, where the frozen sets are the pieces that are in one instance of the feature
    #So the overall structure is dict:dict:set:set of (x,y) coordinates
    def addPiecesToFeatureInDict(self, dict, move, feature, piecesList):
        # print "Adding feature: ", feature, "| For move: ", move, "| Pieces: ", piecesList
        for piece in piecesList:
            if not piece in self.positionToFeatures:
                self.positionToFeatures[piece] = {feature:set()}
            if not feature in self.positionToFeatures[piece]:
                self.positionToFeatures[piece][feature] = set()
            self.positionToFeatures[piece][feature].update([frozenset(piecesList)])
        # self.positionToFeatures[move][feature].append(piecesInFeature)

    def updateFeature(self, player, move, neighbors1, neighbors2):
        """
        Delete/Update the features of the neighbors.
        For example, if neighbor is an open 3 from a different player,
        then update it to be a blocked 3.

        Then, add a new feature according to the given move and its neighbors.
        Parameters: neighbors: (playerIndex, num, blocked, piecesInFeature)
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
                                                #Delete feature from

                        self.deleteFeatureFromDict(self.positionToFeatures, featureToDelete, move, neighbor[3])                        

                        util.deleteItemFromDict(self.features, featureToDelete)
                        featureToAdd = (neighbor[0], 'blocked ' + str(num))

                        piecesInFeature = neighbor[3]
                        self.addPiecesToFeatureInDict(self.positionToFeatures, move, featureToAdd, piecesInFeature)
                        util.addItemToDict(self.features, featureToAdd)
                    else: # blocked
                        featureToDelete = (neighbor[0], 'blocked ' + str(num))

                        self.deleteFeatureFromDict(self.positionToFeatures, featureToDelete, move, neighbor[3])                        
                        util.deleteItemFromDict(self.features, featureToDelete)
            else:
                # neighbor is the same player, so delete the feature
                if num >= 2:
                    if neighbor[2] == 0: # not blocked
                        featureToDelete = (neighbor[0], 'open ' + str(num))

                        self.deleteFeatureFromDict(self.positionToFeatures, featureToDelete, move, neighbor[3])                        
                        util.deleteItemFromDict(self.features, featureToDelete)
                    else: # blocked
                        featureToDelete = (neighbor[0], 'blocked ' + str(num))
                        self.deleteFeatureFromDict(self.positionToFeatures, featureToDelete, move, neighbor[3])                        

                        util.deleteItemFromDict(self.features, featureToDelete)

        # Add a new feature according to the given move and its neighbors.
        num = 1
        blocked = 0
        piecesInFeature = set([move])
        # import pdb; pdb.set_trace();

        # print "Neighbor 1", neighbors1
        for neighbor in [neighbors1]:
            if neighbor[0] != player:
                break
            piecesInFeature.update(neighbor[3])

        # print "Neighbor 2", neighbors2
        for neighbor in [neighbors2]:
            if neighbor[0] != player:
                break
            piecesInFeature.update(neighbor[3])
        # print "Move:", move, "| Pieces In Feature", piecesInFeature

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
        self.addPiecesToFeatureInDict(self.positionToFeatures, move, feature, piecesInFeature)
        # print "Pieces in feature with: ", move, self.positionToFeatures[move][feature]
