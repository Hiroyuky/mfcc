#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Author: Hiroyuky

from __future__ import print_function
from __future__ import division

import mfcc
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == '__main__':
  
  args = sys.argv

  if len(args) == 2:
    ceps = mfcc.mfcc(args[1])
  
  elif len(args) == 3:
    ceps = mfcc.mfcc(args[1], int(args[2]))

  else:
    print("ERROR: argument error...")
    print("=============================================")
    print("$python " + args[0] + " [.wav]	(Output dimension is 12.)")
    print("$python " + args[0] + " [.wav] [MFCC dimension]")
    print("=============================================")
    quit()

  print(ceps)



  """ Plot MFCC 
  """
  filename = args[1].rsplit(".", 1)	# abc/def.wav => abc/def, wav
  filename = filename[0].rsplit("/", 1)	# abc/def => abc, def
  plt.plot(ceps, "o-")
  plt.xlim(-1, 12)
  plt.savefig(filename[1]+".png")






