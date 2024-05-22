#Importing libraries
from collections import deque
import numpy as np


# Creating Queue Class using deque
class Queue:
    def __init__(self):
        self.items = deque()

    def is_empty(self):
        return not self.items

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.popleft()

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[0]

    def __str__(self):
        return str(self.items)
    
# Define the initial and goal states    

# initial_state = np.array([[8, 6, 7],
#                  [2, 5, 4],
#                  [3, 0, 1]])

# 1 2 8 3 0 6 5 7 4
# initial_state = np.array([[1, 3, 5],
#                  [2, 0, 7],
#                  [8, 6, 4]])

#2 6 1 8 0 3 5 7 4
# initial_state = np.array([[2, 8, 5],
#                  [6, 0, 7],
#                  [1, 3, 4]])

# 6 8 3 4 5 2 7 0 1
initial_state = np.array([[6, 4, 7],
                 [8, 5, 0],
                 [3, 2, 1]])


goal_state = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]])


# Column wise arrays
initial_state = initial_state.T
goal_state = goal_state.T

# Moving empty tile
offsets = {
    "right": (0, 1),
    "left": (0, -1),
    "up": (-1, 0),
    "down": (1, 0)
}

# Blank tile position
def blank_tile_pos(current_state):
    if np.ndim(current_state) == 1:
        current_state = np.array(current_state)
        j = np.where(current_state==0)[0]
        return j[0]

    elif np.ndim(current_state) ==2: 
        i,j=np.where(current_state==0)
        return (i[0],j[0])
    
    else:
        return None

# Is Valid move
def is_valid_move(i, j):
    return 0 <= i < 3 and 0 <= j < 3

# Moving Blank Tile
def move_blank(state,di,dj):

    # get position of blank tile
    blank_i,blank_j=blank_tile_pos(state)

    # new position of blank tile
    new_i,new_j=(blank_i+di),(blank_j+dj)

    if is_valid_move(new_i,new_j):

        #Swaping value with blank tile
        new_state = np.copy(state)
        new_state[blank_i][blank_j] = new_state[new_i][new_j]
        new_state[new_i][new_j] = 0
        
        return new_state
    
    #If Not Valid
    else:
        return None

# Get path
def get_path(predecessor, initial_state, goal_state):

    initial_state = tuple(initial_state.flatten())
    goal_state = tuple(goal_state.flatten())

    current_state = goal_state
    path = []

    while current_state != initial_state:
        path.append(current_state)
        current_state = predecessor[current_state]

    path.append(initial_state)
    path.reverse()
    return path

#get nodes info
def get_nodes_info(predecessor):
    nodes_explored = list(predecessor.items())

    node = []
    node_index = []
    parent_node_index = []

    for nodes in nodes_explored:

        node.append(nodes[0])

        node_index.append(blank_tile_pos(nodes[0]))

        parent_node_index.append(blank_tile_pos(nodes[1]))
    

    node_info = list(zip(node_index,parent_node_index,node))

    return (node_info,node)



#bfs
def bfs(initial_state, goal_state):

    #Initialize
    my_queue = Queue()

    my_queue.enqueue(initial_state)

    predecessor = {tuple(initial_state.flatten()):None}

    while not my_queue.is_empty():

        #Dequeue
        current_state = my_queue.dequeue()

        #Check if goal reached
        if np.array_equal(current_state,goal_state):
            
            return get_path(predecessor, initial_state, goal_state),get_nodes_info(predecessor)
        
        
        #If goal not reached add undiscover states to my_queue and update visited

        # Moving in clockwise direction
        for direction in ["up","right","down","left"]:

            row_offset,col_offset=offsets[direction]

            new_state = move_blank(current_state,row_offset,col_offset)

            #Check the validity and if is already visited
            if (new_state is not None) and tuple(new_state.flatten()) not in predecessor:

                #adding to queue
                my_queue.enqueue(new_state)
                
                #adding to predecessor
                predecessor[tuple(new_state.flatten())]=tuple(current_state.flatten())

    return None

if __name__=="__main__":

    path,(node_info,node_visited) = bfs(initial_state,goal_state)
    
    #Writing nodePath.txt
    #Change the path as per your machine
    with open(r"D:\Study\Masters\Robot Planning\Project1\Submission\nodePath.txt", "w") as file:
        for tup in path:
            line = " ".join(map(str, tup))
            file.write(line + "\n")
    
    #Writing Node.txt
    #Change the path as per your machine
    with open(r"D:\Study\Masters\Robot Planning\Project1\Submission\Nodes.txt", "w") as file:
        for node in node_visited:
            line = " ".join(map(str, node))
            file.write(line + "\n")
    
    #Writing NodeInfo.txt
    #Change the path as per your machine
    with open(r"D:\Study\Masters\Robot Planning\Project1\Submission\NodesInfo.txt", "w") as file:
        file.write("Node_index\tParent_Node_index\tNode\n")
        for entry in node_info:
            node_index, parent_node_index, nodes = entry
            nodes_str = " ".join(map(str, nodes))
            line = f"{node_index}\t{parent_node_index}\t{nodes_str}\n"
            file.write(line)
    