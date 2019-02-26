import networkx as nx
from brian2 import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class AdjacencyMatrix:  
    '''
    Function 1: Weighted adjacency matrix
    Call to initiate adjacency matrix
    Call to choose which neural network topology with given parameters
    
    Description:
    Given parameters, constructs network with adjacency matrix and applies random weights.
    
    Returns:
        Graph: NetworkX Graph
        A: Adjacency matrix. Sparse matrix
        rows: Presynaptic neurons
        cols: Postsynaptic neurons
        connect_W: Weights for each E/I connection (in order of rows,cols)
    
    Parameters:
        n: nodes
        m: edges
        k: neighbor connections
        p: probability 
        d: degrees
    '''
    def __init__(self,n): 
        plt.clf() # Clears any previous figures
        plt.close() # Clears any figure windows
        
    def random(self,n,p): 
        # Interchangeable based on UI for different types of topography
        #G = nx.dense_gnm_random_graph(n,m) # Uses NetX to generate random topography, need to add input param m
        Graph = nx.gnp_random_graph(n,p)
        #nx.draw(G, with_labels=True) # Draws connectivity figure
        #plt.savefig("Random.png") # Saves connectivity figure as Random.png

        # Extracts ADJACENCY MATRIX from topography and rearranges to manageable array of (n*n) elements
        A = nx.adjacency_matrix(Graph) # Assigns A as adjacency matrix (which nodes are connected)
        return A, Graph 
    
    def small_world(self,n,k,p): 
        Graph = nx.newman_watts_strogatz_graph(n,k,p) 
        #nx.draw(G, with_labels=True)
        #plt.savefig("Small-world.png")
        A = nx.adjacency_matrix(Graph)
        return A, Graph
    
    def unidir_coord(self,rows, cols):
        # function to remove duplicate connections like (0,3) and (3,0) so that all connections are uni- and not bi-directional
        coord = zip(rows,cols) # To get an array of coordinate pair tuples, to define node pairs or edges 
        new_pairs = set(tuple(sorted(l)) for l in coord) # set removes duplicate tuples that are now ordered pairs
                                                            # set(array of tuples)
        g = np.array(list(new_pairs)) #array of 1 by 2 neuron pair vectors that are connected to each other
                                      # In each 1 by 2 vector: column 0 is source neuron and column 1 is target neuron
        new_rows = g[:,0] #1-D array of all source neurons i
        new_cols = g[:,1] #1-D array of all target neurons j
        new_coord = zip(new_rows,new_cols) # list of tuples, source and target ordered pairs with no duplicates
        return new_coord, new_rows, new_cols
    
    def adj_synapse_type(self,A,excit):
        ### Define connections as inhibitory or excitatory in the adjacency matrix
        A_mat = A.todense() # Converts adjacency matrix from 'scipy.sparse.csr.csr_matrix' to numpy matrix                              
        rows, cols = np.nonzero(A_mat) # Two arrays of index positions for connections
        [new_coord, new_rows, new_cols] = self.unidir_coord(rows,cols) # Removes duplicate connections
        connect = len(new_rows) # number of connections or 1s in adjacency matrix

        for i in range(connect):
            x = new_rows[i]
            y = new_cols [i]
            if x>(excit-1) or y>(excit-1):   # Checking if either source or target neuron belongs to upper 20% of n 
                A_mat[x,y] = A_mat[x,y]*-1   # Inhibitory neuron defined, weight is made negative
                                             # not necessary to repeat for symmetric part of the matrix as it won't be used

        # Constructing array of unweighted connections
        connect_A = [] # Initializaing empty connections array
        for i in range(connect):
            x = new_rows[i]
            y = new_cols [i]
            connect_A.append(A_mat[x,y])
        connect_A = np.array(connect_A) # Converting data type list to numpy array
        return connect_A,new_coord,new_rows,new_cols