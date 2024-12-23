import queue, threading
import sounddevice as sd, numpy as np

class BeatFlare:
    def __init__(self):
        self.sampling_rate = 44100
        self.channels = 1
        self.delay_seconds = 10

        self.buffer_size = self.sampling_rate * self.delay_seconds

        self.q = queue.Queue()
        self.stop_threads = threading.Event()
        self.lock = threading.Lock()

    def run(self):
        self.out_stream = sd.OutputStream(samplerate=self.sampling_rate, channels=self.channels)
        self.out_stream.start()

        self.in_stream = sd.InputStream(samplerate=self.sampling_rate, channels=self.channels, callback=self._input_thread)
        self.in_stream.start()

        out_thread = threading.Thread(target=self._output_thread, args=(self.buffer_size, self.channels))
        out_thread.start()

        try:
            # with sd.InputStream(samplerate=self.sampling_rate, channels=self.channels, callback=self._input_thread):
                # print("Recording...")
            while True:
                sd.sleep(1000)

        except KeyboardInterrupt:
            self.stop_threads.set()
            out_thread.join()
            self.out_stream.stop()
            self.out_stream.close()

    def _input_thread(self, indata, frames, time, status):
        audio_data = indata.copy()
        self.q.put(audio_data)

    def _output_thread(self, buffer_size, channels):
        buffer = np.zeros((buffer_size, channels), dtype=np.float32)

        while not self.stop_threads.is_set():
            try:
                audio_data = self.q.get(timeout=1)
                buffer = np.concatenate((buffer, audio_data))

                if buffer.shape[0] > buffer_size:
                    signal = buffer[:buffer_size]
                    buffer = buffer[buffer_size:]
                    self.out_stream.write(signal)
                    
            except queue.Empty:
                pass