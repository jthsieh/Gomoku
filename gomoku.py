import random
import os
import sys
from gameState import GameState

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
	for i in range(0, length)[::-1]:
		print('-----------------------')
		for j in range(0, length):
			if j == length - 1:
				print(board[i][j] + ' ')
			else:
				print(board[i][j] + ' |'),
	return 0

#Currently hardcoded to two human players
def runGames(gridSize, nInARow, numComputerAgents, numHumanAgents):
	gameIsPlaying = True
	gameState = GameState(gridSize, nInARow)

	playerOneLetter, playerTwoLetter = ('X', 'O')
	turn = 'playerOne'
	while not gameState.gameEnded():
		print gameState
		inputString = sys.stdin.readline()
		print "Input: " + str(inputString)
	return 0

# Check if string represents an int
# http://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-int-without-using-try-except
def isInt(str):
	try:
		int(str)
		return True
	except:
		return False

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
def repl(args):
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
	print "Humans: " + str(numHumanAgents)

	#TODO: Allow the user to play another game after completing one game
	while True:
		runGames(gridSize, nInARow, numComputerAgents, numHumanAgents)
		break

if __name__ == '__main__':
	args = sys.argv[1:] # Get game components based on input
	repl(args)
