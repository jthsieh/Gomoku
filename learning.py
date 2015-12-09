import pickle
import sys
from util import *
from agents import *
from gameState import *


def learnWeights(gridSize, nInARow, verboseFlag, numberOfGames, agents):

    weightVector = None
    try:
        with open( "weightVector.p", "rb" ) as f:
            weightVector = pickle.load(f)
            f.close()
    except IOError:
        weightVector = {}

    wins = [0, 0]

    for gameNum in range(numberOfGames):
        print gameNum
        state = GameState(nInARow, gridSize, 2)
        agentIndex = 0

        while not state.gameEnded():

            def updateWeightVector(weightVector, sars, index):
                gamma = 1.0
                step = 0.5
                (state, action, reward, successorState) = sars

                stateNewFeatures = state.getFeatures(index)
                successorStateNewFeatures = successorState.getFeatures(index)

                stateFeatureVector = {key:1 for key in stateNewFeatures}
                successorStateFeatureVector = {key:1 for key in successorStateNewFeatures}
                if verboseFlag:
                    print "StateFeatureVector: ", stateFeatureVector
                    print "successorStateFeatureVector: ", successorStateFeatureVector

                for key in stateFeatureVector.keys():
                    if not key in weightVector:
                        weightVector[key] = 0
                    if not key in stateNewFeatures:
                        stateFeatureVector[key] = 0
                    if not key in successorStateNewFeatures:
                        successorStateFeatureVector[key] = 0

                    if successorState.gameEnded(): #Do not calculate dot product if sPrime is an end state
                        weightVector[key] = weightVector[key] - step * (dotProduct(weightVector, stateFeatureVector) - reward) * stateFeatureVector[key]
                    else:                    
                        weightVector[key] = weightVector[key] - step * (dotProduct(weightVector, stateFeatureVector) - (reward + gamma * dotProduct(successorStateFeatureVector, weightVector))) * stateFeatureVector[key]

            s = state
            agent = agents[agentIndex]
            action = agent.getAction(state)

            state = state.generateSuccessor(agentIndex, action)
            sPrime = state
            if verboseFlag:
                print sPrime

            for index in range(2):
                reward = 0
                if sPrime.gameEnded():
                    if sPrime.getWinner() == index:
                        reward = 100000
                    else:
                        reward = - 100000

                sars = (s, action, reward, sPrime)
                updateWeightVector(weightVector, sars, index)

            agentIndex = (agentIndex + 1) % 2

        if verboseFlag:
            print 'Winner: ' + str(state.winner)

        if state.winner >= 0:
            wins[state.winner] += 1


    print "================= Final statistics ==================="
    print "Number of games: " + str(numberOfGames)
    print "Player 0: " + str(wins[0]) + ", Player 1: " + str(wins[1])

    pickle.dump(weightVector, open( "weightVector.p", "wb" ) )


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 5:
        print "Invalid arguments"
    else:
        gridSize = int(args[0])
        nInARow = int(args[1])
        verbose = int(args[2])
        numberOfGames = int(args[3])
        agentsQuery = args[4]
        agents = []
        for i in range(2):
            if agentsQuery[i] == 'r':
                agents.append(RandomAgent(i, verbose))
            elif agentsQuery[i] == 'm':
                agents.append(MinimaxAgent(i, verbose))
            else:
                agents.append(MinimaxAgent(i, verbose, hardCodedWeights=True))

        learnWeights(gridSize, nInARow, verbose, numberOfGames, agents)
