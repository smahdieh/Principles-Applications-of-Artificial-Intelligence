# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        ghost_distance = min([manhattanDistance(newPos, ghost_state.getPosition()) for ghost_state in newGhostStates])
        if action == Directions.STOP or ghost_distance <= 1:
            return -5000
        
        scare_time = sum(newScaredTimes)
        if scare_time > 0:
            ghost_distance = 0

        foods_distance = [manhattanDistance(newPos, food) for food in newFood.asList()]

        if foods_distance:
            nearest_food = min(foods_distance)
        else :
            nearest_food = 0

        return 2 * scare_time / 10 + (10 / (nearest_food + 1)) + (3 * ghost_distance / 10) + 4 * successorGameState.getScore() / 10


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        Infinity = float('inf')

        def maxValue(gameState, depth):
            actions = gameState.getLegalActions(0)

            if not actions or depth == self.depth:   #Terminal Test 
                return self.evaluationFunction(gameState)
            
            v = -Infinity
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                v = max (v, minValue(successor, depth + 1, 1))
            return v
        
        def minValue(gameState, depth, agentIndex):
            actions = gameState.getLegalActions(agentIndex)

            if not actions:   #Terminal Test 
                return self.evaluationFunction(gameState)
            
            v = Infinity
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                
                # last ghost
                if agentIndex == (gameState.getNumAgents() - 1):
                    v = min (v, maxValue(successor, depth))
                else:
                    v = min (v, minValue(successor, depth, agentIndex + 1))
            return v
        

        # Root level action
        actions = gameState.getLegalActions(0)
        v = -Infinity
        bestAction = actions[0]
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            # Next level is a min level
            newV = minValue(successor, 1, 1)
            # Choosing the action which is Maximum of the successors.
            if newV > v:
                bestAction = action
                v = newV
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        Infinity = float('inf')

        def minValue(state, depth, agentIndex, a, b):
            actions = state.getLegalActions(agentIndex)
            if not actions:
                return self.evaluationFunction(state)

            v = Infinity
            for action in actions:
                successor = state.generateSuccessor(agentIndex, action)

                # last ghost
                if agentIndex == (state.getNumAgents() - 1):
                    v = min (v, maxValue(successor, depth, a, b))
                else:
                    v = min (v, minValue(successor, depth, agentIndex + 1, a, b))

                if v < a:
                    return v
                b = min(b, v)
            return v

        def maxValue(state, depth, a, b):
            actions = state.getLegalActions(0)
            if not actions or depth == self.depth:
                return self.evaluationFunction(state)

            v = -Infinity
            
            for action in actions:
                successor = state.generateSuccessor(0, action)
                v = max(v, minValue(successor, depth + 1, 1, a, b))

                if v > b:
                    return v
                a = max(a, v)

            return v

        # Root level action
        actions = gameState.getLegalActions(0)
        v = -Infinity
        a = -Infinity
        b = Infinity
        bestAction = actions[0]

        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            # Next level is a min level. Hence calling min for successors of the root.
            newV = minValue(successor, 1, 1, a, b)
            # Choosing the action which is Maximum of the successors.
            if newV > v:
                bestAction = action
                v = newV
               
            if newV > b:
                return bestAction
            a = max(a,newV)
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        Infinity = float('inf')

        def maxValue(gameState,depth):

            actions = gameState.getLegalActions(0)
            if not actions or depth == self.depth:
                return self.evaluationFunction(gameState)

            v = -Infinity
            for action in actions:
                successor= gameState.generateSuccessor(0, action)
                v = max (v, expectedValue(successor, depth + 1, 1))
            return v
        
        #For all ghosts.
        def expectedValue(gameState, depth, agentIndex):

            actions = gameState.getLegalActions(agentIndex)
            if not actions:
                return self.evaluationFunction(gameState)

            v = 0.0
            p = 1 / len(actions)
            for action in actions:
                successor= gameState.generateSuccessor(agentIndex, action)

                # last ghost
                if agentIndex == (gameState.getNumAgents() - 1):
                    v += p * maxValue(successor, depth) 
                else:
                    v += p * expectedValue(successor, depth, agentIndex + 1) 
            return v
        
        #Root level action.
        actions = gameState.getLegalActions(0)
        v = -Infinity
        bestAction = actions[0]
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            # Next level is a expect level.
            newV = expectedValue(successor, 1, 1)
            # Choosing the action which is Maximum of the successors.
            if newV > v:
                bestAction = action
                v = newV
        return bestAction
       

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    Don't forget to use pacmanPosition, foods, scaredTimers, ghostPositions!
    DESCRIPTION: <write something here so we know what you did>
    """
    pacmanPosition = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimers = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPositions = currentGameState.getGhostPositions()
    
    "*** YOUR CODE HERE ***"
    ghost_distance = min([manhattanDistance(pacmanPosition, ghost_pos) for ghost_pos in ghostPositions])

    scare_time = sum(scaredTimers)
    if scare_time > 0:
        ghost_distance = 0

    foods_distance = [manhattanDistance(pacmanPosition, food) for food in foods.asList()]

    if foods_distance:
        nearest_food = min(foods_distance)
    else :
        nearest_food = 0
    
    # calculate score achieved from CAPSULES. the closer the capsules, the higher the evaluation function's result
    capsuleList = currentGameState.getCapsules()
    capsuleScore = 0
    capsuleDistsInverse = [10.0 / manhattanDistance(pacmanPosition, capsule) for capsule in capsuleList]
    if len(capsuleDistsInverse)==0:
        capsuleScore = 0
    else:
        capsuleScore = max(capsuleDistsInverse)

    return capsuleScore + scare_time + (10 / (nearest_food + 1)) + (3 * ghost_distance / 10) + 4 * currentGameState.getScore() / 10


# Abbreviation
better = betterEvaluationFunction
