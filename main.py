import sounddevice as sd
import numpy as np
import threading
import queue
from led_patterns import Lights

def audio_callback(indata, frames, time, status):
    audio_data = indata.copy()  # Make a copy of the audio data
    q.put(audio_data)  # Add audio_data to the queue

def led_control_thread(q):
    lights = Lights()
    lights._set("orange", [1, 2, 3, 4, 5])

    while not stop_threads.is_set():
        lights = Lights()
        lights._set("black", [1, 2, 3, 4, 5])

        try:
            audio_data = q.get(timeout=1)  # Get audio_data from the queue
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
    # Audio config
    sampling_rate = 44100
    channels = 2
    
    # Initialize queue and stop flag
    q = queue.Queue()
    stop_threads = threading.Event()

    # Start the LED control thread
    led_thread = threading.Thread(target=led_control_thread, args=(q,))
    led_thread.start()

    try:
        # Create an input stream with the desired configuration
        with sd.InputStream(samplerate=sampling_rate, channels=channels, callback=audio_callback):
            print("Recording... Press Ctrl+C to stop.")
            while True:
                sd.sleep(1000)  # Wait for audio data to be processed by the callback
    except KeyboardInterrupt:
        stop_threads.set()  # Set the stop flag to stop the LED control thread
        led_thread.join()  # Wait for the LED control thread to finish
