# Chatbot Model Q&A Prediction

import json
import random
import pickle
import pandas as pd
import numpy as np
from math import exp
import collections
from sklearn.model_selection import train_test_split
import datetime
from tensorflow import keras
from collections import Counter
import re

from keras import Input, Model
from keras.layers import Dense
from keras.layers import LSTM,Input
import keras.layers as layers
from keras.layers import Lambda, dot, Activation, concatenate
# from keras.utils import to_categorical

import re
from nltk.corpus import stopwords
from nltk import word_tokenize,pos_tag
from nltk.stem import WordNetLemmatizer

def tokenize(sentence):
    # Remove redundant blanks, word segmentation, part-of-speech tagging
    sentence = re.sub(r'\s+', ' ', sentence)
    token_words = word_tokenize(sentence)
    #token_words = pos_tag(token_words)   
    return token_words

# Read data for standard answer
data1 = pd.read_excel('./Data/FAQ.xls',sheet_name=1)
data1['Standard Question ID'] = 'FAQ' + data1['Standard Question ID'].astype(str)
data1['Standard Question Answer'] = data1['Standard Question Answer']
data1 = data1.iloc[:,0:3]
# print(data1)

data2 = pd.read_excel('./Data/Presenter.xls',sheet_name=0)
data2['Standard Question ID'] = 'Presenter' + data2['Standard Question ID'].astype(str)
data2['Standard Question Answer'] = data2['Standard Question Answer']
data2 = data2.iloc[:,0:3]
# print(data2)

data3 = pd.read_excel('./Data/Session.xls',sheet_name=0)
data3['Standard Question ID'] = 'Session'+data3['Standard Question ID'].astype(str)
data3['Standard Question Answer'] = data3['Standard Question Answer']
data3 = data3.iloc[:,0:3]
# print(data3)

data4 = pd.read_excel('./Data/DailyChat.xls',sheet_name=1)
data4['Standard Question ID'] = 'DailyChat'+data4['Standard Question ID'].astype(str)
data4 = data4.iloc[:,0:3]
# print(data4)

data = data1.append(data2)
data = data.append(data3)
data = data.append(data4)
# print(data.shape)

# Load data dictionary
import pickle
f1 = open('model_files/word_to_id.txt', 'rb')
words_to_id = pickle.load(f1)
f1.close()

# Load model
model = keras.models.load_model('model_files/lstm.h5')

# Load result dictionary
f1 = open('model_files/label_dict.txt', 'rb')
label_dict = pickle.load(f1)
f1.close()

# Load the standard/non-standard dictionary
f1 = open('model_files/dict1.txt', 'rb')
dict1 = pickle.load(f1)
f1.close()

label_dict_reverse = dict(zip(label_dict.values(), label_dict.keys()))

# questions = ['Know something about Jessica Brody','Is Jaktent session open for global people?']

def predict(text):
    # Lowercase processing, remove parentheses
    questions = text
    questions = [a.lower() for a in questions]
    questions = [tokenize(a) for a in questions]
    text_input = []
    for text in questions:
        text_input1 = []
        for word in text:
            if word in words_to_id:
                text_input1.append(words_to_id[word])
            else:
                text_input1.append(len(words_to_id))
        text_input.append(text_input1)
    text_input = keras.preprocessing.sequence.pad_sequences(
        text_input, value=len(words_to_id),
        padding='post', maxlen=30
    )

    # Forecast result
    pred = model.predict(text_input)
    pred = list(np.argmax(pred, 1))
    # Return result
    result = [label_dict_reverse[a] for a in pred]
    # print(result)
    result = [dict1[a] for a in result][0]
    # print(result)
    result = data[data['Standard Question ID'] == result].iloc[0, 2]

    return result
