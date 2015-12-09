import sys
from util import *
import random
import pickle

#Class agent is lifted directly from the pacman code
class Agent:
  """
  An agent must define a getAction method, but may also define the
  following methods which will be called if they exist:

  def registerInitialState(self, state): # inspects the starting state
  """
  def __init__(self, index=0):
    self.index = index

  def getAction(self, state):
    """
    The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
    must return an action from Directions.{North, South, East, West, Stop}
    """
    raiseNotDefined()

class MinimaxAgent(Agent):
    """
      Your minimax agent with alpha-beta pruning 
    """

    WINNING_SCORE = 100000 # a very big number

    def __init__(self, index, verbose, depth = 2, branchingFactor = 5, hardCodedWeights = False):
        self.index = index
        self.depth = depth
        self.branchingFactor = branchingFactor
        self.hardCodedWeights = hardCodedWeights

        try:
            with open('weightVector.p', 'rb') as f:
                self.weights = pickle.load(f)
                f.close()
        except IOError:
            self.weights = {}
        self.discount = 1
        self.verbose = verbose

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        # a <= score <= b
        def recurseWithAlphaBeta(state, d, agentIndex, a, b):
            if state.gameEnded():
                if state.getWinner() == self.index:
                    return (self.WINNING_SCORE, None)
                else:
                    return (self.WINNING_SCORE, None)
            if d == 0 and agentIndex == self.index:
                return (self.evaluationFunction(state), None)

            nextAgentIndex = (agentIndex + 1) % state.numPlayers
            legalMoves = state.getLegalActions()
            if len(legalMoves) == 0:
                # This happens when there's a tie
                return (0, None)

            # evaluate and sort legal actions
            prunedLegalMoves = self.selectActions(state, legalMoves, agentIndex)

            if agentIndex == self.index: # this agent
                bestScore = float('-inf')
                bestActions = []
                for _, action, nextState  in prunedLegalMoves:
                    score, _ = recurseWithAlphaBeta(nextState, d - 1, nextAgentIndex, a, b)
                    score *= self.discount # Add discount
                    if score > bestScore:
                        bestScore = score
                        bestActions = [action]
                    elif score == bestScore:
                        bestActions.append(action)
                    a = max(a, bestScore)
                    if a > b:
                        break
                return (bestScore, random.choice(bestActions))

            else: # all other agents
                worstScore = float('inf')
                for _, action, nextState  in prunedLegalMoves:
                    score, _ = recurseWithAlphaBeta(nextState, d, nextAgentIndex, a, b)
                    score *= self.discount
                    if score < worstScore:
                        worstScore = score
                    b = min(b, worstScore)
                    if b < a:
                        break
                return (worstScore, None)
            
        score, action = recurseWithAlphaBeta(gameState, self.depth, self.index, float('-inf'), float('inf'))
        if self.verbose:
            print score
        return action


    def selectActions(self, state, legalMoves, agentIndex):
        estimates = [] # estimates of the next state
        for action in legalMoves:
            nextState = state.generateSuccessor(agentIndex, action)
            if nextState.gameEnded():
                # if it's a game winning move
                return [(self.WINNING_SCORE, action, nextState)]
            estimates.append((self.evaluationFunction(nextState), action, nextState))

        if agentIndex == self.index:
            # Max agent
            estimates.sort(key = lambda x: -x[0])
        else:
            # Min agent
            estimates.sort(key = lambda x: x[0])
        return estimates[:self.branchingFactor]


    def evaluationFunction(self, state):
        if not self.hardCodedWeights:
            score = 0
            features = state.getFeatures(self.index)
            featureVector = {key:1 for key in features}
            return dotProduct(featureVector, self.weights)
        else:
            # original implementation
            weights = {'blocked 2': 1, 'open 2': 2, 'blocked 3': 10, 'open 3': 50, 'blocked 4': 50, 'open 4': self.WINNING_SCORE / 5, 'open 5': self.WINNING_SCORE, 'closed 5': self.WINNING_SCORE}
            score = 0
            for feature in state.features:
                num = state.features[feature]
                agentIndex = feature[0]
                description = feature[1]
                if description in weights:
                    if agentIndex == self.index:
                        score += weights[description] * num
                    else:
                        score -= weights[description] * num
            return score


    def updateWeights(self, weights):
        self.weights = dict(weights)


class RandomAgent(Agent):
    def __init__(self, index, verbose):
        self.index = index
        self.verbose = verbose

    def getAction(self, state):
        return random.choice(state.getLegalActions())

    def updateWeights(self, weights):
        return

class HumanAgent(Agent):
    def __init__(self, index):
        self.index = index
    def getAction(self, state):
        player = self.index
        while True:
            print "Player " + str(player) + ": Please Enter your next move (In form X,Y)"

            #Process coordinate input
            coordinates = sys.stdin.readline().strip().split(",")
            validInput = len(coordinates) == 2 and isInt(coordinates[0]) and isInt(coordinates[1])
            if validInput:
                coordinates = (int(coordinates[0]), int(coordinates[1])) #Convert to tuple of ints
            else:
                continue

            #Play move if it's valid
            if state.moveIsValid(player, coordinates):
                return coordinates
            else:
                print "Move is invalid."
                continue
