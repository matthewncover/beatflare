import pyaudio, wave

class AudioOutput:
    def __init__(self, device_index: int = 1):
        self.rate = 44100
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.rate,
                                  output=True,
                                  output_device_index=device_index)
        
    def play(self, signal: bytes):
        self.stream.write(signal)

    def play_file(self, filename):
        wf = wave.open(filename, 'rb')
        data = wf.readframes(2048)
        while data:
            self.stream.write(data)
            data = wf.readframes(2048)
        wf.close()

    def generate_test_tone(self, frequency=440, duration=1):
        import numpy as np
        t = np.linspace(0, duration, int(self.rate * duration))
        signal = (np.sin(2 * np.pi * frequency * t) * 0.5 * 32767).astype(np.int16)
        return signal.tobytes()

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()