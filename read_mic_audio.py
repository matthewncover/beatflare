import os, time, numpy as np

import pyaudio
# import threading

# https://github.com/mjhydri/BeatNet/blob/main/src/BeatNet/BeatNet.py

if __name__ == "__main__":
    stream = pyaudio.PyAudio().open(
        format=pyaudio.paFloat32,
        channels = 1,
        rate = 22050,
        input = True,
        frames_per_buffer=441
    )

    i = 0
    while stream.is_active():

        hop = np.frombuffer(stream.read(441), dtype=np.float32)

        if i % 10 == 0:
            print(hop.mean(), hop.std())
        i += 1


## capture audio from a couple songs
    # bluetooth speaker + rap mic

## look for beat patterns that you can repeat
## delay what comes out of the speakers by X seconds (?)
    # to have enough time to learn pattern shifts