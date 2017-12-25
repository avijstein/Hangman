import os, sys, random
from time import sleep
import turtle as t
import hangman as hm
import re
import pandas as pd

os.chdir('/Users/ajstein/Desktop/Real Life/Coding Projects/Hangman/')

# this function brings in everything we need to run the variables from hangman in this space.
# hm.clear_log(True)
# hm.load_game('ant')
# print('-'*20)
# hm.gogogo()

# sys.exit()

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



def write_by_line(init_x, init_y, words):
    t.penup()
    t.setpos((init_x, init_y))
    for i in range(0, len(words)):
        t.write(words[i], font = ('Garamond', 24, 'normal'))
        t.sety(init_y - (i+1)*25)

somewords = ['alpha', 'bravo', 'charlie', 'delta']


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
    def frown():
        t.penup()
        t.setpos((165, 235))
        t.pendown()
        t.left(90)
        t.circle(-10, extent = 180)
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

    t.speed(10)
    parts = ['head()', 'body()', 'arm1()', 'arm2()', 'leg1()', 'leg2()', 'frown()', 'deadeyes()']
    piece = piece - 1
    # print(parts[piece])
    eval(parts[piece])


def run_turtles(messages, turns, wrongs):
    t.ht()
    draw_gallows()
    start_writing = 300

    for i in range(0,len(messages)):
        if (turns[i] == 0 and wrongs[i] == 0):
            # if re.match('Success!', messages[i]):
            #     print(messages[i])
            #     t.speed(3)
            #     t.penup()
            #     t.setpos((0, -50))
            #     t.write(messages[i], font = ('Times New Roman', 24, 'normal'))

            print(messages[i])
            t.speed(3)
            t.penup()
            t.setpos((-450, start_writing))
            t.write(messages[i], font = ('Times New Roman', 24, 'normal'))
            start_writing -= 25
        if wrongs[i] > 0:
            draw_body(wrongs[i])

run_turtles(messages, turns, wrongs)

t.done()






# bottom
