## Import required libraries
import numpy as np
import pandas as pd
import sys
import pickle
import pre_processing as pp
import time

t0 = time.time()

# from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.linear_model import LogisticRegression, SGDClassifier
# from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score


## Loading Data
model_location = sys.argv[1]
test_location = sys.argv[2]
prediction_location = sys.argv[3]


## Loading pre-trained model
pipe = pickle.load(open(model_location, "rb"))


## Reading test data
test = []
with open(test_location, 'r', encoding='ISO-8859-1') as f:
    for line in f:
        test.append(line)
    # test = f.read().splitlines()
    f.close()
df = pd.DataFrame({'Tweet': test})

## Reading gold labels
gold = []
with open('data/gold.txt', 'r') as f:
    # test.append(f.readlines())
    for line in f:
        gold.append(int(line))
    # test = f.read().splitlines()
    f.close()
gold = pd.Series(gold)


## Pre-Processing
df['Tweet_caps'] = df['Tweet'].apply(pp.all_caps)
df['Tweet_regex'] = df['Tweet_caps'].apply(pp.clean_text)
df['Tweet_emoji'] = df['Tweet_regex'].apply(pp.emoticon_translation)
df['Tweet_nopunc'] = df['Tweet_emoji'].apply(pp.remove_punc)
df['Tweet_clitics'] = df['Tweet_nopunc'].apply(pp.handle_clitics)
df['Tweet_shortforms'] = df['Tweet_clitics'].apply(pp.handle_shortforms)
df['Tweet_pure_string'] = df['Tweet_shortforms'].apply(pp.maintain_letters)
df['Tweet_token'] = df['Tweet_pure_string'].apply(pp.tweet_word_tokenizer)
df = pp.sentence_creator(df, 'Tweet_token', 'Tweet_sent')
df['Tweet_normalised'] = df['Tweet_sent'].apply(pp.normalisation_words)
df['Tweet_normal_negated'] = df['Tweet_normalised'].apply(pp.add_negation)
df = pp.sentence_creator(df, 'Tweet_normal_negated', 'Tweet_final_sent')
## Using stemmer, lemmatizer, stopword removal, sentiment lexicon technique, etc. did not add to the F1 Score; even individually. Rather were decreasing the F1.


## Test Data
X_test = df['Tweet_final_sent']


## Generating predictions for test data
y_pred_lr = pipe.predict(X_test)


gold = np.where(gold == 4, 1, 0)

print('F1 Score: ', f1_score(gold, y_pred_lr))


## Converting pos_label and saving predictions
y_pred_lr = np.where(y_pred_lr == 1, 4, 0)
with open(prediction_location, 'w') as f:
    for pred in y_pred_lr:
        f.write('%d' %pred)
        f.write('\n')


t1 = time.time()
total = t1-t0

print('Time spent testing is:', total, 's')