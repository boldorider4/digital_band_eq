from digitalEq import *
from scipy.io.wavfile import read as ReadWav
from scipy.io.wavfile import write as WriteWav

# Global parameters
F0 = [3000, 15000]
Q  = [1.4,  1.4]
G = [1, 1]

def main():

  global F0, Q, G

  # read input audio
  input_filename = 'audio_sample_rock'
  FS, audio_input = ReadWav('../audio_samples/'+input_filename+'.wav')
  # pre-allocate output
  audio_output = np.zeros_like(audio_input)

  eq = digitalEq(FS, audio_input.shape[1])
  err = eq.init_eq(F0, Q, G)
  if err:
    return -1

  print("FS {}".format(FS))
  print("F0 {}".format(F0))
  print("Q {}".format(Q))
  print("number of channels {}".format(audio_input.shape[1]))
  print("type of audio input is {}".format(type(audio_input[0])))
  print("audio is {} samples long".format(len(audio_input)))
  print("rms audio input {}".format(np.sqrt(np.mean(audio_input.astype(np.float)**2))))
  idx = 0

  for sample in audio_input:
    audio_output[idx] = eq.process_sample(sample)
    idx += 1

  output_filename = input_filename+'_filt'
  for f0,Q in zip(F0,Q):
    output_filename += '_f'+str(f0)+'Q'+str(Q)
  output_filename += '.wav'
  WriteWav(output_filename, FS, audio_output)

if __name__ == '__main__':
  main()
  exit(0)
