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


## Combining Data
df = data_neg.append(data_pos)
df = df.iloc[:,1:]


### Relabelling positive labels from 4 to 1
def polarity_modifier(df):
    df['Polarity'] = np.where(df['Polarity'] == 4, 1, 0)
    return df



### Tokenising tweets
def tweet_word_tokenizer(tweet):
    return tweet.split(' ')


### Cleaning tweets using regular expressions
def clean_text(tweet):
    tweet = tweet.lower()                                   # Converting to lower case
    tweet = re.sub(r'\b\w+@[^\s]+', ' <MAIL> ', tweet)      # Removing email IDs
    tweet = re.sub(r'@[^\s]+', ' <MENTION> ', tweet)        # Removing mentions
    tweet = re.sub(r'https?:\/[^\s]+', ' <URL> ', tweet)    # Removing URLs
    tweet = re.sub(r'www.[^\s]+', ' <WEBSITE> ', tweet)     # Removing Websites
    tweet = re.sub(r'\b\w+\.com', ' <WEBSITE> ', tweet)     # Removing email IDs
    tweet = re.sub(r'#', ' <HASHTAG> ', tweet)              # Removing hashtags
    tweet = re.sub(r'_', ' ', tweet)                        # Sometimes hashtags are done with _ representing break between two words
    tweet = re.sub(r'\.{2,}', ' ', tweet)                   # Removing sentence separators
    tweet = re.sub(r"[0-9]+",' ', tweet)                    # Removing numbers as they do not indicate sentiment
    tweet = re.sub(r"\bamp\b", ' ', tweet)                  # Removing &amp signs mis-translated
    tweet = re.sub(r"\bquot\b", ' ', tweet)                 # Removing &quot signs mis-translated
    tweet = re.sub(r"\b\w+;[^\s]+\b", ' ', tweet)           # Removing ';gt' kinds of issues
    
    # if len(tweet) == 0:
    #   tweet = 'None'
    return ' '.join(tweet.split())


### Removes extra punctuations except for clitic
def remove_punc(tweet):
    tweet = re.sub(r"[^\w'\s]+",' ', tweet)                  # Removing punctuations apart from clitic
    return tweet


# Handling clitics
def handle_clitics(tweet):
    tweet = re.sub(r"\bwon\'t\b", "will not", tweet)
    tweet = re.sub(r"\bwont \b", "will not", tweet)
    tweet = re.sub(r"\bwouldn't\b", "would not", tweet)
    tweet = re.sub(r"\bwouldnt\b", "would not", tweet)

    tweet = re.sub(r"\bcan\'t\b", "can not", tweet)
    tweet = re.sub(r"\bcant\b", "can not", tweet)

    tweet = re.sub(r"\bdon't\b", "do not", tweet)
    tweet = re.sub(r"\bdont\b", "do not", tweet)
    tweet = re.sub(r"\bdoesn't\b", "does not", tweet)
    tweet = re.sub(r"\bdoesnt\b", "does not", tweet)
    tweet = re.sub(r"\bdidn't\b", "did not", tweet)
    tweet = re.sub(r"\bdidnt\b", "did not", tweet)

    tweet = re.sub(r"\bhasn't\b", "has not", tweet)
    tweet = re.sub(r"\bhasnt\b", "has not", tweet)
    tweet = re.sub(r"\bhaven't\b", "have not", tweet)
    tweet = re.sub(r"\bhavent\b", "have not", tweet)
    tweet = re.sub(r"\bhadn't\b", "had not", tweet)
    tweet = re.sub(r"\bhadnt\b", "had not", tweet)

    ## Have to be done after the previous ones because they are overallaping in nature
    tweet = re.sub(r"n\'t", " not", tweet)
    tweet = re.sub(r"\'ve", " have", tweet)
    tweet = re.sub(r"\'re", " are", tweet)
    tweet = re.sub(r"\'s", " is", tweet)
    tweet = re.sub(r"\'m", " am", tweet)
    tweet = re.sub(r"\'re", " are", tweet)
    tweet = re.sub(r"\'ll", " will", tweet)
    tweet = re.sub(r"\'d", " would", tweet)
    
    return ' '.join(tweet.split())


