import random
import os
import sys
from gameState import GameState


#Returns a valid coordinate for the current player to make a move
def getValidMove(player, gameState):
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
		if gameState.moveIsValid(player, coordinates):
			return coordinates
		else:
			continue


#Currently hardcoded to two human players
#Runs a full game until completion
def runGames(gridSize, nInARow, numComputerAgents, numHumanAgents):
	gameIsPlaying = True
	gameState = GameState(nInARow, gridSize)

	playerOneLetter, playerTwoLetter = ('X', 'O')
	turn = 0

	while not gameState.gameEnded():
		print gameState

		#Read input until we get a valid move to play
		move = getValidMove(turn, gameState)
		gameState.makeMove(turn, move)
		turn = (turn + 1) % 2 #TODO: GENERALIZE TO N players

	print gameState
	print "Game has ended!"
	if gameState.getWinner() == -1:
		print "The game was a tie."
	else:
		print "Player " + str(gameState.getWinner()) + " won the game!"
			
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
	print "Humans: " + str(numHumanAgents) + "\n"

	#TODO: Allow the user to play another game after completing one game
	while True:
		runGames(gridSize, nInARow, numComputerAgents, numHumanAgents)
		break

if __name__ == '__main__':
	args = sys.argv[1:] # Get game components based on input
	repl(args)
