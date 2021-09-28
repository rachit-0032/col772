## Import required libraries
import numpy as np
import pandas as pd
import re
import nltk
import sklearn
import sys
import pickle

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, f1_score

## NLTK Packages
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import sentiwordnet as swn
from nltk import ngrams, FreqDist
from nltk.corpus import wordnet

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

## Loading Data
train_pos_location = sys.argv[1]
train_neg_location = sys.argv[2]
model_location = sys.argv[3]


## Reading data
data_pos = pd.read_csv(train_pos_location, encoding='ISO-8859-1')
data_neg = pd.read_csv(train_neg_location, encoding='ISO-8859-1')


