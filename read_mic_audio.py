from concurrent.futures import thread
import datetime as dt, time
from multiprocessing.util import is_abstract_socket_namespace
import concurrent.futures
import multiprocessing
# import billiard as multiprocessing
# multiprocessing.forking_enable(False)
import threading

import numpy as np
import pyaudio


from ident_beats import find_beats
# import threading

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

    while input_stream.is_active():
        output_stream.write(
            input_stream.read(stream_clip_size)
        )

def print_something(input_stream, that_something, wait=1):
    
    while input_stream.is_active():
        time.sleep(wait)
        print(that_something)

def print_beats(stream_clip_size, start):

    input_stream = in_stream(stream_clip_size)

    stream_data_arr = np.zeros(stream_clip_size)

    while input_stream.is_active():
        stream_clip = input_stream.read(stream_clip_size)
        hop = np.frombuffer(stream_clip, dtype=np.float32)
        stream_data_arr = np.vstack([stream_data_arr, hop])

        if (int(time.time()) - int(start)) % 15 == 0:
            beat_midpoints, runtime_delta = find_beats(stream_data_arr)
            stream_data_arr = np.zeros(stream_clip_size)

            print(beat_midpoints)

if __name__ == "__main__":
    stream_clip_size = 440

    start = time.time()

    p1 = multiprocessing.Process(target=play_music, args=[stream_clip_size])
    p2 = multiprocessing.Process(target=print_beats, args=[stream_clip_size, start])

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # input_stream = in_stream(stream_clip_size)
    # output_stream = out_stream()

    # p1 = threading.Thread(target=play_music, args=[input_stream, output_stream, stream_clip_size])
    # p2 = threading.Thread(target=print_something, args=[input_stream, "beat", 1])
    # p2 = threading.Thread(target=print_beats, args=[input_stream, stream_clip_size, start])

    # p1.start()
    # p2.start()

    # p1.join()
    # p2.join()

        # play_music(input_stream, output_stream, stream_clip_size)
        # print_something(input_stream, "beat", wait=1)

    # stream_data_arr = np.zeros(stream_clip_size)

    # while input_stream.is_active():
    #     stream_clip = input_stream.read(stream_clip_size)

    #     output_stream.write(stream_clip)

    ## TODO
    #
    # Use beat midpoints to print something using i / 50 = 1 sec
        # need way to not use time.sleep() because it stops the writing process
            # while dt.datetime.now() < some_time:
    # how to write the chunks together for an uninterrupted output
    # only use time.time(), get rid of i so on same basis
    # start = time.time()
    # with concurrent.futures.ProcessPoolExecutor() as executor:

        # continuously play music
        # periodically calculate beats and timely print beats

        # pass

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

    # i = 0
    # # start = dt.datetime.now()
    # start = time.time()
    # while input_stream.is_active():
    #     stream_clip = input_stream.read(stream_clip_size)

    #     hop = np.frombuffer(stream_clip, dtype=np.float32)
    #     stream_data_arr = np.vstack([stream_data_arr, hop])
    #     if (i % 1e3 == 0) & (i > 0):
    #         beat_midpoints, runtime_delta = find_beats(stream_data_arr)
    #         # print(beat_midpoints)
    #         for beat in beat_midpoints:
    #             projected_beat_time = start + beat/(stream_clip_size*50) + runtime_delta/beat_midpoints.shape[0] + i/50 + 3
    #             # print(start, beat/(stream_clip_size*50), runtime_delta)
    #             print(round(time.time() - projected_beat_time, 2))
    #             print(i)
    #             # while dt.datetime.now() < (start + i/50)
    #             while time.time() < projected_beat_time:
    #                 # output_stream.write(stream_clip)
    #                 _ = 0
    #             print("beat")

    #         stream_data_arr = np.zeros(stream_clip_size)


    #     output_stream.write(stream_clip)
    #     i += 1

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