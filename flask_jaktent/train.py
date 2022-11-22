# Chatbot Model Training

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
import tensorflow
from collections import Counter
import re

from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM,Input
import tensorflow.keras.layers as layers
from tensorflow.keras.layers import Lambda, dot, Activation, concatenate
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

import re
from nltk.corpus import stopwords
from nltk import word_tokenize,pos_tag
from nltk.stem import WordNetLemmatizer

# Use standard and non-standard questions as training data
data1 = pd.read_excel('./Data/FAQ.xls', sheet_name=0)
data1['Standard Question ID'] = 'FAQ' + data1['Standard Question ID'].astype(str)
# print(data1)
data2 = pd.read_excel('./Data/Presenter.xls', sheet_name=1)
data2['Standard Question ID'] = 'Presenter' + data2['Standard Question ID'].astype(str)
# print(data2)
data3 = pd.read_excel('./Data/Session.xls', sheet_name=1)
data3['Standard Question ID'] = 'Session' + data3['Standard Question ID'].astype(str)
# print(data3)
data4 = pd.read_excel('./Data/DailyChat.xls', sheet_name=0)
data4['Standard Question ID'] = 'DailyChat' + data4['Standard Question ID'].astype(str)
# print(data4)

data1 = data2.append(data1)
data1 = data1.append(data3)
data1 = data1.append(data4)
data1 = data1.sample(frac=1)

# print(data1.head())

# Create a map comparison table between Standard Question ID and Standard Question
dict1 = data1[['Standard Question ID','Standard Question']].drop_duplicates()
dict1 = dict(zip(list(data1['Standard Question']), list(data1['Standard Question ID'])))

def tokenize(sentence):
    # Remove redundant blanks, word segmentation, part-of-speech tagging
    sentence = re.sub(r'\s+', ' ', sentence)
    token_words = word_tokenize(sentence)
    # token_words = pos_tag(token_words)
    return token_words

'''Data processing'''
texts = list(data1['Non Standard Question'])
# Lowercase processing, remove parentheses
texts = [a.lower() for a in texts ]
# texts = [re.sub('\)','',a) for a in texts ]
# texts = [re.sub('\(','',a) for a in texts ]

# Symbol handling
texts = [tokenize(a) for a in texts ]

# words_to_id: Convert each word in the corpus into a word vector form, which is convenient for later training with LSTM network
words1 = []
for i in texts:
    words1.extend(i)
b = Counter(words1)
words = b.most_common()
# print(words)
words = [x[0] for x in words]
# print(words)
words_to_id = dict(zip(words,range(len(words))))
# print(len(words))
# print(words_to_id)

# Count the longest non-standard problem, so that it is convenient to specify the maxlen of LSTM
max_len = [len(a) for a in texts]
# print(max(max_len))
# print(np.mean(max_len))

# Convert a non standard question to the format of a set of word vectors
text_input = []
for text in texts:
    text_input1 = []
    for word in text:
        if word in words_to_id:
            text_input1.append(words_to_id[word])
        else:
            text_input1.append(len(words))
    text_input.append(text_input1)
# print(text_input)

# Use the pad_sequence() function to convert the sequence into a new sequence of the same length after padding

# text_input: nested list, 
# value: used to pad the sequence, 
# padding: post value means that when it is determined that it needs to be filled with 0, it will be filled at the end, 
# maxlen: the maximum length of the sequence
text_input = tensorflow.keras.preprocessing.sequence.pad_sequences(
    text_input, value=len(words),
    padding='post', maxlen=30
)

# Generate Standard Question tags so that non standard question tags can be matched according to tags
label_set = list(set(data1['Standard Question']))
label_dict = dict(zip(label_set,range(len(label_set))))
# print(label_set)
# print(label_dict)

data1['label'] = data1['Standard Question'].replace(label_dict)
labels = list(data1['label'])
labels = np.array(labels)
# print(labels)

# Divide training set and test set
X_train,X_test = text_input[0:20000],text_input[20000:]
Y_train,Y_test = labels[0:20000],labels[20000:]

# Build the model, shape: [None, 30, 128], pay attention to the input data dimension len(words)+1, "+1" is for irrelevant words
input_tensor = Input(shape=(30,))
embeding = layers.Embedding(len(words)+1,128)(input_tensor)
print(embeding.shape)

# return_sequences=False: Only return the value of the output based on the current input, 
# Dropout: prevent the model from overfitting
lstm1 = layers.LSTM(256,return_sequences=False)(embeding)
dropout1 = layers.Dropout(0.05)(lstm1)

# The final output of the entire network adopts Softmax, which is fully connected with LSTM
output_tensor = layers.Dense(len(label_dict))(dropout1)
output_tensor = layers.Softmax()(output_tensor)

# Input and output models
model = Model(inputs=input_tensor,outputs=output_tensor)

# Compile and execute training, using Adam optimizer, loss function using cross entropy
model.compile(optimizer=tensorflow.keras.optimizers.Adam(1e-2), loss='sparse_categorical_crossentropy', metrics=['acc'])
model.fit(X_train,Y_train,validation_data=(X_test,Y_test),epochs=10, batch_size=32,verbose=1)

# Save model file
model.save('model_files/lstm.h5')

import pickle
# Data dictionary: a set of non standard question word vectors, used as a standard for predicting answers after and user input questions
f1 = open('model_files/word_to_id.txt', 'wb')
pickle.dump(words_to_id, f1)
f1.close()

# Tag dictionary: for tag matching
f1 = open('model_files/label_dict.txt', 'wb')
pickle.dump(label_dict, f1)
f1.close()

# Standard question and non standard question comparison table
f1 = open('model_files/dict1.txt', 'wb')
pickle.dump(dict1, f1)
f1.close()