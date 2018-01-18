import os, sys, random, re, logging
from time import sleep
import turtle as t
import pandas as pd

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
    logging.info('---- Initializing Game ----')
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
        logging.info('Success! Only took ' + str(len(guessed_letters)) + ' turns with ' + str(wrongs) + ' wrong guesses!')
        logging.info('Final word: ' + str((''.join(current_word)).upper()))
        kill_switch = 1
        return

    # calculates frequency of each letter of all possible words.
    # finds the most likely (that hasn't been guessed already).
    # guesses it.
    new_df = df.apply(pd.value_counts).fillna(0)
    new_df['total'] = new_df.sum(axis = 1)
    new_df = new_df.sort_values(by = 'total', ascending = False)
    options = new_df['total'].index
    options = options[~options.isin(guessed_letters)]
    logging.info('Best Options: ' + str(list(options)[0:5]))
    guess = options[0]
    guessed_letters.append(guess)
    logging.info('Guessed Letter: ' + str(guess))

    # checks the guess to see if it's correct (and where it is in the word).
    positions = [x for x, char in enumerate(target_word) if char == guess]
    if positions == []:
        wrongs += 1
        logging.info('wrongs: ' + str(wrongs))
         # testing losing scenarios.
        if wrongs > 100:
            logging.info('Failed! The computer guessed wrong 100 times.')
            logging.info(str(''.join(current_word)))
            sys.exit()
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

def write_new_word(word, go):
    """
    Clears the comm.log and loads a game on the turtle_gui side.
    Doesn't generate gui, just preps it.
    """
    clear_log(True)
    load_game(word)
    gogogo()
    if go != 'go':
        sys.exit()

def draw_gallows():
    """
    A series of turtle commands to draw the gallows.
    """
    t.speed(10)
    t.penup()
    t.setpos((175, 275))
    t.pendown()
    t.setpos((175, 300))
    t.setpos((300, 300))
    t.setpos((300, 0))
    t.penup()
    t.setpos((350,0))
    t.pendown()
    t.setpos((200,0))
    t.penup()

def draw_body(piece):
    """
    A series of turtle commands to draw the body, to be executed one at a time.
    """
    def head():
        t.penup()
        t.setpos((175, 225))
        t.pendown()
        t.circle(25)
        t.penup()
        t.setpos((165, 255))
        t.dot()
        t.setpos((185, 255))
        t.dot()
    def body():
        t.penup()
        t.setpos((175, 225))
        t.pendown()
        t.setpos((175, 125))
    def arm1():
        t.penup()
        t.setpos((175,200))
        t.pendown()
        t.setpos((145, 220))
    def arm2():
        t.penup()
        t.setpos((175,200))
        t.pendown()
        t.setpos((205, 220))
    def leg1():
        t.penup()
        t.setpos((175,125))
        t.pendown()
        t.setpos((145, 95))
    def leg2():
        t.penup()
        t.setpos((175,125))
        t.pendown()
        t.setpos((205, 95))
    def open_mouth():
        t.penup()
        t.setpos((175, 235))
        t.pendown()
        t.dot(10)
    def frown():
        t.penup()
        t.setpos((175, 235))
        t.pendown()
        t.dot(15, 'white')
        t.penup()
        t.setpos((165, 235))
        t.pendown()
        t.left(90)
        t.circle(-10, extent = 180)
        t.penup()
    def smile():
        t.penup()
        t.setpos((175, 235))
        t.pendown()
        t.dot(15, 'white')
        t.penup()
        t.setpos((165, 240))
        t.pendown()
        t.right(90)
        t.circle(10, extent = 180)
        t.penup()

    def deadeyes():
        t.register_shape('dead', ((-5,-5), (-0.01,0), (-5,5), (0,0.01), (5,5), (0.01,0), (5,-5), (0,-0.01)))
        t.penup()
        t.setpos((165, 255))
        t.dot(15, 'white')
        t.shape('dead')
        stamp1 = t.stamp()
        t.setpos((185, 255))
        t.dot(15, 'white')
        stamp2 = t.stamp()

    if piece == 0:
        t.speed(10)
    else:
        t.speed(3)
    parts = ['head()', 'body()', 'arm1()', 'arm2()', 'leg1()', 'leg2()', 'open_mouth()', 'deadeyes()', 'frown()', 'smile()']
    piece = piece - 1
    eval(parts[piece])

def over_write(text, align, font):
    """
    Overwriting turtles is surprisingly hard. This function writes the previous
    text five times in white to clear it.
    """
    t.pencolor('white')
    for i in range(0,5):
        t.write(text, align = align, font = font)
    t.pencolor('black')

