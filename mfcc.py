#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Author: Hiroyuky
"""
Extract MFCC for sound.

"""
from __future__ import division
from __future__ import print_function

#import sys
import wave
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.signal


def input_wav(filename):
  """ wav データ　読み込み """
  wf = wave.open(filename, 'r')
  fs = wf.getframerate()
  x = wf.readframes(wf.getnframes())
  x = np.frombuffer(x, dtype='int16') / 32768.0
  wf.close()
  
  return x, float(fs)

def preEmphasis(signal, p):
  """FIR filter """
  return scipy.signal.lfilter([1.0, -p], 1, signal)

def hz2mel(f):
  return 1127.01048 * np.log(f/700.0+1.0)

def mel2hz(m):
  return 700.0 * (np.exp(m/1127.01048) - 1.0)


def melFilterBank(fs, nfft, numChannels):
  """ メルフィルタバンク """
  fmax = fs / 2
  melmax = hz2mel(fmax)
  nmax = nfft / 2
  df = fs / nfft
  dmel = melmax / (numChannels + 1)
  melcenters = np.arange(1, numChannels + 1) * dmel
  fcenters = mel2hz(melcenters)
  indexcenter = np.round(fcenters / df)
  indexstart = np.hstack(([0], indexcenter[0:numChannels - 1]))
  indexstop = np.hstack((indexcenter[1:numChannels], [int(nmax)]))

  filterbank = np.zeros((numChannels, int(nmax)), dtype=np.float)
  for c in np.arange(0, numChannels):
    increment = 1.0 / (indexcenter[c] - indexstart[c])
    for i in np.arange(indexstart[c], indexcenter[c]):
      i = int(i)
      filterbank[c, i] = (i - indexstart[c]) * increment
      decrement = 1.0 / (indexstop[c] - indexcenter[c])
    for i in np.arange(indexcenter[c], indexstop[c]):
      i = int(i)
      filterbank[c, i] = 1.0 - ((i - indexcenter[c]) * decrement)
      
  return filterbank, fcenters

def DCT(mspec, nceps):
  """ 離散コサイン変換 """
  ceps = scipy.fftpack.realtransforms.dct(mspec, type=2, norm="ortho", axis=-1)

  return ceps[:nceps]

#if __name__ == '__main__':

def mfcc(filename, nceps=12):
  #args = sys.argv

  # read wave file
  #filename = args[1]
  wav, fs = input_wav(filename)
  center = len(wav) / 2
  cuttime = 0.04
  wavdata = wav[int(center - (cuttime/2*fs)) : int(center + (cuttime/2*fs))]
  
  # PreEmphasis firter
  p = 0.97
  signal = preEmphasis(wavdata, p)
  
  # Hamming Window function
  hammingWindow = np.hamming(len(signal))
  signal = signal * hammingWindow

  # FFT
  nfft = 2048
  spec = np.abs(np.fft.fft(signal, nfft))[:int(nfft/2)]
  fscale = np.fft.fftfreq(nfft, d=(1.0/fs))[:int(nfft/2)]

  numChannels = 20
  df = fs / nfft
  
  filterbank, fcenters = melFilterBank(fs, nfft, numChannels)

  mspec = np.array(np.log10(np.dot(spec, filterbank.T)))

  #nceps = 12
  ceps = DCT(mspec ,nceps)
  ceps = np.array(ceps)
  #print(ceps)
  
  plt.plot(ceps, "o-")
  plt.xlim(-1, 13)
  plt.savefig("MFCC12.png")
  #plt.show()
  
  return ceps




