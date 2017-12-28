import os, sys, random
from time import sleep
import turtle as t
import hangman as hm
import re
import pandas as pd

os.chdir('/Users/ajstein/Desktop/Real Life/Coding Projects/Hangman/')

def write_new_word(word):
    """
    Clears the comm.log and loads a game on the turtle_gui side.
    Doesn't generate gui, just preps it.
    """
    hm.clear_log(True)
    hm.load_game(word)
    print('-'*20)
    hm.gogogo()
    # sys.exit() inherited from play_game().

# write_new_word('cow')

print('---- LOG TIME ----')
# short = hm.all_words.iloc[0:5,0]
# sys.exit()

log = open('comm.log', 'r')
messages = []
turns = []
wrongs = []
for line in log:
    messages.append(line[:-1])
    turns.append(0)
    wrongs.append(0)
    if re.match('turns', line):
        turns[len(turns)-1] = int(re.search('\d+', line).group())
    if re.match('wrongs', line):
        wrongs[len(wrongs)-1] = int(re.search('\d+', line).group())


# content = pd.DataFrame({'message': loglist, 'turns': turns, 'wrongs': wrongs})
# short = (content[content['turns'] != 0]).append(content[content['wrongs'] != 0]).sort_index()


# print(len(messages))
# print('turns: ', turns)
# print('wrongs: ', wrongs)

# for i in range(0,10):
    # print(messages[i], turns[i], wrongs[i])

# sys.exit()


def draw_gallows():
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


# print(eval(messages[4][14:]))
#
# top_guess = eval(messages[4][14:])[0]
# other_guesses = eval(messages[4][14:])[1:]
#
# print('top_guess: ', top_guess)
# print('other_guesses: ', other_guesses)
#
#
# sys.exit()



def run_turtles(messages, turns, wrongs):
    t.ht()
    draw_gallows()
    start_writing = 300
    last_message = ''

    # Displaying "Initializing" message.
    t.penup(); t.setpos((0, 400))
    t.write(messages[0], align = 'center', font = ('Times New Roman', 24, 'normal'))
    t.setpos((0, 375))
    t.write(messages[1], align = 'center', font = ('Times New Roman', 24, 'normal'))


    for i in range(2,len(messages)):
        if (turns[i] == 0 and wrongs[i] == 0):
            if re.match('Success!', messages[i]):
                draw_body(10)
                t.setpos((250, 325))
                t.write('Success! The computer wins.', align = 'center', font = ('Times New Roman', 22, 'bold'))
                return
            if re.match('Current word: ', messages[i]):
                t.setpos((250, -50))
                over_write(last_message, align = 'center', font = ('Times New Roman', 22, 'bold'))
                t.write(messages[i], align = 'center', font = ('Times New Roman', 22, 'bold'))
                last_message = messages[i]
                continue
            t.speed(3)
            t.penup()
            t.setpos((-450, start_writing))
            t.write(messages[i], font = ('Times New Roman', 22, 'normal'))
            start_writing -= 25
        if wrongs[i] > 0:
            if wrongs[i] == 9:
                draw_body(wrongs[i])
                t.setpos((250, 325))
                t.write('Failed! The computer loses.', align = 'center', font = ('Times New Roman', 22, 'bold'))
                return
            draw_body(wrongs[i])

run_turtles(messages, turns, wrongs)

t.done()


# TODO: Add feature of "how many words am i pulling from" with len(df).
# TODO: Build "best options" leaderboard with #1 suggestion and four others below it. Have it update each time.
# TODO: Update README with description of turtles, along with screencaps of it.
# TODO: Play again? Come up with a word to beat the game?
# TODO: Advance by clicking.




# bottom
