import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from brian2 import *

class BrianVisualization:
    '''
    Function 4: Visualization of Brian 
    Define LIF neural population in Brian
    Call to save spike times
    Call to plot voltage monitor
    Call to plot raster plot
    Call to plot histogram
    
    Description:
    Will plot the voltage monitor, raster plot, and histogram of neural network
    
    Returns:
        G: NeuronGroup
        spike_times: Spike times for neuron 0
        all_spikes: Spike times for all neurons
        
    
    Parameters:
        statemon: StateMonitor
        spikemon: SpikeMonitor
        run_time: Simulation run time
    
    '''
    def __init__(self):
        plt.clf() # Clears any previous figures
        plt.close() # Clears any figure windows
        
        start_scope()
    
    def network_indv(self,rows,cols,connect_W,N,PInput,gname,sname,neuron_diffeqns,integ_method,v_c,g_EE,g_II):
        # rows and cols 1-D arrays of source and target neurons that are connected as defined in graph from networkx
        # connect_W: 1-D array of strength of connections corresponding to source and target neuron pairs 
        '''
        For full synch: G1.v = fixed
                        PI = off
        '''
        eqs = neuron_diffeqns # Defined in the input parameter block 
                
        G1 = NeuronGroup(N, eqs, threshold='v>v_th', reset='v=v_r', refractory=10*ms, method=integ_method,name=gname) #integ_method defined in input parameter block
        G1.v = v_c # initial voltage value defined in input block
        G1.ge = g_EE
        G1.gi = g_II
    
        '''
        Injection current is constant but with slight perturbations from PoissonInput, if that function is active
        To get rid of highly synchronized, G1.v='rand()' and turn on P1
        '''
        
        # PoissonInput injection current -- changes each neuron's firing rate
        # Each neuron has different input current depending on Poisson distribution
        PI_num = 0.8*N 
        #subG1 = G1[int(PI_num):] # Top 20% of total neurons stimulated
        subG1 = G1[:] # All neurons stimulated via Poisson 
        '''
        PoissonInput(target,target_var,N,rate,weight)
            target: which neurons to send PoissonInput
            target_var: which variable that is being changed from input
            N: number of inputs (more input = higher firing rate)
            rate: rate of input (100Hz = 10ms per spike)
            weight: amount added to voltage
        '''
        P1 = PoissonInput(subG1, 'v', 5, 100*Hz, weight=PInput) # PoissonInput off if PInput = 0
        
        '''
        Synapses(source,target,model,on_pre,name)
            source: neuron group for pre-synaptic neurons
            target: neuron group for post-synaptic neurons
            model: synapse equations, in this case only a weight variable, w is used
            on_pre: the pre-synaptic event. Weight, w is added to voltage from pre-synaptic neuron and this becomes the 
                    post-synaptic neuron voltage
            name: to uniquely identify the synapse group
        '''
        S1 = Synapses(G1, G1, model ='''w : volt''', on_pre='''v_post += w
                                                               ge+=we*(w>0*volt)
                                                               gi+=wi*(w<0*volt)''',name=sname)
        S1.connect(i=rows, j=cols) # Adjacency matrix from Adj.weighted, this uses network structure defined on networkx
        S1.w = connect_W/float(100) # Weighted matrix defined from networkx graph 
               
        return G1,S1,P1

    def network_coupling(self,N,excit,inhib,p_couple,w_couple,G1,G2,sname,connect_type):
        '''
        Should see how coupling between different subpopulation has global effects (raster plot)
            - Could see difference if neurons have same firing rate (non-PoissonInput) vs. different firing rate (all-PoissonInput)
            - May only want to record (Statemon, Spikemon) from this last coupling (G2) to save resources
                - See Monitoring Synaptic Variables from http://brian2.readthedocs.io/en/2.0.1/user/synapses.html
            = Can introduce multiple output synapses (multisynaptic_index from http://brian2.readthedocs.io/en/2.0.1/user/synapses.html)
                - Or more simply "S.connect(i=numpy.arange(10), j=1)"
        '''
        S3 = Synapses(G1,G2, model ='''w : volt''', on_pre='''v_post += w
                                                              ge+=we*(w>0*volt)
                                                              gi+=wi*(w<0*volt)''',name=sname)#, delay=5*ms) # G1 drives G2
        
        ### Manually defining coupling ###
        p_couple2 = p_couple*excit
        i_couple2 = p_couple*inhib
        
        # If want 1:1 for only first p_couple% neurons (excitatory --> excitatory)
        if connect_type == 'ee':
            c_rows = list(arange(0,p_couple2,dtype=int)) # Source neurons
            c_cols = list(arange(0,p_couple2,dtype=int)) # Target neurons
        elif connect_type == 'ii':
            c_rows = list(arange(N-i_couple2,N,dtype=int))
            c_cols = list(arange(N-i_couple2,N,dtype=int))
        elif connect_type == 'ie':
            c_rows = list(arange(N-i_couple2,N,dtype=int))
            c_cols = list(arange(0,p_couple2,dtype=int))
        elif connect_type == 'ei':
            c_rows = list(arange(0,p_couple2,dtype=int))
            c_cols = list(arange(N-i_couple2,N,dtype=int))

        S3.connect(i=c_rows, j=c_cols) # Manually defined coupling
        S3.w = w_couple
        ###################################
        
        ##### Probabilistic coupling #####
        #S3.connect(p=0.05) # Probabilistic connection - Chance that G2 will connect with and spike from G1
        #S3.w = 0.02
        #S3.connect(p=p_couple)
        ###################################
                
        # Coupling matrix
        coup_mat = [[0 for x in range(N)] for y in range(N)]

        for ii in range(len(c_rows)):
            for jj in range(len(c_cols)):
                coup_mat[ii][ii] = 1      # Matrix has 1s for connections and 0s for none

        #statemon1 = StateMonitor(G1, 'v', record=0,name='statemon1_'+ G1.name) # Records just neuron 0 to save resources
        statemon1 = StateMonitor(G1,variables=('v','ge','gi'), record=0, dt=10*us,name='statemon_cG1')
        spikemon1 = SpikeMonitor(G1, variables='v',name='spikemon_cG1')
        statemon2 = StateMonitor(G2, variables=('v','ge','gi'), record=0, dt=10*us,name='statemon_cG2') # Records neuron 0
        spikemon2 = SpikeMonitor(G2, variables='v',name='spikemon_cG2')
        # statemon_syn = StateMonitor(S3, variables=['v','ge','gi'], record=0, name='statemon_syn') # Records synaptic index 0
        
        return statemon1,spikemon1,statemon2,spikemon2,c_rows,c_cols,coup_mat,S3
        
    def spike_time(self,spikemon):
        all_values = spikemon.all_values()
        spike_times = all_values['t'][0] # Spike times for just neuron 0
        all_spikes = spikemon.t/ms # Spike times for all neurons
        
        return spike_times,all_spikes
        
    def voltage_monitor(self,statemon):
        plot(statemon.t/ms, statemon.v[0])
        #plot(statemon.t/ms, statemon.v[1])  # Plots second neuron      
        ylabel('Voltage (V)')
        xlabel('Time (ms)')
        
    def raster_plot(self,spikemon,spikemon_other):
        #ion()
        plot(spikemon.t/ms, spikemon.i, '.r')
        plot(spikemon_other.t/ms, spikemon_other.i, '.k') # Plots overlay of each network
        #plt.xlim([0,105])
        #plt.xticks(np.arange(0, 1200, step=20))
        xlabel('Time (ms)')
        ylabel('Neuron index');
        #plt.show(block=True)
        
    def spike_hist(self,run_time,all_spikes):
        my_bins = arange(0,run_time+2,2)
        plt.hist(all_spikes, bins=my_bins)
        plt.xlim([0,105])
        plt.yticks(np.arange(0, 30, step=2))
        plt.margins()
        xlabel('Time (ms)')
        ylabel('Total number of spikes')