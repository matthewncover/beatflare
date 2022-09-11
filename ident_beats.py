import numpy as np, pandas as pd
from sklearn.cluster import k_means

import datetime as dt

def play_beats(beat_midpoints, i):



    pass

def find_beats(stream_data_arr):
    """current time master fn
    """

    start = dt.datetime.now()

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

    beat_midpoints = loc_beat_midpoints(df)

    runtime_delta = dt.datetime.now() - start

    return beat_midpoints, runtime_delta


def loc_beat_midpoints(df, jump_size_cutoff=1e4):
    """identify timestep midpoints of beats

    Parameters:
        df (DataFrame): columns \in {timestep, db, abs_db}
        jump_size_cutoff (int): minimum timestep distance between beats
    """

    db_cutoff = df.abs_db.quantile(.999)
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