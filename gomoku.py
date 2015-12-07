import random
import os
import sys
import time
from gameState import *
from agents import *
from util import *

class Game:

	def __init__(self):
		self.agents = []
		self.moveHistory = []

	# Runs a full game until completion
	# Returns a map of statistics, where the keys are:
	# numMoves (int) - the number of moves played by all players
	# avgMoveTime (float) - average time in seconds per move for each player
	def runGames(self, gridSize, nInARow, numComputerAgents, numHumanAgents, verboseFlag):
		#Collect statistics on the game
		stats = {}
		numberOfMoves = 0

		self.state = GameState(nInARow, gridSize, numComputerAgents + numHumanAgents)
		if verboseFlag:
			print self.state

		agentIndex = 0
		agentTimeTaken = {}
		while not self.state.gameEnded():
			# Set agent time taken to 0 if this is the first move
			if not agentIndex in agentTimeTaken:
				agentTimeTaken[agentIndex] = 0

			turnStartTime = time.clock()

			agent = self.agents[agentIndex]
			action = agent.getAction(self.state)

			self.moveHistory.append((agentIndex, action))
			numberOfMoves += 1
			turnEndTime = time.clock()
			self.state = self.state.generateSuccessor(agentIndex, action)

			if verboseFlag:
				print self.state

			agentTimeTaken[agentIndex] += turnEndTime - turnStartTime
			agentIndex = (agentIndex + 1) % len(self.agents)

		print "Game has ended!"
		if self.state.getWinner() == -1:
			print "The game was a tie."
		else:
			print "Player " + str(self.state.getWinner()) + " won the game!"
				
		numberOfMovesPerPlayer = numberOfMoves / len(self.agents) #Integer truncation
		lastPlayer = numberOfMoves % len(self.agents)
		def oneMoreMove(agentIndex, lastPlayer): #Add the last move if the player did move. Needed for average time
			if agentIndex <= lastPlayer:
				return 1
			return 0

		stats["numMoves"] = numberOfMoves
		stats["avgMoveTime"] = dict((agent, agentTimeTaken[agent]/numberOfMovesPerPlayer + oneMoreMove(agent, lastPlayer)) for agent in agentTimeTaken)
		# stats["moveHistory"] = self.moveHistory
		return stats



		# Repl is a read, evaluate, print loop
		# Parses the args entered in the command line to set up the game
		# Ex: python gomoku.py 5 3 1 1
		# ============================================
		# Arguments (in order):
		# ============================================
		# gridSize - Int representing the NxX dimension of the board (default: 5)
		# nInARow - Int representing the number of pieces in a row to win (default: 5)
		# numComputerAgents - Number of AI agents the user will play against (default: 1)
		# numHumanAgents - Number of human players in this game (default: 1)
		# verboseFlag - Print boards for each turn and other turn data (default: False)
	def repl(self, args):
		#Defaults
		numArgs = 6
		gridSize = 19
		nInARow = 5
		numComputerAgents = 1
		numHumanAgents = 1
		numberOfGames = 1
		verbose = False

		argumentsString = '''
		============================================
		Arguments (in order):
		============================================
		gridSize - Int representing the NxX dimension of the board (default: 5)
		nInARow - Int representing the number of pieces in a row to win (default: 5)
		numComputerAgents - Number of AI agents the user will play against (default: 1)
		numHumanAgents - Number of human players in this game (default: 1)
		'''

		#Parse arguments
		if len(args) > numArgs:
			print "\nDid not enter valid arguments!"
			print argumentsString
			return
		if len(args) > 5:
			if args[5] == "verbose" or args[5] == "v" or args[5] == "Verbose":
				verbose = True
		if len(args) > 4 and isInt(args[4]):
			numberOfGames = int(args[4])
		if len(args) > 3 and isInt(args[3]):
			numHumanAgents = int(args[3])
		if len(args) > 2 and isInt(args[2]):
			numComputerAgents = int(args[2])
		if len(args) > 1 and isInt(args[1]):
			nInARow = int(args[1])
		if len(args) >= 1 and isInt(args[0]):
			gridSize = int(args[0])

		print('Welcome to our Gomoku game for CS221')
		print "Grid Size: " + str(gridSize)
		print "N in a row: " + str(nInARow)
		print "Computers: " + str(numComputerAgents)
		print "Humans: " + str(numHumanAgents) + "\n"

		#Setup agents
		for i in range(numHumanAgents):
			human = HumanAgent(len(self.agents))
			self.agents.append(human)
		for j in range(numComputerAgents):
			computer = MinimaxAgent(len(self.agents), verbose)
			self.agents.append(computer)

		#TODO: Allow the user to play another game after completing one game
		for i in range(numberOfGames):
			gameStats = self.runGames(gridSize, nInARow, numComputerAgents, numHumanAgents, verbose)
			print gameStats

if __name__ == '__main__':
	args = sys.argv[1:] # Get game components based on input
	game = Game()
	game.repl(args)

