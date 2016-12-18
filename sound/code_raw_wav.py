#! /usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess	# using Linux command

def r2w(N, rawName, wavName):
	for var in range(0, N):
		line1 = 'sox -e signed-integer -c 1 -b 16 -r 16000 '
		line2 = rawName
		line3 = str('{0:03d}'.format(var)) + '.raw'
		line4 = ' '
		line5 = wavName
		line6 = str('{0:03d}'.format(var)) + '.wav'
		line7 = line1 + line2 + line3 + line4 + line5 + line6
		print(line7)
		subprocess.call(line7)

if __name__ == "__main__":
	data_num = 100	# max data
	raw_filename = 'raw_data/raw_particl2/'
	wav_filename = 'wav_data/wav_particl2/'
	
	r2w(data_num, raw_filename, wav_filename)


