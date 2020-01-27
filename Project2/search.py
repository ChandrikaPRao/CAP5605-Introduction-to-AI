    # search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    This function takes the start state of a search problem and applies the \
    depth first search strategy to find the goal state.
    """
    from game import Directions
    South = Directions.SOUTH
    West = Directions.WEST
    East = Directions.EAST
    North = Directions.NORTH
    """Frontier is initialized to LIFO stack"""
    frontier = util.Stack()
    frontier.push(problem.getStartState())
    explored = set()
    leafnode = []
    solution = []
    j=1
 
    while True:
        if frontier.isEmpty():
            print "Frontier is empty and hence a FAILURE!"
            break

        leafnode=frontier.pop()        
        if j==1:
            ln = leafnode
            prevfringedata = []
        else:
            leafnodelist = list(leafnode)
            lnlength = len(leafnodelist)           
            ln = leafnodelist[lnlength-3]
            prevfringedata = leafnodelist[-lnlength-3:]
            solution = prevfringedata
            
        if problem.isGoalState(ln):
            solution = prevfringedata[1::3]
            return solution
            break        
        explored.add(ln)
        for successor in problem.getSuccessors(ln):
            numofsuccessors = 0
            if (successor[0] not in explored):
                fringedata = list(prevfringedata)+list(successor)
                frontier.push(fringedata)                 
                numofsuccessors+=1   
        j+=1
    
    util.raiseNotDefined()
    
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    This function takes the start state of a search problem and applies the \
    breadth first search strategy to find the goal state.
    """
    from game import Directions
    South = Directions.SOUTH
    West = Directions.WEST
    East = Directions.EAST
    North = Directions.NORTH
    """Frontier is initialized to FIFO queue"""
    frontier = util.Queue()
    frontier.push(problem.getStartState())
    explored = set()
    leafnode = []
    solution = []
    j=1

    while True:
        if frontier.isEmpty():
            print "Frontier is empty and hence a FAILURE!"
            break

        leafnode=frontier.pop()       
        if j==1:
            ln = leafnode
            prevfringedata = []
        else:
            leafnodelist = list(leafnode)
            lnlength = len(leafnodelist)           
            ln = leafnodelist[lnlength-3]
            prevfringedata = leafnodelist[-lnlength-3:]
            solution = prevfringedata
            
        if problem.isGoalState(ln):
            solution = prevfringedata[1::3]
            return solution
            break
        
        explored.add(ln)
        for successor in problem.getSuccessors(ln):
            if (successor[0] not in explored):
                fringedata = list(prevfringedata)+list(successor)
                frontier.push(fringedata)                 
                explored.add(successor[0])
        j+=1
    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """
    Search the node of least total cost first. 
    This function takes the start state of a search problem and applies the \
    uniform cost search strategy to find the goal state. A priority queue is \
    used to decided on a successor state to explore.
    Instead of expanding the shallowest node, uniform-cost search
    expands the node n with the lowest path cost g(n). "getCostOfActions" 
    function is used to calculate the path cost.
    """
    root_node = problem.getStartState()
    explored = set()
    frontier = util.PriorityQueue()
    frontier.push((root_node,[]),0)
    while frontier.isEmpty() != True:
        leaf_node, actions = frontier.pop()
        if problem.isGoalState(leaf_node):
            return actions
        if leaf_node not in explored:
            successors = problem.getSuccessors(leaf_node)
            for successor in successors:
                if successor[0] not in explored:
                    direction = successor[1]
                    path_cost = actions + [direction]
                    frontier.push((successor[0],actions + [direction]), \
                                  problem.getCostOfActions(path_cost))              
        explored.add(leaf_node)
    return actions
    util.raiseNotDefined()
           
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the \
    nearest goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    This function takes the start state of a search problem and applies the \
    uniform cost search strategy to find the goal state. A priority queue is \
    used to decided on a successor state to explore.
    A* star search expands the node that has the lowest combined cost g(n) \
    and heuristic h(n). "getCostOfActions" function is used to calculate the \
    cost g(n).
    """
    
    root_node = problem.getStartState()
    explored = set()
    frontier = util.PriorityQueue()
    frontier.push((root_node, []), heuristic(root_node, problem))
    h_Cost = 0
    while frontier.isEmpty() != True:
        leaf_node, actions = frontier.pop()
        if problem.isGoalState(leaf_node):
            return actions
        if leaf_node not in explored:
            successors = problem.getSuccessors(leaf_node)
            for successor in successors:
                if successor[0] not in explored:
                    direction = successor[1]
                    path_cost = actions + [direction]
                    h_Cost = problem.getCostOfActions(path_cost) + \
                    heuristic(successor[0], problem)
                    frontier.push((successor[0], actions + [direction]),h_Cost)
        explored.add(leaf_node)
    return actions
    util.raiseNotDefined()
    
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
