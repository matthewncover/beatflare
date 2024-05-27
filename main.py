from audio_out import AudioOutput

out = AudioOutput()
signal = out.generate_test_tone()
out.play(signal)