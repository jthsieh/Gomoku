import sys
from util import isInt
import random

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
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    # a <= score <= b
    def recurseWithAlphaBeta(state, d, agentIndex, a, b):
        if state.isWin() or state.isLose():
            return (state.getScore(), None)
        if d == 0 and agentIndex == self.index:
            return (self.evaluationFunction(state), None)

        nextAgentIndex = (agentIndex + 1) % state.getNumAgents()
        legalMoves = state.getLegalActions(agentIndex)
        if len(legalMoves) == 0:
            return (state.getScore(), None)

        if agentIndex == self.index: # pacman
            bestScore = float('-inf')
            bestActions = []
            for action in legalMoves:
                nextState = state.generateSuccessor(agentIndex, action)
                score, _ = recurseWithAlphaBeta(nextState, d - 1, nextAgentIndex, a, b)
                if score > bestScore:
                    bestScore = score
                    bestActions = [action]
                elif score == bestScore:
                    bestActions.append(action)
                a = max(a, bestScore)
                if a > b:
                    break
            return (bestScore, random.choice(bestActions))
        else: # ghost, doesn't need to return an action
            worstScore = float('inf')
            for action in legalMoves:
                nextState = state.generateSuccessor(agentIndex, action)
                score, _ = recurseWithAlphaBeta(nextState, d, nextAgentIndex, a, b)
                if score < worstScore:
                    worstScore = score
                b = min(b, worstScore)
                if b < a:
                    break
            return (worstScore, None)
        
    score, action = recurseWithAlphaBeta(gameState, self.depth, self.index, float('-inf'), float('inf'))
    return action


class RandomAgent(Agent):
	def __init__(self, index):
		self.index = index

	def getAction(self, state):
		xAxis = range(state.boardSize)
		random.shuffle(xAxis)

		yAxis = range(state.boardSize)
		random.shuffle(yAxis)
		for x in xAxis:
			for y in yAxis:
				move = (x,y)
				if state.moveIsValid(self.index, move):
					print "Player " + str(self.index) + " has moved at " + str(move)
					return move

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
				continue
