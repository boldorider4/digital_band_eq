from digitalEq import *
from scipy.io.wavfile import read as ReadWav
from scipy.io.wavfile import write as WriteWav

# Global parameters
F0_vec = [[1000],
          [3000, 15000],
          [100, 10000, 17000],
          [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]]
Q_vec  = [[1.4],
          [1,  2],
          [.8,  1.9, .3],
          [1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3]]
G_vec  = [[.8],
          [.5, .9],
          [.6, 1, .9],
          [.95, .9, .7, .55, .5, .7, .8, .9, .95, .97]]
FILENAME = ['audio_sample.wav', 'audio_sample_rock.wav', 'audio_sample_beguine.wav']

def main():

  global F0, Q, G, FILENAME

  for input_filename in FILENAME:
    # read input audio
    FS, audio_input = ReadWav('../audio_samples/'+input_filename)
    # extract channels
    audio_input_ch0, audio_input_ch1 = audio_input[:,0], audio_input[:,1]
    # pre-allocate output
    audio_output = np.zeros_like(audio_input)

    if len(F0_vec) != len(Q_vec) or len(F0_vec) != len(G_vec):
      print('invalid global parameter sizes')
      return -1

    for F0, Q, G in zip(F0_vec, Q_vec, G_vec):
      eq_ch0 = digitalEq(FS)
      eq_ch1 = digitalEq(FS)
      err = eq_ch0.init_eq(F0, Q, G)
      if err:
        return -1
      err = eq_ch1.init_eq(F0, Q, G)
      if err:
        return -1

      print()
      print("filename {}".format(input_filename))
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
      if len(F0) > 3:
        output_filename += '_f'+str(F0[0])+'_'+str(F0[-1])
      else:
        for f0,Q in zip(F0,Q):
          output_filename += '_f'+str(f0)
      output_filename += '_ref.wav'
      WriteWav(output_filename, FS, audio_output)


if __name__ == '__main__':
  main()
  exit(0)
