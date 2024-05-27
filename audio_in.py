import pyaudio, wave

class AudioInput:
    def __init__(self, device_index:int=1):
        self.rate = 44100
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  input_device_index=device_index,
                                  frames_per_buffer=self.chunk_size)
        
    def record(self, duration=5):
        frames = []
        for _ in range(0, int(self.rate / self.chunk_size * duration)):
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            frames.append(data)
        return b''.join(frames)
    
    def save(self, frames, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(frames)
        wf.close()