# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    
#     Depth First Search
#     Data Structure Used : Stack
#     Searches the deepest nodes in the search tree first.
#     This algorithm return a list of actions that reaches the
#     goal.
#     
#     We use the visited array to mark nodes as we visit them and no nodes are marked until they
#     are visited.
#     Space Optimization:
#     We use a dictionary of parent-child key pairs that update themselves as we move through the search tree nodes.
#     This helps us to maintain just a single mapping data structure for the whole tree in order to avoid creating 
#     repeated lists with path nodes.    
    
    startState = problem.getStartState()
    stack = util.Stack()
    stack.push((startState,'None',0))
    visited = []
    parent = {}
    currentState = None
    while(not stack.isEmpty()):
        currentState = stack.pop()
        if problem.isGoalState(currentState[0]):
            break
        
        if currentState[0] not in visited:
            visited.append(currentState[0])
            for successor in problem.getSuccessors(currentState[0]):
                if successor[0] not in visited:
                    parent[successor] = currentState
                    stack.push(successor)
    
    #Since actions were stored in reverse order, we need to reverse them in order to get root to goal path.
    actions = []
    statePointer = currentState
    actions.append(statePointer[1])
    if problem.isGoalState(currentState[0]):
        while parent[statePointer][0] != problem.getStartState():
            actions.append(parent[statePointer][1])
            statePointer = parent[statePointer]
    actions.reverse()
    return actions
    
def breadthFirstSearch(problem):
    
#     Searches the shallowest nodes in the search tree first.
#     Data Structure Used : Queue
#     We implement BFS with the help of our common utility function common_bfs(problem,heuristic,algoType)
#     Since simple BFS doesn't have a heuristic, we pass None as second parameter in which case the utility
#     function ignores the cost calculation and heuristic calculation altogether.
#     As per the algorithm, the shallow nodes are expanded first and no node is mark visited until it is fully explored.
    
    return common_bfs(problem,None,'bfs')

def uniformCostSearch(problem):
    
    #Implementation of UCS algorithm
    # Data Structure Used : PriorityQueue
    # This algorithm is an extension of BFS such that we start to consider the cost/weight associated 
    # with each path in the nodes.
    # The priorityQueue ensures that the least cost path is chosen first and the node expansion starts in
    # that direction.
    
    return common_bfs(problem,None,'ucs')

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    # Implementation of A* Algorithm
    # Data Structure Used : PriorityQueue
    # Cost Function f(n) : current_path_cost g(n) + heuristic_function h(n)
    # This algorithm tries to expand nodes towards the direction of the goal rather than expanding nodes in all
    # directions.
    # The successor cost is calculated by adding all the cost from source to current successor along with a heuristic value.
    return common_bfs(problem,heuristic,'astar')


def common_bfs(problem, heuristic=nullHeuristic, algoType = 'bfs'):
    #Common Utility function to cater the BFS algorithm and its extensions.
    
    #Getting source node from the problem
    startState = problem.getStartState()
    
    #Initializing a priority Queue to store nodes
    queue = util.PriorityQueue()
    
    #Pushing the initial node in a "List" in order to store path information
    queue.push([(startState,'STOP',0)],0)
    
    currentState = None
    visited = []
    while(not queue.isEmpty()):
        #Returns the first list with minimum corresponding value in the priority queue.
        currentList = queue.pop()
        
        #Extract the last node from the current list as this node is the one to be processed. Rest all the previous
        #nodes are stored only for path information.
        currentState = currentList[-1]
        
        #If goal node is found, the actions from the current list are returned in the order from root to goal state.
        if problem.isGoalState(currentState[0]):
            traversal = [node[1] for node in currentList if node[1] != 'STOP']
            return traversal
        
        #We check if the current state has already been visited, if not, we mark it visited and explore all its children.
        if currentState[0] not in visited:
            visited.append(currentState[0])
            #Visit all the successors of the current node.
            for successor in problem.getSuccessors(currentState[0]):
                if(successor[0] not in visited):
                    #If we find a new successor, we create a copy of the current path list and append this successor at the
                    #end in order to be processed during next iterations.
                    newParentPath = currentList[:]
                    newParentPath.append(successor)
                    
                    # The sum stores the "SUM" of all the costs from root to current successor. This is used to determine the 
                    #priority value of a node in UCS and ASTAR algorithms.
                    sum = 0
                    for node in newParentPath:
                        sum += node[2]
                        
                    #If the algo type is "UCS" we simply use the path cost as priority value of a node.    
                    if(algoType == 'ucs'):
                        queue.push(newParentPath,sum)
                    #If the algo type is "ASTAR" we use the combination of path cost and heuristic function for priority value.    
                    elif(algoType == 'astar'):
                        queue.push(newParentPath,sum + heuristic(successor[0],problem))
                    # If the algo type is "BFS", we simply pass the cost as 1 for all the nodes, making a priority queue to simulate
                    # like a normal queue data structure.    
                    else:
                        queue.push(newParentPath,1)
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
