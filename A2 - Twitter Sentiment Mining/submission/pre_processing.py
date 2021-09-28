import numpy as np
import regex as re
from nltk import ngrams, FreqDist

### Relabelling positive labels from 4 to 1
def polarity_modifier(df):
    df['Polarity'] = np.where(df['Polarity'] == 4, 1, 0)
    return df


### Adding a prefix to completely capital words
def all_caps(tweet):
    tweet = re.sub(r'\b([A-Z]{2,})\b', r'CAPS_\1', tweet)
    return tweet


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
    return ' '.join(tweet.split())


### Removes extra punctuations except for clitic
def remove_punc(tweet):
    tweet = re.sub(r"[^\w'\s]+",' ', tweet)                  # Removing punctuations apart from clitic
    return tweet


### Handling clitics
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


### Common short forms that are worth translating
short_forms = {
    'n': 'and',
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
    'ty': 'thanks',
    'sux': 'sucks',
    'missin': 'missing'
    }


### To convert shortforms
def handle_shortforms(tweet):
    temp = ''
    for word in tweet.split():
        if word in short_forms.keys():
            temp = temp + ' ' + short_forms[word]
        else:
            temp = temp + ' ' + word
    return ' '.join(temp.split())


### Maintaining only letters within a tweet and removing every other information since not indicative of sentiment
def maintain_letters(tweet):
    tweet = re.sub(r'[^a-zA-Z]', ' ', tweet) 
    return ' '.join(tweet.split())


### Emoticons store a lot of information
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


### Normalises words with repititive letters like loooolll
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


### Add negation to following two words after 'not'
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


### Creating sentence from tokenised version
def sentence_creator(df, col_name, title):
    df[title] = df[col_name].apply(lambda x:' '.join([token for token in x]))
    return df