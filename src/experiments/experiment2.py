# -*- coding: utf-8 -*-
import os, sys

cmd_folder = os.path.dirname(os.path.abspath('../src/'))
if cmd_folder not in sys.path:
     sys.path.insert(0, cmd_folder)

import festival


engine = festival.Festival()

text1       = 'Sally sells seashells by the seashore.'
text2       = 'The quick brown fox jumped over the lazy dog.'
dest        = './text.wav'
#wave_type   = 'riff' # default

engine.wave(text=text1 + text2, source = 'experiment1.py', dest = dest)
#engine.wave(text2)
