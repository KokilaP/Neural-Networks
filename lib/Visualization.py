import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np

class Visualization:
    '''
    Function 2: Visualize neural network
    Inputs graph G 
    Returns cluster coefficient & characteristic path length
        & plot of connections between neurons (color-coded)
    For more info: see collective dynamics paper
    
    Description:
    From network model, determines cluster coefficient and characteristic path length for each
        node. For each network, will take average of those values, respectively and yield 
        single integer value.
    From network model, will output plot of connections, color-coded for excitatory and
        inhibitory.
    
    Returns:
        cc_avg: Cluster coefficient averaged over all nodes
        ex_in_plot: Plot of colored excitatory/inhibitory connections
        cpl_avg: Number of edges at shortest path over all nodes 
        
    Parameters:
        G: NetworkX Graph from Function 1
    '''
    def __init__(self):
        #plt.clf() # Clears any previous figures
        plt.close() # Clears any figure windows

    def cluster_coeff(self,G):        
        cc = nx.clustering(G) # calculate clustering co-eff according to different rules eg. no of triangles going through node
        # outputs co-eff for all or specified nodes in dict form
        cc_y=[]
        for idx in cc:
            cc_y=np.append(cc_y,cc[idx]) # access and append dict values (co-effs in this case) to array
        
        cc_avg = np.ndarray.mean(cc_y, dtype=np.float64)
        return cc_avg
    
    def ex_in_connec(self,G,connect_W,new_coord):
        plt.figure()
        red_patch = mpatches.Patch(color='red', label='Excitatory')
        blue_patch = mpatches.Patch(color='blue', label='Inhibitory')
        plt.legend(handles=[red_patch,blue_patch])
        plt.suptitle('Structural Connections', fontsize=14, fontweight='bold')

        edges = G.edges() # list of tuple pairs
        nodes = G.nodes() # array of nodes

        custom_color={}
        for idx in range(len(connect_W)):
            if connect_W[idx] < 0:
                inhib_edge = new_coord[idx]
                G.add_edge(*inhib_edge)     # adds an inhibitory edge connection to graph if it's not already there
                custom_color[inhib_edge]='b'
            else:
                excit_edge = new_coord[idx]
                G.add_edge(*excit_edge)
                custom_color[excit_edge]='r'
        if 0:
            for idx,idy in enumerate(edges):
                x1,y1 = edges[idx]
                if connect_W < 0:
                    inhib_edge = (x1,y1)
                    G.add_edge(x1,y1)
                    custom_color[x1,y1]='b' # Stores color of edges in dict
                else:
                    excit_edge = (x1,y1)
                    G.add_edge(x1,y1)
                    custom_color[x1,y1]='r'
        
        ex_in_plot=nx.draw_networkx(G,node_color='w',
                         with_labels=True,
                         node_list=nodes,
                         #node_size=50,
                         node_size=200,
                         edge_list=custom_color.keys(),
                         edge_color=custom_color.values(),
                         label='Blue=Inhibitory, Red=Excitatory')
        #plt.savefig("Structural Connections.png")
        
    def char_path_len(self,G):
        cpl = nx.all_pairs_shortest_path_length(G) # shortest path lengths. Gen. returns tuple with source and target dict
        my_array = []
        my_key = []
        cpl_count = []
        for idx in cpl: # looping through each source node and looking at no of targets and length to target nodes
            myarray = cpl[idx[1]] # cpl is a generator object. idx is a tuple (source, target dict). Should be idx[1].
            min_val = min(ii for ii in myarray if ii > 0) # Find min length
            for key,length in myarray.iteritems():
                if length == min_val:
                    my_key = np.append(my_key,key) # array of target nodes with min length for specific source node
            my_count = len(my_key) # Find number of edges of that length
            cpl_count = np.append(cpl_count,my_count)
            my_key = []
            cpl_avg = np.mean(cpl_count) # Find average of those edges
        return cpl_avg