import pandas as pd

class OscillatorsPythonAddons:
    """
    Extra Python utilities for Oscillators objects.
    """

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
    
    #def simulation_results(self):
    #    """
    #    Convert self.results (a dict[int -> 2D list]) into a single wide DataFrame.

    #    Column names become:
    #        simulation_i_oscillator_j
    #    """

    #    results = self.simulation_results_dict   # uses your Python getter

    #    # Determine max number of time points and oscillators
    #    max_rows = max(len(mat) for mat in results.values())
    #    max_cols = max(len(row) for mat in results.values() for row in mat)

    #    # Build a dataframe dict of columns
    #    df_dict = {}

    #    for sim, mat in results.items():
    #        # Ensure rectangular (pad short rows if needed)
    #        padded = []
    #        for row in mat:
    #            if len(row) < max_cols:
    #                row = row + [None] * (max_cols - len(row))
    #            padded.append(row)

    #        if len(padded) < max_rows:
    #            blank = [None] * max_cols
    #            padded += [blank] * (max_rows - len(padded))

    #        # Now padded is max_rows × max_cols
    #        # Convert to DataFrame to help transpose
    #        tmp = pd.DataFrame(padded).T

    #        # tmp is oscillators × timepoints
    #        for osc_index, col in tmp.iterrows():
    #            colname = f"simulation_{sim}_oscillator_{osc_index+1}"
    #            df_dict[colname] = col.values

    #    return pd.DataFrame(df_dict)
    _cached_results_df = None
    _results_dirty = True

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
        first_sim = next(iter(results))
        osc_matrices = results[first_sim]

        # Each oscillator has a time series of equal length
        T = len(osc_matrices[0])   # number of time steps

        df = pd.DataFrame()

        for sim_i, osc_list in results.items():
            for osc_j, series in enumerate(osc_list, start=1):
                colname = f"simulation_{sim_i}_oscillator_{osc_j}"
                df[colname] = series

        # Ensure rows correspond to time steps exactly
        df.index = range(T)

        return df
