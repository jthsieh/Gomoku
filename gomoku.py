import random
import os
import sys
import pickle
import time
from gameState import *
from agents import *
from util import *

class Game:

    def __init__(self):
        self.agents = []
        self.moveHistory = []

    def learnWeights(self, gridSize, nInARow, numComputerAgents, numHumanAgents, verboseFlag, learningAgentIndex, numberOfGames):
        self.state = GameState(nInARow, gridSize, numComputerAgents + numHumanAgents)

        weightVector = None
        try:
            with open( "weightVector.p", "rb" ) as f:
                weightVector = pickle.load(f)
        except IOError:
            weightVector = {}

        for gameNum in range(numberOfGames):
            agentIndex = 0
            while not self.state.gameEnded():
                s = self.state
                reward = 0
                agent = self.agents[agentIndex]
                action = agent.getAction(self.state)

                self.moveHistory.append((agentIndex, action))
                self.state = self.state.generateSuccessor(agentIndex, action)
                sPrime = self.state

                if sPrime.gameEnded():
                    if sPrime.getWinner() == agentIndex:
                        reward = 100000
                    else:
                        reward = - 100000

                sars = (s, action, reward, sPrime)

                def updateWeightVector(weightVector, sars):
                    gamma = 1.0
                    step = 0.5
                    (state, action, reward, successorState) = sars

                    stateNewFeatures = state.getFeatures(agentIndex)
                    successorStateNewFeatures = successorState.getFeatures(agentIndex)

                    stateFeatureVector = {key:1 for key in stateNewFeatures}
                    successorStateFeatureVector = {key:1 for key in successorStateNewFeatures}
                    print "StateFeatureVector: ", stateFeatureVector
                    print "successorStateFeatureVector: ", successorStateFeatureVector

                    for key in stateFeatureVector.keys():
                        if not key in weightVector:
                            weightVector[key] = 0
                        if not key in stateNewFeatures:
                            stateFeatureVector[key] = 0
                        if not key in successorStateNewFeatures:
                            successorStateFeatureVector[key] = 0
                            
                        weightVector[key] = weightVector[key] - step * (dotProduct(weightVector, stateFeatureVector)-(reward + gamma * dotProduct(successorStateFeatureVector, weightVector))) * stateFeatureVector[key]
                updateWeightVector(weightVector, sars)
                agentIndex = (agentIndex + 1) % len(self.agents)


        pickle.dump(weightVector, open( "weightVector.p", "wb" ) )


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

        stats["winner"] = self.state.getWinner()
        stats["numMoves"] = numberOfMoves
        stats["avgMoveTime"] = dict((agent, agentTimeTaken[agent]/(numberOfMovesPerPlayer + oneMoreMove(agent, lastPlayer))) for agent in agentTimeTaken)
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
        # numGames - Number of games to play
        # verboseFlag - Print boards for each turn and other turn data. "verbose" will turn this on (default: False)
        # agentTypes - a string of structure 'mrmm', where each letter defines the AI agent type. m - Minimax. r - random
    def repl(self, args):
        #Defaults
        numArgs = 8
        gridSize = 19
        nInARow = 5
        numComputerAgents = 1
        numHumanAgents = 1
        numberOfGames = 1
        verbose = False
        learningAgentIndex = None
        learningMode = False

        argumentsString = '''
        ============================================
        Arguments (in order):
        ============================================
        gridSize - Int representing the NxX dimension of the board (default: 5)
        nInARow - Int representing the number of pieces in a row to win (default: 5)
        numComputerAgents - Number of AI agents the user will play against (default: 1)
        numHumanAgents - Number of human players in this game (default: 1)
        numGames - Number of games to play
        verboseFlag - Print boards for each turn and other turn data. "verbose" will turn this on (default: False)
        agentTypes - a string of structure 'mrmm', where each letter defines the AI agent type. m - Minimax. r - random
        '''

        #Parse arguments
        if len(args) > numArgs:
            print "\nDid not enter valid arguments!"
            print argumentsString
            return
        if len(args) > 7 and isInt(args[7]):
            learningAgentIndex = int(args[7])
            learningMode = True
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
        if len(args) > 6: #Parse what kind of agents
            print args[6]
            if numComputerAgents != len(args[6]):
                print "\nDid not enter valid arguments!"
                print argumentsString
                return
            for i in range(numComputerAgents):
                queryString = args[6]
                agentType = None
                if queryString[i] == "m":
                    agentType = MinimaxAgent(len(self.agents), verbose)
                elif queryString[i] == "r":
                    agentType = RandomAgent(len(self.agents), verbose)
                else:
                    print "\nDid not enter valid arguments! Invalid agent types"
                    print argumentsString
                    return
                self.agents.append(agentType)
        else: #Setup computer agents (default)
            for j in range(numComputerAgents):
                computer = MinimaxAgent(len(self.agents), verbose)
                print computer.index
                self.agents.append(computer)

        print('Welcome to our Gomoku game for CS221')
        print "Grid Size: " + str(gridSize)
        print "N in a row: " + str(nInARow)
        print "Computers: " + str(numComputerAgents)
        print "Humans: " + str(numHumanAgents) + "\n"

        #Setup Human agents
        for i in range(numHumanAgents):
            human = HumanAgent(len(self.agents))
            self.agents.append(human)

        numMoves = 0
        avgMoveTime = {agent:0 for agent in range(numComputerAgents + numHumanAgents)}
        wins = {agent: 0 for agent in range(numComputerAgents + numHumanAgents)}
        wins[-1] = 0 #Keep track of ties


        if learningMode:
            self.learnWeights(gridSize, nInARow, numComputerAgents, numHumanAgents, verbose, learningAgentIndex, numberOfGames)
        else:
            for i in range(numberOfGames):
                gameStats = self.runGames(gridSize, nInARow, numComputerAgents, numHumanAgents, verbose)
                print gameStats

                numMoves += gameStats["numMoves"]
                wins[gameStats["winner"]] += 1
                for agent in gameStats["avgMoveTime"]:
                    avgMoveTime[agent] += gameStats["avgMoveTime"][agent]/numberOfGames

            #Final Statistics
            print "================= Final statistics ==================="
            print "Number of games: " + str(numberOfGames)
            print "Average Total moves in game: " + str(numMoves/numberOfGames)
            print "Average Time Per Move For Each Player: " + str(avgMoveTime)
            print "Wins For Each Player: " + str(wins)
if __name__ == '__main__':
    args = sys.argv[1:] # Get game components based on input
    game = Game()
    game.repl(args)

