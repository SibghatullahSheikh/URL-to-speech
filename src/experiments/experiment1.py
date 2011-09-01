#!/bin/python

import pyttsx

engine = pyttsx.init()

voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('rate',rate-70)


for voice in voices:
  engine.setProperty('voice',voice.id)
  engine.say('Sally sells seashells by the seashore.')
  engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()