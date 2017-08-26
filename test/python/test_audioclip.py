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
  # extract channels
  audio_input_ch0, audio_input_ch1 = audio_input[:,0], audio_input[:,1]
  # pre-allocate output
  audio_output = np.zeros_like(audio_input)

  eq_ch0 = digitalEq(FS)
  eq_ch1 = digitalEq(FS)
  err = eq_ch0.init_eq(F0, Q, G)
  if err:
    return -1
  err = eq_ch1.init_eq(F0, Q, G)
  if err:
    return -1

  print("FS {}".format(FS))
  print("F0 {}".format(F0))
  print("Q {}".format(Q))
  print("number of channels {}".format(audio_input[0].size))
  print("type of audio input is {}".format(type(audio_input[0])))
  print("audio is {} samples long".format(len(audio_input)))
  print("rms audio input {}".format(np.sqrt(np.mean(audio_input.astype(np.float)**2))))
  idx = 0

  for sample_ch0, sample_ch1 in zip(audio_input_ch0, audio_input_ch1):
    audio_output[idx, 0] = eq_ch0.process_sample(sample_ch0)
    audio_output[idx, 1] = eq_ch1.process_sample(sample_ch1)
    idx += 1

  output_filename = input_filename+'_filt'
  for f0,Q in zip(F0,Q):
    output_filename += '_f'+str(f0)+'Q'+str(Q)
  output_filename += '.wav'
  WriteWav(output_filename, FS, audio_output)

if __name__ == '__main__':
  main()
  exit(0)
