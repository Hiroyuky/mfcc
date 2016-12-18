#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Author: Hiroyuky
from __future__ import print_function

import mfcc
import sys
import numpy as np
from scipy import ceil, complex64, float64, hamming, zeros
import csv
import wave
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('dark')

def read_wav_data(wavname):
  '''read wave data'''
  wf = wave.open(wavname, 'r')
  fs = wf.getframerate()
  x = wf.readframes(wf.getnframes())
  X = np.frombuffer(x, dtype='int16')
  x_ = np.arange(0, len(X)) / float(fs)

  return X, float(fs), x_
  
if __name__ == '__main__':
  
  '''args[1]: read to text file of wave list.'''
  args = sys.argv

  # WAVE list
  getwav = []
  with open(args[1], "r") as f:
    wavedata = f.readlines()
    getwav = [line.replace('\n','') for line in wavedata] # Remove to '\n'
  print('Get wave data list: ', getwav)
  
  """ Read wave datas """
  wavdata, fs, time_shift = read_wav_data(getwav[0])

  """ MFCC """
  #mfcc.mfcc => wavdata, fs, time_song, ceps
  wavdata, fs, time_song, ceps = mfcc.mfcc(wavdata, fs)
  
  """ Delta MFCC """
  delta_mfcc = np.empty((0, len(ceps)), int)
  for line in range(len(ceps.T)):
    delta_mfcc = np.append(delta_mfcc, [mfcc.delta(ceps.T[line])], axis=0)


  ''' Calculate the average '''
  # MFCC
  #print(len(ceps.T))	# 12
  #print(ceps[0, :])	# 12 value
  ave_mfcc = []
  #for i in range(len(ceps.T)):
  #  ave_mfcc.append(sum(ceps.T[i, :])/len(ceps))
  print(ceps.T.mean(axis=1))
  ave_mfcc.append(ceps.T.mean(axis=1))

  """ Plot """
  # WAVE
  plt.subplot(3,1,1)
  plt.plot(time_shift, wavdata)
  plt.ylabel('Amplitude')
  
  # MFCC
  plt.subplot(3,1,2)
  plt.imshow(ceps.T, extent=[0, time_song, 1, len(ceps.T)], 
	     aspect='auto', interpolation='nearest')
  plt.ylabel('MFCC')
  plt.jet()
  #plt.colorbar()

  # Delta MFCC
  plt.subplot(3,1,3)
  plt.imshow(delta_mfcc, extent=[0, time_song, 1, len(delta_mfcc)],
	     aspect='auto', interpolation='nearest')
  plt.ylabel('Delta MFCC')
  plt.jet()
  #plt.colorbar()

  plt.xlabel('time [sec]')
  plt.savefig('image.png')
  #plt.show()

  ''' CSVに書き込み'''
  # MFCC
  print('Output MFCC')
  f = open('csv/MFCC.csv','wb')
  dataWriter = csv.writer(f)
  dataWriter.writerows(ceps)
  f.close()
  
  # Delta MFCC
  print('Output Delta MFCC')
  f = open('csv/DeltaMFCC.csv','wb')
  dataWriter2 = csv.writer(f)
  dataWriter2.writerows(delta_mfcc)
  f.close()
  

  ''' CSVにAverageを書き込み '''
  print('Output Averages')

  # Average MFCC
  f = open('csv/aveMFCC.csv', 'wb')
  dataWriter3 = csv.writer(f)
  dataWriter3.writerows(ave_mfcc)
  f.close()

  # Average Delta MFCC
  f = open('csv/aveDeltaMFCC.csv', 'wb')
  f.close()



