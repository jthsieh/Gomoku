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