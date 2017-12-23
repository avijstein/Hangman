import os, sys, random
from time import sleep
import turtle as t
import hangman as hm

os.chdir('/Users/ajstein/Desktop/Real Life/Coding Projects/Hangman/')

# this function brings in everything we need to run the variables from hangman in this space.
# hm.load_game('ant')
# print('-'*20)
# hm.gogogo()

# print(hm.all_words.head())


# short = hm.all_words.iloc[0:5,0]



# for i in range(0,len(short)):
#     print(short.iloc[i].upper())
#     print('move down 50')


# sys.exit()


def write_by_line(init_x, init_y, words):
    t.penup()
    t.setpos((init_x, init_y))
    for i in range(0, len(words)):
        t.write(words[i], font = ('Garamond', 24, 'normal'))
        t.sety(init_y - (i+1)*25)



somewords = ['alpha', 'bravo', 'charlie', 'delta']

t.speed(6)
# write_by_line(-400, 300, somewords)

# t.done()


# the hangman drawing
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

def draw_body(pieces):
    def head():
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
    for i in range(0,pieces):
        eval(parts[i])


t.ht()
draw_gallows()
draw_body(8)

t.done()





# bottom
