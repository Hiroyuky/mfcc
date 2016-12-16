#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Author: Hiroyuky

from __future__ import print_function
#from __future__ import division

import mfcc
import sys
import numpy as np
from scipy import ceil, complex64, float64, hamming, zeros
import csv
import wave
import matplotlib.pyplot as plt
import seaborn as sns
import deltaMFCC


if __name__ == '__main__':
  
  args = sys.argv

  # Listi
  getwav = []
  with open(args[1], "r") as f:
    wavedata = f.readlines()
    getwav = [line.replace('\n','') for line in wavedata] # Remove to '\n'


  ceps = mfcc.mfcc(getwav[0])
  
  print(ceps)
  
  # CSVに書き込み
  f = open('writeDataMFCC.csv','ab')
  dataWriter = csv.writer(f)
  dataWriter.writerows(ceps)
  f.close()
  
  #print(ceps[0, 0])
  
  print(len(ceps))
  # calculate delta from MFCC
  #d_mfcc = np.array([])
  d_mfcc = np.empty((0,106), int)
  print(d_mfcc.shape)
  ceps = ceps.T

  print(len(ceps))
  #print(ceps[11])
  #for i in ceps:

  testline = np.array(deltaMFCC.delta(ceps[0]))
  
  print("ceps delta: ", testline)
  
  for line in range(len(ceps)):
    d_mfcc = np.append(d_mfcc, [deltaMFCC.delta(ceps[line])], axis=0)

  print(d_mfcc)

  f = open('writeDeltaMFCC.csv','ab')
  dataWriter2 = csv.writer(f)
  dataWriter2.writerows(d_mfcc)
  f.close()
  




