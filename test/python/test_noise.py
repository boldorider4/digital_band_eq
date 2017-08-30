from math import pi as Pi
from math import cos as Cos
from math import tan as Tan
from digitalEq import *
from scipy.io.wavfile import write as WriteWav

# Global parameters

FS = 44100
F0 = [1000]
Q = [1.4]
G = [1]

def main():

  global FS, F0, Q, G

  # read input audio
  audio_input = np.random.randint(-2**14, 2**14, size=96000, dtype='int16')
  # pre-allocate output
  audio_output = np.zeros_like(audio_input)

  eq = digitalEq(FS, 1)
  err = eq.init_eq(F0, Q, G)
  if err:
    return -1

  print("FS {}".format(FS))
  print("F0 {}".format(F0))
  print("Q {}".format(Q))
  print("type of audio input is {}".format(type(audio_input[0])))
  print("rms audio input {}".format(np.sqrt(np.mean(audio_input.astype(np.float)**2))))
  idx = 0

  for sample in audio_input:
    audio_output[idx] = eq.process_sample(sample)
    idx += 1

  WriteWav('noise.wav', FS, audio_input)
  WriteWav('noise_filtered.wav', FS, audio_output)

if __name__ == '__main__':
  main()
  exit(0)
