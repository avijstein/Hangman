import os, sys, random
from time import sleep
import numpy as np
import pandas as pd

# making sure everything is in the right directory.
# os.chdir('/Users/ajstein/Desktop/Real Life/Coding Projects/Hangman/')
all_words = pd.read_table('./master_dict.txt', sep='\r', header=None, names=['words']) # read in data.
all_words['words'] = all_words['words'].str.lower().drop_duplicates() # make sure there are no duplicates because of capitalization.

# initializing the game.
print('---- Initializing Game ----')
# target_word = 'butterfly'

# asking for input and making sure it's in the dictionary.
target_word = input('What word would you like to choose? ')
while True:
    if (target_word not in all_words['words'].values):
        print("That's not a valid word, please try another.")
        target_word = input('What word would you like to choose? ')
    else:
        break

print("Your word is ", target_word.upper(), ", but the computer doesn't know that.", sep='')
guessed_letters, wrongs = [], 0
current_word = list('_'*len(target_word))
print('Current word: ', ''.join(current_word))

# reduces all words down to only words of the same length as target.
# expands possible words into a dataframe containing one letter in each column.
# expanding is very slow.
all_words = all_words.loc[all_words['words'].str.len() == len(target_word)]
possible_words = all_words['words'].apply(lambda x: pd.Series(list(x)))

def play_game(df):
    """
    Takes in a dataframe of all possible words (expanded), finds the most frequent letter,
    guesses it, and then evaluates the possibilities from there.
    """
    global guessed_letters, current_word, target_word, wrongs

    # testing winning scenarios.
    if (''.join(current_word) == ''.join(target_word)):
        print('Success! Only took ', len(guessed_letters), ' turns with ', wrongs, ' wrong guesses!', sep = '')
        print('Final word: ', (''.join(current_word)).upper())
        sys.exit()

    # calculates frequency of each letter of all possible words.
    # finds the most likely (that hasn't been guessed already).
    # guesses it.
    new_df = df.apply(pd.value_counts).fillna(0)
    new_df['total'] = new_df.sum(axis = 1)
    new_df = new_df.sort_values(by = 'total', ascending = False)
    # print('all options: ', list(new_df['total'].index))
    options = new_df['total'].index
    options = options[~options.isin(guessed_letters)]
    # print('options: ', list(options))
    # print('guessed letters: ', guessed_letters)
    guess = options[0]
    guessed_letters.append(guess)
    # print('my guess: ', guess)

    # checks the guess to see if it's correct (and where it is in the word).
    positions = [x for x, char in enumerate(target_word) if char == guess]
    if positions == []:
        wrongs += 1
         # testing losing scenarios.
        if wrongs > 100:
            print('Failed! The computer guessed wrong 100 times.')
            print(''.join(current_word))
            sys.exit()
        # print('Wrong guess. So far: ', wrongs)
        sleep(.3)
        return(df)

    # fills in any correct guesses.
    # narrows down possible words based on letters and positions.
    for i in positions:
        current_word[i] = guess
        df = df.loc[df[i] == guess]
    print('Current word: ', ''.join(current_word))
    sleep(.5)
    return(df)

# runs the game until it wins or loses.
while(True):
    possible_words = play_game(possible_words)


"""
---- Stats ----
n: 100
mean: 2.76
st dev: 2.43
success rate: 95%
conclusion: not bad at all
---------------
"""


# bottom
