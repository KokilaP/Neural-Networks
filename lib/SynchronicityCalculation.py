import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

class SynchronicityCalculation:
    '''
    To calculate different metrics of synchronicity
    
    For more information:
        See Synch Metrics bookmarks folder
        http://wwwold.fi.isc.cnr.it/users/thomas.kreuz/sourcecode.html
        https://arxiv.org/pdf/1603.03293.pdf
        http://mariomulansky.github.io/PySpike/pyspike.html#pyspike.SpikeTrain.SpikeTrain
        http://mariomulansky.github.io/PySpike/index.html
        http://www.scholarpedia.org/article/Measures_of_spike_train_synchrony#ISI-distance
    '''
    def __init__(self):
        plt.clf() # Clears any previous figures
        plt.close() # Clears any figure windows

    def Initialize(self,spikemon1,spikemon2,tstart,tend):
        try:
            st1 = spk.SpikeTrain(spikemon1.t/ms, edges=[tstart,tend])
            st2 = spk.SpikeTrain(spikemon2.t/ms, edges=[tstart,tend])
            
        except AttributeError:
        # In case parameters passed to function are a dictionary of spike times in 'ms' and not spike monitors 
        # The AttributeError 'dict' object has no attribute 't' results and is caught here
            st1 = spk.SpikeTrain(spikemon1/ms, edges=[tstart,tend])
            st2 = spk.SpikeTrain(spikemon2/ms, edges=[tstart,tend])

        return st1,st2

    def SPIKEsynch(self,st1,st2):
        '''
        SPIKE-synchronization measures similarity where 0 means absence of synchrony and bounded to 1
        indicating absolute synchrony
        '''
        spike_sync = spk.spike_sync([st1,st2])
        #print spike_sync

        # Plotting SPIKE-synchronicity
        spike_profile = spk.spike_sync_profile([st1,st2])
        x,y = spike_profile.get_plottable_data()
        plot(x,y,'-k')
        ylabel('SPIKE-sync')

    def ISIdistance(self,st1,st2):
        '''
        ISI-distance quantifies dissimilarity based on differences of interspike intervals from two
        different spike trains. Becomes 0 for identical spike trains and approaches -1 and 1 when
        first or second spike train is faster than the other, respectively.
        '''
        isi_prof = spk.isi_profile(st1,st2)
        isi_dist = isi_prof.avrg()
        #print isi_dist # Outputs nan if spike train has same time values

        # Plotting ISI profile
        x,y = isi_prof.get_plottable_data()
        plot(x,y,'-k')
        ylabel('ISI')

    def SPIKEdistance(self,st1,st2):
        '''
        SPIKE-distance quantifies dissimilarity based on exact spike timings. In other words,
        dissimilarity in terms of deviations from exact coincidences of spikes
        Becomes 0 for identical spike trains, and bounded by 1 for highly dissimilar
        '''
        spike_dist = spk.spike_distance([st1,st2])
        #print spike_dist

        spike_profile = spk.spike_profile([st1,st2])
        x,y = spike_profile.get_plottable_data()
        plot(x,y,'-k')
        xlabel('Time (ms)')
        ylabel('SPIKE-dist')

    def CrossCorrelation(self,spikemon1,spikemon2):
        # Normalize spike times
        try:
            norm1 = spikemon1.t / np.linalg.norm(spikemon1.t)
            norm2 = spikemon2.t / np.linalg.norm(spikemon2.t)
        
        except AttributeError:
            norm1 = spikemon1 / np.linalg.norm(spikemon1)
            norm2 = spikemon2 / np.linalg.norm(spikemon2)
            
        test1 = norm1
        test2 = norm2
        y = np.correlate(test1,test2,"full") 
        z = np.correlate(test1,test1,"full") 

        # Plotting correlation
        x_valy = range(len(y))
        x_valz = range(len(z))
        plot(x_valy-np.argmax(z/ms),y,'b')
        plot(x_valz-np.argmax(z/ms),z,'g')
        blue_patch = mpatches.Patch(color='blue', label='Test Correlation')
        green_patch = mpatches.Patch(color='green', label='Autocorrelation')
        suptitle('Comparing network 2 to network 1', fontsize=14, fontweight='bold')
        plt.legend(handles=[blue_patch,green_patch])
        
    def sync_parameter(self,mean,sigma,N):
        '''
        Takes in the mean value of a parameter and generates another value from a Gaussian distribution within the range
        specified by the standard deviation(sigma). The number of values generated corresponds to N. 
        '''
        interval = np.random.normal(mean, sigma,N)
        return interval