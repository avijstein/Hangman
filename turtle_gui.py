import os, sys, random, re
from time import sleep
import turtle as t
import hangman as hm
import pandas as pd

# Change to user's cwd.
os.chdir('/Users/ajstein/Desktop/Real Life/Coding Projects/Hangman/')

def write_new_word(word, go):
    """
    Clears the comm.log and loads a game on the turtle_gui side.
    Doesn't generate gui, just preps it.
    """
    hm.clear_log(True)
    hm.load_game(word)
    print('-'*20)
    hm.gogogo()
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

# def discard_bin(word, num):




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
    word = input('What word would you like to choose? ')
    print('Your game is loading...')
    sys.stdout = open(os.devnull, 'w')  # disable printing
    write_new_word(word, go)
    run_turtles()
    t.done()
    sys.stdout = sys.__stdout__  # enable printing

# total_turtles('go')

# write_new_word('catfish', 'go away')

run_turtles()
t.done()



# bottom
