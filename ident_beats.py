import numpy as np, pandas as pd
from sklearn.cluster import k_means

import datetime as dt, time

def find_beats(stream_data_arr, return_df = False):
    """current time master fn
    """

    start = time.time()
    stream_data_arr = stream_data_arr[1:]

    df = (
        pd.Series(
            stream_data_arr.ravel()
            )
            .reset_index()
            .rename(columns={
                "index": "timestep",
                0: "db"
            })
        )

    df["abs_db"] = abs(df.db)

    df_abs_rolled = (
        df.abs_db
        .rolling(20).mean()
        .dropna()
        .reset_index()
        .rename(columns={"index": "timestep"})
    )

    # beat_midpoints = loc_beat_midpoints(df)
    beat_midpoints = loc_beat_midpoints(
        df_abs_rolled, 
        percentile=.993, 
        jump_size_cutoff=1000
        )

    # runtime_delta = (dt.datetime.now() - start).seconds
    runtime_delta = time.time() - start

    if return_df:
        return beat_midpoints, df

    else:
        return beat_midpoints, runtime_delta


def loc_beat_midpoints(df, percentile=.999, jump_size_cutoff=5e3):
    """identify timestep midpoints of beats

    timestamp = seconds*sampling_rate

    Parameters:
        df (DataFrame): columns \in {timestep, db, abs_db}
        percentile (float): abs(amplitude) percentile cutoff
        jump_size_cutoff (int): minimum timestep distance between beats
    """

    assert percentile < 1, "percentile must be < 1"

    db_cutoff = df.abs_db.quantile(percentile)
    beat_inds = pd.Series(df[df.abs_db > db_cutoff].index)

    timestamp_jump_sizes = abs(np.array(beat_inds - beat_inds.shift(1).iloc[1:], dtype="int32"))

    beat_cluster_centers = k_means(
        np.array(beat_inds).reshape(-1, 1),
        n_clusters = np.where(timestamp_jump_sizes > jump_size_cutoff)[0].shape[0] + 1
    )

    beat_midpoints = (
        pd.Series(beat_cluster_centers[0].flatten())
        .sort_values()
        .astype(int)
        .values
    )

    return beat_midpoints

if __name__ == "__main__":

    start = dt.datetime.now()

    arr_kendrick = np.load("./kendrick_clip.npy")

    beat_midpoints = find_beats(arr_kendrick)

    print(f'done: {dt.datetime.now() - start}')