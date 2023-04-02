from helpers import files

dir = './split-segments'

print(files.get_wav_segments(dir))

print(files.get_references('sources'))

print(files.get_references('sources/Anders Tegnell.wav'))

print(files.get_references('sources/speakers.json'))