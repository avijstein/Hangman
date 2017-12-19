import os, sys
from time import sleep
import numpy as np
import pandas as pd


os.chdir('/Users/ajstein/Desktop/Real Life/Coding Projects/Hangman/')
all_words = pd.read_table('./master_dict.txt', sep='\r', header=None, names=['words'])
all_words['words'] = all_words['words'].str.lower().drop_duplicates()

print('---- Initializing Game ----')
target_word = 'dreamy'
print("Your word is ", target_word.upper(), ", but the computer doesn't know that.", sep='')
guessed_letters, wrongs = [], 0
current_word = list('_'*len(target_word))
print('Current word: ', ''.join(current_word))


all_words = all_words.loc[all_words['words'].str.len() == len(target_word)]

possible_words = all_words['words'].apply(lambda x: pd.Series(list(x))) # CHOKE POINT


def play_game(df):
    global guessed_letters, current_word, target_word, wrongs
    if (''.join(current_word) == ''.join(target_word)):
        print('Success! Only took ', len(guessed_letters), ' turns with ', wrongs, ' wrong guesses!', sep = '')
        print('Final word: ', (''.join(current_word)).upper())
        sys.exit()

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

    positions = [x for x, char in enumerate(target_word) if char == guess]
    if positions == []:
        wrongs += 1
        if wrongs > 7:
            print('Failed! You guessed wrong 7 times.')
            print(''.join(current_word))
            sys.exit()
        # print('Wrong guess. So far: ', wrongs)
        sleep(.3)
        return(df)

    for i in positions:
        current_word[i] = guess
        df = df.loc[df[i] == guess]
    print('Current word: ', ''.join(current_word))
    sleep(.5)
    return(df)



while(True):
    possible_words = play_game(possible_words)











# bottom
