import pandas as pd
import numpy as np

class OscillatorsPythonAddons:
    """
    Extra Python utilities for Oscillators objects.
    """
    
    _cached_results_df = None
    _results_dirty = True

    def inter_event_times(self):
        """
        Convert a list-of-lists into a pandas DataFrame.
        """

        data = self.inter_event_times_list

        # Build DataFrame
        df = pd.DataFrame(data)
        df = df.T
        # Column names: 1..N
        df.columns = list(range(1, df.shape[1] + 1))

        return df
    

    def mark_results_dirty(self):
        self._results_dirty = True

    
    def simulation_results(self, force=False):
        if force or self._results_dirty or self._cached_results_df is None:
            results = self.simulation_results_dict   # uses your Python getter
            df = self._build_results_dataframe(results)
            self._cached_results_df = df
            self._results_dirty = False
            return df

        return self._cached_results_df

    def _build_results_dataframe(self, results):
        """
        Convert:
            { sim_i : [[osc1_ts...], [osc2_ts...], ...] }
        into a DataFrame with:
            rows = time steps
            columns = "simulation_i_oscillator_j"
        """

        # First, determine number of time steps from the first simulation
        common_length = len(results[1][0])
        for i in range(1, len(results)):
            for j in range(0, len(results[i])):
                if len(results[i][j]) < common_length:
                    common_length = len(results[i][j])

        first_sim = next(iter(results))
        osc_matrices = results[first_sim]

        # Each oscillator has a time series of equal length
        T = common_length   # number of time steps

        data = {}
        for sim_i, osc_list in results.items():
            for osc_j, series in enumerate(osc_list, start=1):
                data[f"simulation_{sim_i}_oscillator_{osc_j}"] = series[0:T]

        df = pd.DataFrame.from_dict(data)
        
        # Ensure rows correspond to time steps exactly
        df.index = range(T)

        return df

    
    def one_dimensional_coupling_search(self, indices, bounds, step=1):
        mu    = {}    
        sigma = {}
        coupling_matrix = self.coupling
        i = bounds[0]

        while i < bounds[1] + step:
            coupling_matrix[indices[0]][indices[1]] = float(i) 
            self.coupling = coupling_matrix
            self.kuramoto_simulations(100, "interEventTimes")
            df = self.simulation_results()
            model_ie_times = df.values.flatten()
            mean = np.mean(model_ie_times)
            std_dev = np.std(model_ie_times)
            mu[i] = mean
            sigma[i] = std_dev
            self.reset()
            i += step

        return mu, sigma