## Common short forms that are worth translating
short_forms = {
    'n': 'and',
    'nu': 'not',
    'no': 'not',
    'ya': 'you',
    'luv': 'love',
    'lol': 'laugh',
    'k': 'okay',
    'na': 'not',
    'ily': 'love',
    'im': 'am',
    'morn': 'morning',
    'nght': 'night',
    'no': 'not',
    'Ill': 'will',
    'shoulda': 'should have',
    'thnks': 'thanks',
    'ty': 'thanks'
    }


## To convert shortforms
def handle_shortforms(tweet):
    temp = ''
    for word in tweet.split():
        if word in short_forms.keys():
            temp = temp + ' ' + short_forms[word]
        else:
            temp = temp + ' ' + word
    return ' '.join(temp.split())



## Maintaining only letters within a tweet and removing every other information since not indicative of sentiment
def maintain_letters(tweet):
    tweet = re.sub(r'[^a-zA-Z]', ' ', tweet) 
    return ' '.join(tweet.split())


## Emoticons store a lot of information
def emoticon_translation(tweet):
    tweet = re.sub(r":\)", " happy ", tweet)
    tweet = re.sub(r":-\)", " happy ", tweet)
    tweet = re.sub(r";\)", " happy ", tweet)
    tweet = re.sub(r":d", " laaugh ", tweet)            # 'aa' in laugh to specify that emoji has a certain significance; also used later in extended versions of ha and lol
    tweet = re.sub(r";d", " laaugh ", tweet)            # To give more significance
    tweet = re.sub(r"xd", " laaugh ", tweet)
    tweet = re.sub(r"<3", " love ", tweet)

    tweet = re.sub(r":\(", " sad ", tweet)
    tweet = re.sub(r":-\(", " sad ", tweet)
    tweet = re.sub(r":/", " sad ", tweet)
    tweet = re.sub(r":\\", " sad ", tweet)
    tweet = re.sub(r":o", " sad ", tweet)           # Suprised might not be the correct representation

    return tweet


## Normalises words with repititive letters like loooolll
def normalisation_words(tweet):
    tweet = tweet.replace(r'([a-z])\1{1,}', r'\1\1')
    tweet = re.sub(r'h+a+[ha]+\b', r'laaugh', tweet)     # To give more significance
    tweet = re.sub(r'l+o+[lo]+\b', r'laaugh', tweet)     # To give more significance

    tweet = re.sub(r'\b([a-z])\1{1,}', r' ', tweet)     # If only repeated letters are left, remove them
    tweet = re.sub(r'\b([a-z])\1{1,}', r' ', tweet)     # If only repeated letters are left, remove them
    tweet = re.sub(r'([a-z])\1{2,}', r'\1\1', tweet)     
    tweet = re.sub(r'([a-z])\1{1,}\b', r'\1\1', tweet)     

    tweet = re.sub(r"\b[a-zA-Z]{1}\b", ' ', tweet)        # Removing single letters
    return tweet.split()


## Add negation to following two words after 'not'
def add_negation(tweet):
    flag = False
    count = 0
    tweet_new = []

    for word in tweet:
        if flag and count < 2:          # Adding prefix to next three words
            word = 'NEG_' + word
            count += 1
        elif word in ['not', 'cannot', 'cant']:     # Others must have already been processed
            flag = True
        tweet_new.append(word)
    return tweet_new


## Creating sentence from tokenised version
def sentence_creator(df, col_name, title):
    df[title] = df[col_name].apply(lambda x:' '.join([token for token in x]))
    return df


## Pre-Processing
df = df.sample(frac=0.1, random_state=1)

## To create temporary test file
# X_train, X_test, y_train, y_test = train_test_split(df['Tweet'], df['Polarity'], stratify=df['Polarity'], test_size=0.1, random_state=2) 
# with open('data/test.txt', 'w', encoding='ISO-8859-1') as f:
#     for tweet in X_test:
#         f.write(tweet)
#         f.write('\n')


