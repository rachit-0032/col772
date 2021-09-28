## Import required libraries
import pandas as pd
import time
import sys
import pickle
import pre_processing as pp

t0 = time.time()

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
# from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
# from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, f1_score


## Loading Data
train_location = sys.argv[1]
model_location = sys.argv[2]


## Reading data
df = pd.read_csv(train_location, encoding='ISO-8859-1')


## Pre-Processing
df = pp.polarity_modifier(df)
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

## Training Data. Complete pre-processed dataset
X_train = df['Tweet_final_sent']
y_train = df['Polarity']


## Building Pipeline
pipe = Pipeline([
                ('vectoriser', CountVectorizer(ngram_range=(1, 2), min_df=1)),
                ('model', LogisticRegression(penalty='l2',
                         solver='saga',
                         multi_class='multinomial',
                         tol=1e-5,
                         n_jobs = -1,
                         max_iter = 100))
                ])
                

## Fitting over training data
pipe.fit(X_train, y_train)


## Saving model at the given location
pickle.dump(pipe, open(model_location, "wb"))


t1 = time.time()
total = t1-t0

print('Time spent training is:', total, 's')