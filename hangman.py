import os
import numpy as np
import pandas as pd


os.chdir('/Users/ajstein/Desktop/Real Life/Coding Projects/Hangman/')
df = pd.read_table('./master_dict.txt', sep='\r', header=None, names=['words'])
df['words'] = df['words'].str.lower().drop_duplicates()

word_length = 8
df = df.loc[df['words'].str.len() == word_length]

df2 = df['words'].apply(lambda x: pd.Series(list(x))) # this is SLOW


def letter_freq(df):
    new_df = df.apply(pd.value_counts).fillna(0)
    new_df['total'] = new_df.sum(axis = 1)
    new_df = new_df.sort_values(by = 'total', ascending = False)
    return(new_df['total'].index)


print(letter_freq(df2))






# bottom