df = polarity_modifier(df)
df['Tweet_regex'] = df['Tweet'].apply(clean_text)
df['Tweet_emoji'] = df['Tweet_regex'].apply(emoticon_translation)
df['Tweet_nopunc'] = df['Tweet_emoji'].apply(remove_punc)
df['Tweet_clitics'] = df['Tweet_nopunc'].apply(handle_clitics)
df['Tweet_shortforms'] = df['Tweet_clitics'].apply(handle_shortforms)
df['Tweet_pure_string'] = df['Tweet_shortforms'].apply(maintain_letters)
df['Tweet_token'] = df['Tweet_pure_string'].apply(tweet_word_tokenizer)
df = sentence_creator(df, 'Tweet_token', 'Tweet_sent')
df['Tweet_normalised'] = df['Tweet_sent'].apply(normalisation_words)
df = sentence_creator(df, 'Tweet_normalised', 'Tweet_sent_normal')
df['Tweet_normal_negated'] = df['Tweet_normalised'].apply(add_negation)
df = sentence_creator(df, 'Tweet_normal_negated', 'Tweet_final_sent')


X_train, X_test, y_train, y_test = train_test_split(df['Tweet'], df['Polarity'], stratify=df['Polarity'], test_size=0.1, random_state=2)      # to create temporary test file


pipe = Pipeline([
                ('vectoriser', TfidfVectorizer(token_pattern=r'[a-z]+', min_df=1, ngram_range=(1,2))),
                ('model', SGDClassifier(random_state=1, loss='hinge'))
                ])

pipe.fit(X_train, y_train)
y_pred_sgd = pipe.predict(X_test)
print('F1 Score: ', f1_score(y_test, y_pred_sgd))
sum(y_pred_sgd == y_test)/len(y_test)


coefs = pd.DataFrame(pipe['model'].coef_, 
                     columns=pipe['vectoriser'].get_feature_names())
coefs = coefs.T.rename(columns={0:'coef'}).sort_values('coef')
## To create temporary test file
# X_train, X_test, y_train, y_test = train_test_split(df['Tweet'], df['Polarity'], stratify=df['Polarity'], test_size=0.1, random_state=2) 
# with open('data/coefs.csv', 'w', encoding='ISO-8859-1') as f:
#     for tweet in X_test:
#         f.write(tweet)
#         f.write('\n')
coefs.to_csv('data/coef.csv')

coef_pos_set = set(coefs.iloc[np.where(coefs['coef'] > 1)].index.tolist())        # 'good' was missing if put 1
coef_neg_set = set(coefs.iloc[np.where(coefs['coef'] < 1)].index.tolist())


## Adds some keywords depicting the overall polarity felt
def words_freq(tweet):
  num_pos = len(set(tweet).intersection(coef_pos_set))
  num_neg = len(set(tweet).intersection(coef_neg_set))
  
  # If there exist positive words in the tweet
  if num_pos:
      for num in range(num_pos):
          tweet.append('POSITIVE')
  if num_neg:
      for num in range(num_neg):
          tweet.append('NEGATIVE')
  return tweet


df['Tweet_lexicons'] = df['Tweet_normal_negated'].apply(words_freq)
df = sentence_creator(df, 'Tweet_lexicons', 'Tweet_final_sent_lexicons')


X_train, X_test, y_train, y_test = train_test_split(df['Tweet_final_sent_lexicons'], df['Polarity'], stratify=df['Polarity'], test_size=0.1, random_state=2)


pipe = Pipeline([
                ('vectoriser', CountVectorizer(ngram_range=(1, 2), min_df=1)),
                ('model', LogisticRegression(penalty='l2',
                         solver='saga',
                         multi_class='multinomial',
                         tol=1e-5,
                         n_jobs = -1,
                         max_iter = 100))
                ])

pipe.fit(X_train, y_train)
y_pred_lr = pipe.predict(X_test)
print('F1 Score after using Lexicons: ', f1_score(y_test, y_pred_lr))
# sum(y_pred_lr == y_test)/len(y_test)