import time
import multiprocessing

import numpy as np
import pyaudio

from ident_beats import find_beats

def in_stream(stream_clip_size):

    input_stream = pyaudio.PyAudio().open(
            format=pyaudio.paFloat32,
            channels = 1,
            rate = 22050,
            input = True,
            frames_per_buffer=stream_clip_size
        )

    return input_stream

def out_stream():

    output_stream = pyaudio.PyAudio().open(
        format=pyaudio.paFloat32,
        channels = 1,
        rate = 22050,
        output=True
    )

    return output_stream

def play_music(stream_clip_size):

    input_stream = in_stream(stream_clip_size)
    output_stream = out_stream()

    # time.sleep(3)
    while input_stream.is_active():
        output_stream.write(
            input_stream.read(stream_clip_size)
        )

def print_something(input_stream, that_something, wait=1):
    
    while input_stream.is_active():
        time.sleep(wait)
        print(that_something)

def print_beats(stream_clip_size, start):

    # beat_start = time.time()

    input_stream = in_stream(stream_clip_size)

    # stream_data_arr = np.zeros(stream_clip_size)

    while input_stream.is_active():
        stream_clip = input_stream.read(stream_clip_size)
        hop = np.frombuffer(stream_clip, dtype=np.float32)

        try:
            beat_midpoints, _ = find_beats(hop)
            beat_midpoints = beat_midpoints / 25000

            for i, beat in enumerate(beat_midpoints):
                # time.sleep(beat / 25000)
                if i > 0:
                    time.sleep(beat - beat_midpoints[i-1])
                else:
                    time.sleep(beat)
                print(np.random.choice(["beat", "beat!"]))

        except ValueError:
            continue

if __name__ == "__main__":
    stream_clip_size = int(440*400*(10/8)*(10/9.977658571428572)) # ~10 second clip

    start = time.time()

    p1 = multiprocessing.Process(target=play_music, args=[stream_clip_size])
    p2 = multiprocessing.Process(target=print_beats, args=[stream_clip_size, start])

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # while input_stream.is_active():
    #     stream_clip = input_stream.read(stream_clip_size)
    #     hop = np.frombuffer(stream_clip, dtype=np.float32)
    #     stream_data_arr = np.vstack([stream_data_arr, hop])

    #     if (int(time.time()) - int(start)) % 15 == 0:
    #         with concurrent.futures.ProcessPoolExecutor() as executor:
    #             print("ye")
    #             f1 = executor.submit(find_beats, stream_data_arr)
    #             f2 = executor.submit(play_music, output_stream, stream_clip)
    #             # f2.result()
    #             beat_midpoints, runtime_delta = f1.result()
    #             print(beat_midpoints)
    #             for beat in beat_midpoints:
    #                 projected_beat_time = start + beat/(stream_clip_size*50) + runtime_delta/beat_midpoints.shape[0]
    #                 if (time.time() - projected_beat_time) < 1:
    #                     print("beat")
    #     else:
    #         # f2 = executor.submit(play_music, output_stream, stream_clip)
    #         output_stream.write(stream_clip)
                # f2.result()

        # if (int(time.time()) - int(start)) % 5 == 0:
        #     beat_midpoints, runtime_delta = find_beats(stream_data_arr)

            

        # output_stream.write(stream_clip)

## capture audio from a couple songs
    # bluetooth speaker + rap mic

## look for beat patterns that you can repeat
## delay what comes out of the speakers by X seconds (?)
    # to have enough time to learn pattern shifts