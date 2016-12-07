#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Author: Hiroyuky

from __future__ import print_function
from __future__ import division

import mfcc
import sys
import numpy as np
import csv
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == '__main__':
  
  args = sys.argv

  # Listi
  getwav = []
  with open(args[1], "r") as f:
    wavedata = f.readlines()
    getwav = [line.replace('\n','') for line in wavedata] # Remove to '\n'

  # MFCC
  ceps = []
  if len(args) == 2:
    ceps = np.array([mfcc.mfcc(line) for line in getwav])
  elif len(args) == 3:
    ceps = np.array([mfcc.mfcc(line, int(args[2])) for line in getwav])
  else:
    print("ERROR: Invalid argument.")
    quit()


  # output CSV
  csvOutputFileName = args[1].rsplit(".", 1)	# abc/def.wav => abc/def, wav
  with open((csvOutputFileName[0]+".csv"), "w") as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(ceps)

  
  """ Plot MFCC
  CSV に出力するようにしたので機能排除
  """
  """
  filename = args[1].rsplit(".", 1)	# abc/def.wav => abc/def, wav
  filename = filename[0].rsplit("/", 1)	# abc/def => abc, def
  plt.plot(ceps, "o-")
  plt.xlim(-1, (len(ceps)+1))	# -1, cepsの最大値+1
  plt.savefig(filename[1]+".png")
  """





