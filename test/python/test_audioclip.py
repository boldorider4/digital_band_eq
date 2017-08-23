from digital_eq_prototype import *
from scipy.io.wavfile import read as ReadWav
from scipy.io.wavfile import write as WriteWav

# Global parameters

F0 = [3000, 15000]
Q  = [1.4,  1.4]

def main():

  # read input audio
  FS, audio_input = ReadWav('../audio_sample_rock.wav')
  # extract one channel
  audio_input = audio_input[:,0]
  # pre-allocate output
  audio_output = np.zeros_like(audio_input)

  eq = digitalEq(FS)
  eq.init_eq(F0, Q)

  print("FS {}".format(FS))
  print("F0 {}".format(F0))
  print("Q {}".format(Q))
  print("type of audio input is {}".format(type(audio_input[0])))
  print("audio is {} samples long".format(len(audio_input)))
  print("rms audio input {}".format(np.sqrt(np.mean(audio_input.astype(np.float)**2))))
  idx = 0

  for sample in audio_input:
    audio_output[idx] = eq.process_sample(sample)
#    audio_output[idx] = eq.process_sample(sample) / 4
    idx += 1

  WriteWav('audioclip_' + str(F0) + 'filtered.wav', FS, audio_output)

if __name__ == '__main__':
  main()
  exit(0)
