import pyaudio, wave

class AudioBase:
    def __init__(self):
        self.rate = 44100
        self.chunk_size = 1024
        self.channels = 1

        self.format = pyaudio.paInt16
        self.device_index = 1
        self.p = pyaudio.PyAudio()


class AudioInput (AudioBase):
    def __init__(self):
        super().__init__()

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  input_device_index=self.device_index,
                                  frames_per_buffer=self.chunk_size)
        
    def record(self, duration=5):
        frames = []
        for _ in range(0, int(self.rate / self.chunk_size * duration)):
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            frames.append(data)
        return b''.join(frames)
    
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


class AudioOutput (AudioBase):
    def __init__(self):
        super().__init__()

        self.stream = self.p.open(format=self.format,
                                  channels=1,
                                  rate=self.rate,
                                  output=True,
                                  output_device_index=self.device_index)
        
    def play(self, signal: bytes):
        self.stream.write(signal)

    def generate_test_tone(self, frequency=440, duration=1):
        import numpy as np
        t = np.linspace(0, duration, int(self.rate * duration))
        signal = (np.sin(2 * np.pi * frequency * t) * 0.5 * 32767).astype(np.int16)
        return signal.tobytes()
    
    def get_signal_from_file(self, filename):
        wf = wave.open(filename, 'rb')
        return wf.readframes(wf.getnframes())

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


class AudioUtils:
    @staticmethod
    def save_signal(channels, sample_size, rate, signal, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(sample_size)
        wf.setframerate(rate)
        wf.writeframes(signal)
        wf.close()