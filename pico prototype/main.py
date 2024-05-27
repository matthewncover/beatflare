import sounddevice as sd
import numpy as np
import threading
import queue
from led_patterns import Lights

def audio_callback(indata, frames, time, status):
    audio_data = indata.copy()  
    q.put(audio_data) 

def led_control_thread(q):
    lights = Lights()
    lights._set("orange", [1, 2, 3, 4, 5])

    while not stop_threads.is_set():
        lights = Lights()
        lights._set("black", [1, 2, 3, 4, 5])

        try:
            audio_data = q.get(timeout=1)
            print(np.max(np.abs(audio_data)))
            print(f'******{np.mean(np.abs(audio_data))}')
            if np.max(np.abs(audio_data)) > .06:
                lights.fade()
                lights.pico.close()
                lights = Lights()
                lights._set("orange", [1, 2, 3, 4, 5])

            if abs(np.mean(np.abs(audio_data)) - .007) < .001:
                lights.stagger(t=.2)
                lights.pico.close()
                lights = Lights()
                lights._set("seagreen", [1, 2, 3, 4, 5])

        except queue.Empty:
            pass


if __name__ == "__main__":
    sampling_rate = 44100
    channels = 2
    
    q = queue.Queue()
    stop_threads = threading.Event()

    led_thread = threading.Thread(target=led_control_thread, args=(q,))
    led_thread.start()

    try:
        with sd.InputStream(samplerate=sampling_rate, channels=channels, callback=audio_callback):
            print("Recording... Press Ctrl+C to stop.")
            while True:
                sd.sleep(1000)

    except KeyboardInterrupt:
        stop_threads.set()
        led_thread.join()
