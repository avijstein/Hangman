import os, sys, random
from time import sleep
import pandas as pd
import logging

# Change to user's cwd.
# os.chdir('/Users/ajstein/Desktop/Real Life/Coding Projects/Hangman/')

def clear_log(yes_or_no):
    """
    True or False. Gatekeeper whether to clear overwrite the log, or keep it for playback.
    """
    if yes_or_no:
        filehandler_dbg = logging.FileHandler('comm.log', mode='w')
        logging.basicConfig(filename='comm.log', level = logging.DEBUG, format = '')
    else:
        filehandler_dbg = logging.FileHandler('comm.log', mode='a')
        logging.basicConfig(filename='comm.log', level = logging.DEBUG, format = '')

def reading():
    """
    Read in data, make sure there are no duplicates because of capitalization.
    """
    all_words = pd.read_table('./master_dict.txt', sep='\r', header=None, names=['words'])
    all_words['words'] = all_words['words'].str.lower().drop_duplicates()
    return(all_words)

def friendly():
    """
    Initializing the game, asking for user input and checking if it's a real word.
    Tries the input again if it's not in the dictionary.
    """
    print('---- Initializing Game ----')
    target_word = input('What word would you like to choose? ')
    while True:
        if (target_word not in all_words['words'].values):
            print("That's not a valid word, please try another.")
            target_word = input('What word would you like to choose? ')
        else:
            break
    print("Your word is ", target_word.upper(), ", but the computer doesn't know that.", sep='')
    return(target_word)

def unfriendly(target_word):
    """
    Initializing the game, receives input rather than asking for it.
    Ends game if it's not in the dictionary.
    """
    global all_words
    if (target_word not in all_words['words'].values):
        sys.stdout = sys.__stdout__ # enable printing
        print("That's not a valid word, please try another and start again.")
        logging.info("That's not a valid word, please try another and start again.")
        sys.exit()
    print('---- Initializing Game ----')
    logging.info('---- Initializing Game ----')
    print("Your word is ", target_word.upper(), ", but the computer doesn't know that.", sep='')
    logging.info("Your word is " + str(target_word.upper()) + ", but the computer doesn't know that.")
    return(target_word)

def game_setup():
    """
    Sets up variables needed to run the game. Reduces the dictionary to words of the same length.
    Expands possible words into a dataframe containing one letter in each column. This is slow.
    """
    global guessed_letters, wrongs, all_words, target_word, current_word
    guessed_letters, wrongs = [], 0
    current_word = list('-'*len(target_word))
    print('Current word: ', ''.join(current_word))
    logging.info('Current word: ' + str(''.join(current_word)))
    all_words = all_words.loc[all_words['words'].str.len() == len(target_word)]
    possible_words = all_words['words'].apply(lambda x: pd.Series(list(x)))
    return(possible_words)

def play_game(df):
    """
    Takes in a dataframe of all possible words (expanded), finds the most frequent letter,
    guesses it, and then evaluates the possibilities from there.
    """
    global guessed_letters, current_word, target_word, wrongs, kill_switch
    logging.info('dict_size: ' + str(len(df)))
    # testing winning scenarios.
    if (''.join(current_word) == ''.join(target_word)):
        print('Success! Only took ', len(guessed_letters), ' turns with ', wrongs, ' wrong guesses!', sep = '')
        print('Final word: ', (''.join(current_word)).upper())
        logging.info('Success! Only took ' + str(len(guessed_letters)) + ' turns with ' + str(wrongs) + ' wrong guesses!')
        logging.info('Final word: ' + str((''.join(current_word)).upper()))
        # sys.exit()
        kill_switch = 1
        return

    # calculates frequency of each letter of all possible words.
    # finds the most likely (that hasn't been guessed already).
    # guesses it.
    new_df = df.apply(pd.value_counts).fillna(0)
    new_df['total'] = new_df.sum(axis = 1)
    new_df = new_df.sort_values(by = 'total', ascending = False)
    # print('all options: ', list(new_df['total'].index))
    options = new_df['total'].index
    options = options[~options.isin(guessed_letters)]
    # print('options: ', list(options)[0:5])
    logging.info('Best Options: ' + str(list(options)[0:5]))
    # print('guessed letters: ', guessed_letters)
    guess = options[0]
    guessed_letters.append(guess)
    logging.info('Guessed Letter: ' + str(guess))
    # print('my guess: ', guess)

    # checks the guess to see if it's correct (and where it is in the word).
    positions = [x for x, char in enumerate(target_word) if char == guess]
    # print('positions: ', positions)
    if positions == []:
        wrongs += 1
        logging.info('wrongs: ' + str(wrongs))
         # testing losing scenarios.
        if wrongs > 100:
            print('Failed! The computer guessed wrong 100 times.')
            print(''.join(current_word))
            logging.info('Failed! The computer guessed wrong 100 times.')
            logging.info(str(''.join(current_word)))
            sys.exit()
        # print('Wrong guess. So far: ', wrongs)
        sleep(.3)

        # If a letter isn't in the target word, remove all words containing that letter.
        for i in range(0,len(df.columns)):
            df = df.loc[df[i] != guess]
        return(df)


    # fills in any correct guesses.
    # narrows down possible words based on letters and positions.
    for i in positions:
        current_word[i] = guess
        df = df.loc[df[i] == guess]
    print('Current word: ', ''.join(current_word))
    logging.info('Current word: ' + str(''.join(current_word)))
    sleep(.5)
    return(df)

def gogogo():
    """
    Runs play_game until play_game decides it's done.
    """
    global possible_words, kill_switch
    kill_switch = 0
    n = 0
    while(kill_switch == 0):
        n += 1
        logging.info('turns: ' + str(n))
        possible_words = play_game(possible_words)


def load_game(my_word):
    """
    Loads all variables needed for the game when run from another script.
    """
    global guessed_letters, wrongs, all_words, target_word, current_word, possible_words
    all_words = reading()
    target_word = unfriendly(my_word)
    possible_words = game_setup()
    print('The game is fully loaded.')
    # logging.info('The game is fully loaded.')

def fullgameplay():
    """
    Runs full game when operated from the command line.
    """
    global guessed_letters, wrongs, all_words, target_word, current_word, possible_words
    all_words = reading()
    target_word = friendly()
    possible_words = game_setup()
    gogogo()


# sys.exit()


# If running this script from the command line, full game plays.
# Otherwise, it only loads functions.
if __name__ == '__main__':
    fullgameplay()



"""
---- Stats ----
n: 100
mean: 2.76
st dev: 2.43
success rate: 95%
conclusion: not bad at all
null check: doesn't affect it at all.
---------------
"""


# bottom
