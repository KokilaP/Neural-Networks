import numpy as np
from brian2 import *

class Spike_Stats:
    '''
    Description: Given spike times of each neuron, statistical parameters of ISI(Inter-Spike-Interval) can be calculated
                 like mean, variance, co-efficent of variation. Spike trains can also be compared to produce correlation
                 coefficients

    Parameters:
    '''

    def __init__(self):  # Not sure what to do here yet
        pass

    def ISI_stats(self, spikemon):
        neuron_spikes = spikemon.spike_trains()  # Dictionary with dict keys as neuron indices and
        # dict values as an array of spike times for that neuron
        firing_n = list(set(sort(spikemon.i)))  # To create a set or list of all unique neuron indices that have spiked
        # in order to calculate statistical parameters for each unique neuron

        ISI = {}  # Create an empty dictionary to contain dict keys as neuron indices and dict values as an array of ISIs
        ISI_mean = {}  # Dict for ISI mean of each neuron index
        ISI_var = {}  # Dict for ISI variance of each neuron index
        ISI_cv = {}  # Dict for ISI co-efficient of variation (CV) for each neuron index

        # Calculate variance and mean of each ISI (Inter-Spike-Interval)
        for i in firing_n:
            # Calculate ISI array by subtracting spike times of each neuron to get an array of spike intervals
            ISI[i] = np.diff(neuron_spikes[i])
            # Calculate mean of ISI
            ISI_mean[i] = np.mean(ISI[i])
            # Calculate variance of ISI
            ISI_var[i] = np.var(ISI[i])
            # Calculate co-efficient of variation(CV) of ISI
            ISI_cv[i] = np.sqrt(ISI_var[i]) / ISI_mean[i]
        return ISI, ISI_mean, ISI_var, ISI_cv

    def spk_extract(self, spikemon, tstart, tend):
        '''
        This function splits up spike monitors into desired time intervals and outputs:
        - a dictionary of neuron indices with their corresponding spike times within the specified interval
        - an array of spike times generated within the time interval for the entire network irrespective of neuron indices
        - an array of neuron indices corresponding to spike times
        '''
        SN_t = []
        SN_i = []
        SN_mon = {}

        for neuron in arange(n):
            temp_time = [j for j in spikemon.spike_trains()[neuron] if j > tstart * ms and j <= tend * ms]
            SN_t.extend(temp_time[:])
            SN_mon[neuron] = temp_time
        SN_t = sort(SN_t)

        # This for loop is to return an array of neuron indices corresponding to spikes times. Identical to any
        # spikemonitor.i output
        for t in SN_t:
            for index in SN_mon.keys():  # iterating through neuron indices' spike trains
                for spike in SN_mon[index]:  # iterating through values in spike trains
                    if t == spike / ms:
                        SN_i.append(index)
                        flag = 1
                        break
                    else:
                        flag = 0
            if flag == 1:
                break

        return SN_mon, SN_t, SN_i

    def spikebin_indv(self, sp_time, tstart, tend):
        '''
        This function takes in an array of spike times and counts the number of spikes occuring within a time interval
        defined by bin_size.
        It outputs an array of 0's and 1's to indicate whether or not a spike occured within an interval:
        - for each neuron (sp_ibinary)
        - bins: [t0,t0 + bin_size), [t1,t1 + bin_size).....
        '''

        sp_ibinary = {}
        t_interval = arange(tstart, tend, bin_size)  # bin_size is a global parameter defined in the input section
        t_size = len(t_interval) + 1

        for k in range(0, len(sp_time)):
            temp = np.array([0] * t_size)  # Converting to an array so that simulatenous assignment
            # to multiple indices is possible
            if sp_time[k] != []:
                bin_pos = ((sp_time[k] / (bin_size * ms)) - tstart / bin_size).astype(int)
                temp[bin_pos] = 1
                sp_ibinary[k] = temp

        return sp_ibinary

    def spikebin_total(self, sp_time, tstart, tend,bin_size):
        '''
        This function takes in an array of spike times and counts the number of spikes occuring within a time interval
        defined by bin_size.
        It outputs an array of the number of times a spike occured within an interval normalized by bin size:
        - for the overall network (sp_tbinary)
        - bins: [t0,t0 + bin_size), [t1,t1 + bin_size).....
        '''
        # Calculating binary spike train for the overall network
        t_interval = np.arange(tstart, tend, bin_size)  # bin_size is a global parameter defined in the input section
        t_size = len(t_interval) + 1

        sp_tbinary = np.array([0] * t_size)  # empty array to store the binary spike train
        sp_time_phase = [j for j in sp_time if
                         j > tstart * ms and j <= tend * ms]  # removes spike times above or below the
        # desired time interval
        for k in sp_time_phase:
            bin_pos = int((k / (bin_size * ms)) - tstart / bin_size)
            sp_tbinary[bin_pos] = 1 + sp_tbinary[bin_pos]

        sp_tbinary = sp_tbinary / bin_size

        return sp_tbinary

    def spike_cc(self, set1, set2):
        '''
        This function calculates Pearson product-moment correlation co-efficients of individual neuron spike trains
        '''
        # set1 = SN1_2_binary
        # set2 = SN2_2_binary
        final_CC = np.zeros((n, n))

        for i in set1:
            val1 = set1[i]
            for j in set2:
                val2 = set2[j]
                corr = np.corrcoef(val1, val2)
                final_CC[i][j] = corr[0, 1]
        return final_CC

    def spike_tcc(self, set1, set2):
        '''
        This function calculates Pearson product-moment correlation co-efficients by comparing
        spike trains of the total network (used for batch simulation)

        NOTE: Pearson product-moment correlation co-efficients is undefined for a constant time series like [1,1,1]
        because the variance/std is zero
        https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
        '''
        if all(set1 == [1] * len(set1)) and all(
                set2 == [1] * len(set2)):  # Check if all elements in both binary spike trains
            # are all 1s (if so Pearson method is undefined)
            corr = array([[1, 1], [1, 1]])  # set a value of 1 to show both spike trains are the same
        else:
            corr = np.corrcoef(set1, set2)

        return corr[0, 1]

    def batch_cc(self, SN1_2t, SN2_2t,phase1,phase2,bin_size):
        SN1_2_tbin = self.spikebin_total(SN1_2t, phase1, phase2,bin_size)
        SN2_2_tbin = self.spikebin_total(SN2_2t, phase1, phase2,bin_size)
        SN_2_tCC = self.spike_tcc(SN1_2_tbin, SN2_2_tbin)
        return SN_2_tCC

    # older func. Made newer one to cut down on unnecessary data
    def batch_cc_old(self, SN1, SN2):
        '''
        This function can be called each time a simulation is run to generate statistics of spike trains for each network
        and for each neuron within the networks

        SN0 is a spike monitor recording all spikes occuring in all neurons within a network
        SN0_all is a dictionary with spike times for corresponding neuron indices within the specified time period
        SN0_allt is an array of all spike times generated by the network within the time period
        SN0_ibin is a dictionary of binary spike trains corresponding to each neuron in the network
        SN0_tbin is the binary spike train of the network as a whole
        SN0_iCC is a matrix of correlation co-efficients generated by comparing all neurons in one network to another (N by N)
        SN0_tCC is a single number between -1 and 1 indicating how similar the overall binary spike train of one network is
        compared to the other
        '''
        # Extract spike times and corresponding neuron indices for each phase
        # Get a dictionary of neuron indices and corresponding spike times for each phase(1,2 or 3)
        # Get an array of overall network spike times for each phase, this will be used as input for PySpike functions

        # [SN0_all,SN0_allt] = stats.spk_extract(SN0,0,run_time)

        [SN1_1, SN1_1t, _] = self.spk_extract(SN1, 0, phase1)
        [SN2_1, SN2_1t, _] = self.spk_extract(SN2, 0, phase1)

        [SN1_2, SN1_2t, _] = self.spk_extract(SN1, phase1, phase2)
        [SN2_2, SN2_2t, _] = self.spk_extract(SN2, phase1, phase2)

        [SN1_3, SN1_3t, _] = self.spk_extract(SN1, phase2, phase3)
        [SN2_3, SN2_3t, _] = self.spk_extract(SN2, phase2, phase3)

        ##############################################################################
        # Create binary spike trains, put into stats class

        '''# Stand-alone network 1
        SN0_ibin = stats.spikebin_indv(SN0_all,0,run_time)
        SN0_tbin = stats.spikebin_total(SN0_allt,0,run_time)
        SN0_iCC = stats.spike_cc(SN0_ibin,SN0_ibin)
        SN0_tCC = stats.spike_tcc(SN0_tbin,SN0_tbin)'''

        # First phase of uncoupled networks
        #         SN1_1_ibin = self.spikebin_indv(SN1_1,0,phase1)
        #         SN2_1_ibin = self.spikebin_indv(SN2_1,0,phase1)
        #         SN1_1_tbin = self.spikebin_total(SN1_1t,0,phase1)
        #         SN2_1_tbin = self.spikebin_total(SN2_1t,0,phase1)
        #         SN_1_iCC = self.spike_cc(SN1_1_ibin,SN2_1_ibin)
        #         SN_1_tCC = self.spike_tcc(SN1_1_tbin,SN2_1_tbin)

        # Coupled networks
        SN1_2_ibin = self.spikebin_indv(SN1_2, phase1, phase2)
        SN2_2_ibin = self.spikebin_indv(SN2_2, phase1, phase2)
        SN1_2_tbin = self.spikebin_total(SN1_1t, phase1, phase2)
        SN2_2_tbin = self.spikebin_total(SN2_1t, phase1, phase2)
        SN_2_iCC = self.spike_cc(SN1_2_ibin, SN2_2_ibin)
        SN_2_tCC = self.spike_tcc(SN1_2_tbin, SN2_2_tbin)

        # Second phase of uncoupled networks
        #         SN1_3_ibin = self.spikebin_indv(SN1_3,phase2,phase3)
        #         SN2_3_ibin = self.spikebin_indv(SN2_3,phase2,phase3)
        #         SN1_3_tbin = self.spikebin_total(SN1_3t,phase2,phase3)
        #         SN2_3_tbin = self.spikebin_total(SN2_3t,phase2,phase3)
        #         SN_3_iCC = self.spike_cc(SN1_3_ibin,SN2_3_ibin)
        #         SN_3_tCC = self.spike_tcc(SN1_3_tbin,SN2_3_tbin)

        return SN_2_tCC