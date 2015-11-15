import random
import os
import sys
from gameState import *
from agents import *
from util import *

<<<<<<< HEAD
#function createBoard:
#--------------------
#Create a grid of size n by n
def createBoard(n):
	#Generate rows with length of n
	board = []
	for row in range(n):
	# Append a blank list to each row cell
		board.append([])
		for column in range(n):
		# Assign x to each row
			board[row].append('X')
	return board

#Create the graphic of the current board
def drawBoard(board):
	# This function prints out the board that it was passed.
	# "board" is a list of 10 strings representing the board (ignore index 0)
	length = len(board)
	for i in range(0, length):
		print('-----------------------')
		for j in range(0, length):
			if j == length - 1:
				print(' ' + board[i][j] + ' ')
			else:
				print(' ' + board[i][j] + ' |'),
	return 0

def runGames():
	print('Welcome to our Gomoku game for CS221')
	while True:
		myBoard = createBoard(5)
		playerOneLetter, playerTwoLetter = ('X', 'O')
		gameIsPlaying = True
		turn = 'playerOne'
		while gameIsPlaying:
			if turn == 'playerOne':
			#Player 1's turn
				drawBoard(myBoard)
			break
		break
	return 0
=======
>>>>>>> 0d322b335ab23dd0e89b27696540c099b939ed58

class Game:

	def __init__(self):
		self.agents = []
		self.moveHistory = []

	#Runs a full game until completion
	def runGames(self, gridSize, nInARow, numComputerAgents, numHumanAgents):
		self.state = GameState(nInARow, gridSize, numComputerAgents + numHumanAgents)
		print self.state

		agentIndex = 0

		while not self.state.gameEnded():
			agent = self.agents[agentIndex]
			
			action = agent.getAction(self.state)

			self.moveHistory.append(action)
			self.state = self.state.generateSuccessor(agentIndex, action)

			print self.state

			# self.state.makeMove(agentIndex, action)
			agentIndex = (agentIndex + 1) % len(self.agents)

		print "Game has ended!"
		if self.state.getWinner() == -1:
			print "The game was a tie."
		else:
			print "Player " + str(self.state.getWinner()) + " won the game!"
				
		return 0



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
	def repl(self, args):
		#Defaults
		gridSize = 5
		nInARow = 5
		numComputerAgents = 1
		numHumanAgents = 1

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
		if len(args) > 4:
			print "\nDid not enter valid arguments!"
			print argumentsString
			return
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
			computer = MinimaxAgent(len(self.agents))
			self.agents.append(computer)

		#TODO: Allow the user to play another game after completing one game
		while True:
			self.runGames(gridSize, nInARow, numComputerAgents, numHumanAgents)
			break

if __name__ == '__main__':
	args = sys.argv[1:] # Get game components based on input
	game = Game()
	game.repl(args)

