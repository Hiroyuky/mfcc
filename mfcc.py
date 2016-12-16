#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Author: Hiroyuky
"""
Extract MFCC for sound.

"""
from __future__ import division
from __future__ import print_function

import wave
import numpy as np
import scipy.signal
import functions as fn

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
  wavdata, fs = input_wav(filename)
  #center = len(wav) / 2
  #cuttime = 0.04
  #wavdata = wav[int(center - (cuttime/2*fs)) : int(center + (cuttime/2*fs))]
  # ステレオファイルをモノラル化します
  x = fn.monauralize(wavdata)

  nfft = 16 * 25 # フレーム: 16kHz - 25ms  [400 frame]
  OVERLAP = nfft - (16 * 10) # 10ms
  frame_length = len(wavdata)
  time_song = float(frame_length) / fs
  time_unit = 1 / float(fs)
  print("Frame: ", nfft)
  print("OverLap: ", OVERLAP)
  print("length: ", frame_length)
  print("波長の長さ(s): ", time_song)
  print("1サンプルの長さ(s): ", time_unit)

  start = (nfft / 2) * time_unit	# 中心時間 12.5[ms]
  stop = time_song			# 終わり
  step = (nfft - OVERLAP) * time_unit	# ずらした時間
  time_ruler = np.arange(start, stop, step)


  print("start: ", start)

  # PreEmphasis firter
  p = 0.97
  signal = preEmphasis(wavdata, p)
  #signal = preEmphasis(filename, p)
  #fs = 16000

  # Hamming Window function
  #hammingWindow = np.hamming(len(signal))
  #signal = signal * hammingWindow
  window = np.hamming(nfft)
  #spec = np.zeros([len(time_ruler), 1 + (nfft / 2)])
  pos = 0

  ceps = []
  for mfcc_index in range(len(time_ruler)):
    frame = x[pos:pos+nfft]
    if len(frame) == nfft:
      windowed = window * frame		# 窓掛け
      # FFT
      #nfft = 2048
      spec = np.abs(np.fft.fft(windowed, nfft))[:int(nfft/2)]
      fscale = np.fft.fftfreq(nfft, d=(1.0/fs))[:int(nfft/2)]

      numChannels = 20
      df = fs / nfft
  
      filterbank, fcenters = melFilterBank(fs, nfft, numChannels)

      mspec = np.array(np.log10(np.dot(spec, filterbank.T)))

      ceps.append(DCT(mspec ,nceps))
      pos += (nfft -OVERLAP)
  
  print("cost frame: ", mfcc_index)
  ceps = np.array(ceps)

  return ceps