def run_turtles():
    """
    Reads the log file and commands turtles to move or write based on each line of the log.
    """
    global last_message, last_options, last_size, last_len, i, guess_counter
    log = open('comm.log', 'r')
    messages = [line[:-1] for line in list(log)]
    t.ht()
    draw_gallows()
    last_message, last_options, last_size, last_len, i, guess_counter = '', '', '', 6, 0, 0
    normal_font, bold_font = ('Times New Roman', 24, 'normal'), ('Times New Roman', 24, 'bold')

    # Displaying "Initializing" message.
    t.penup(); t.setpos((0, 400))
    t.write(messages[0], align = 'center', font = normal_font)
    t.setpos((0, 375))
    init_str = "Your word is " + (messages[1].split(' ')[3][:-1]) + ", but I can't see that."
    t.write(init_str, align = 'center', font = normal_font)
    t.penup(); t.setpos((0, -100))
    t.write('Ready!', align = 'center', font = ('Times New Roman', 30, 'bold'))
    t.setpos((0, -225))
    t.write('Guessed Letters', align = 'center', font = bold_font)

    def clickme(x, y):
        global last_message, last_options, last_size, last_len, i, guess_counter

        # Clearing the "Ready!"
        t.penup(); t.setpos((0, -100))
        over_write('Ready!', align = 'center', font = ('Times New Roman', 30, 'bold'))

        # Every click advances line by line until it reaches a new turn.
        while(True):
            i += 1
            if (i == len(messages)):
                # I don't know how to kill this thing short of sys.exit()
                sys.exit()

            if re.match('turns: ', messages[i]):
                # Writing "Ready!" at the end of each turn.
                t.penup(); t.setpos((0, -100))
                t.write('Ready!', align = 'center', font = ('Times New Roman', 30, 'bold'))
                return

            if re.match('dict_size: ', messages[i]):
                # Show Number of Words Left
                t.penup(); t.setpos((-450, 275))
                over_write(last_size, align = 'left', font = normal_font)
                write_str = 'Words to Choose From: ' + str(re.search('\d+', messages[i]).group())
                t.write(write_str, font = normal_font)
                last_size = write_str

            if re.match('Success!', messages[i]):
                # Clear Last Options
                t.setpos((-450, 200))
                for j in range(1, last_len):
                    overwrite_str = "My #" + str(j) + " guess: " + eval(last_options[14:])[j-1].upper()
                    if j == 1:
                        over_write(overwrite_str, align = 'left', font = bold_font)
                    else:
                        over_write(overwrite_str, align = 'left', font = normal_font)
                    t.setpos((-450, (200-j*25)))

                # Draw Smile
                draw_body(10)
                t.setpos((250, 325))
                t.write('I won! Want to play again?', align = 'center', font = ('Times New Roman', 22, 'bold'))
                return

            if re.match('Current word: ', messages[i]):
                # Updating Current Word
                t.setpos((250, -50))
                over_write(last_message, align = 'center', font = ('Times New Roman', 22, 'bold'))
                t.write(messages[i], align = 'center', font = ('Times New Roman', 22, 'bold'))
                last_message = messages[i]

            if re.match('Best Options: ', messages[i]):
                t.penup(); t.setpos((-450, 200))
                options_length = len(eval(messages[i][14:]))+1

                # Clearing Last Options
                for j in range(1, last_len):
                    if last_options == '': break
                    overwrite_str = "My #" + str(j) + " guess: " + eval(last_options[14:])[j-1].upper()
                    if j == 1:
                        over_write(overwrite_str, align = 'left', font = bold_font)
                    else:
                        over_write(overwrite_str, align = 'left', font = normal_font)
                    t.setpos((-450, (200-j*25)))

                t.setpos((-450, 200))

                # Write Current Options
                for j in range(1, options_length):
                    write_str = "My #" + str(j) + " guess: " + eval(messages[i][14:])[j-1].upper()
                    if j == 1:
                        t.write(write_str, font = bold_font)
                    else:
                        t.write(write_str, font = normal_font)
                    t.setpos((-450, (200-j*25)))

                last_options, last_len = messages[i], options_length

            if re.match('Guessed Letter: ', messages[i]):
                # Adds guessed words to bin at the bottom.
                guess_letter = re.search('\w$', messages[i]).group().upper()
                xspacing = list(range(-300, 300, 23))
                t.penup()
                t.setpos((xspacing[guess_counter], -300))
                if (guess_letter not in messages[1].split(' ')[3][:-1]):
                    t.pencolor('red')
                    t.write(guess_letter, align = 'center', font = normal_font)
                    t.pencolor('black')
                else:
                    t.write(guess_letter, align = 'center', font = normal_font)
                guess_counter += 1

            if re.match('wrongs: ', messages[i]):
                # Update the Hangman
                wrong = int(re.search('\d+', messages[i]).group())
                draw_body(wrong)
                if wrong == 9:
                    t.setpos((250, 325))
                    t.write('I lost! Want to play again?', align = 'center', font = ('Times New Roman', 22, 'bold'))
                    i = len(messages) - 1 # triggers sys.exit() in next iteration.
                    return

    t.onscreenclick(clickme)


def total_turtles(go):
    """
    This executes the whole function from beginning to end, starting with
    choosing a word to displaying the GUI.
    """
    word = input('What word would you like to choose? ')
    print('Your game is loading...')
    sys.stdout = open(os.devnull, 'w')  # disable printing
    write_new_word(word, go)
    run_turtles()
    t.done()
    sys.stdout = sys.__stdout__  # enable printing



# If running this script from the command line, full game plays.
# Otherwise, it only loads functions.
if __name__ == '__main__':
    total_turtles('go')



# bottom
