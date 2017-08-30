from digitalEq import *
from scipy.io.wavfile import read as ReadWav
from scipy.io.wavfile import write as WriteWav

# Global parameters
F0_vec = [[1000],
         [100, 10000, 17000],
         [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]]
Q_vec  = [[1.4],
         [.8,  1.9, .3],
         [1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3]]
G_vec  = [[.8],
         [.6, 1, .9],
         [.95, .9, .7, .55, .5, .7, .8, .9, .95, .97]]
FILENAME = ['audio_sample.wav', 'audio_sample_rock.wav', 'audio_sample_beguine.wav']

def main():

  global F0, Q, G, FILENAME

  for input_filename in FILENAME:
    # read input audio
    FS, audio_input = ReadWav('../audio_samples/'+input_filename)
    # pre-allocate output
    audio_output = np.zeros_like(audio_input)

    if len(F0_vec) != len(Q_vec) or len(F0_vec) != len(G_vec):
      print('invalid size of global array of parameter')
      return -1

    for F0, Q, G in zip(F0_vec, Q_vec, G_vec):
      if len(F0) != len(Q) or len(F0) != len(G):
        print('invalid parameter sizes')
        return -1

      eq = digitalEq(FS, 2)
      err = eq.init_eq(F0, Q, G)
      if err:
        return -1

      print()
      print("filename {}".format(input_filename))
      print("FS {}".format(FS))
      print("F0 {}".format(F0))
      print("Q {}".format(Q))
      print("number of channels {}".format(audio_input[0].size))
      print("type of audio input is {}".format(type(audio_input[0,0])))
      print("audio is {} samples long".format(len(audio_input)))
      print("rms audio input {}".format(np.sqrt(np.mean(audio_input.astype(np.float)**2))))
      idx = 0

      for sample in audio_input:
        audio_output[idx] = eq.process_sample(sample)
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
