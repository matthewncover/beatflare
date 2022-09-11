import datetime as dt, time
import numpy as np

import pyaudio

from ident_beats import find_beats
# import threading

# https://github.com/mjhydri/BeatNet/blob/main/src/BeatNet/BeatNet.py

if __name__ == "__main__":
    stream_clip_size = 440

    input_stream = pyaudio.PyAudio().open(
        format=pyaudio.paFloat32,
        channels = 1,
        rate = 22050,
        input = True,
        frames_per_buffer=stream_clip_size
    )

    output_stream = pyaudio.PyAudio().open(
        format=pyaudio.paFloat32,
        channels = 1,
        rate = 22050,
        output=True
    )

    stream_data_arr = np.zeros(stream_clip_size)

    i = 0
    while input_stream.is_active():
        stream_clip = input_stream.read(stream_clip_size)

        hop = np.frombuffer(stream_clip, dtype=np.float32)
        stream_data_arr = np.vstack([stream_data_arr, hop])
        if (i % 200 == 0) & (i > 0):
            beat_midpoints, runtime_delta = find_beats(stream_data_arr)
            print(beat_midpoints)

        output_stream.write(stream_clip)
        i += 1

    # stream2.write

    # stream.start_stream()

    # # wait for stream to finish (5)
    # while stream.is_active():
    #     print(np.random.choice(["ye", "yeet"]))
    #     time.sleep(0.1)

    # # stop stream (6)
    # stream.stop_stream()
    # stream.close()
    
    # stream_clip = np.zeros(stream_clip_size)

    # start = dt.datetime.now()
    # beta_s2 = 0
    # betas = np.array([])

    # i = 0
    # while stream.is_active():

    #     hop = np.frombuffer(stream.read(stream_clip_size), dtype=np.float32)
        
    #     stream_clip = np.vstack([stream_clip, hop])

        # if i % 15 == 0:
        #     avg_hop = round(hop.mean()*100, 1)

        #     print(avg_hop, round(hop.std()*10, 1), i)

        # if (i % 1e2 == 0) & (i > 0):
        #     # np.save("./kendrick_clip.npy", stream_clip)

        #     beta = (dt.datetime.now() - start)
        #     beta_s = beta.seconds + beta.microseconds/1e6
        #     print(beta_s)
        #     betas = np.append(betas, beta_s - beta_s2)
        #     print(beta_s-beta_s2)
        #     print(betas.mean())
        #     beta_s2 = beta_s
            
        # i += 1


## capture audio from a couple songs
    # bluetooth speaker + rap mic

## look for beat patterns that you can repeat
## delay what comes out of the speakers by X seconds (?)
    # to have enough time to learn pattern shifts