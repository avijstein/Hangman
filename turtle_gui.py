import os, sys, random
from time import sleep
import turtle as t
import hangman as hm

os.chdir('/Users/ajstein/Desktop/Real Life/Coding Projects/Hangman/')

# this function brings in everything we need to run the variables from hangman in this space.
hm.load_game('ant')


print(hm.all_words.head())


about_time = hm.all_words.iloc[0,0]

sys.exit()

t.color('black')
t.write(about_time, font = 100)
t.done()


# bottom
