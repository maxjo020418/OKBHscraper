import numpy as np
import pandas as pd
import pickle
import praw
import time

from termcolor import colored
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

lemmatizer = WordNetLemmatizer()

print('importing complete\n')

# you can remove the 3 lines below (used for getting api stuffs)
infile = open('../keys', 'rb')
keys = pickle.load(infile)
infile.close()
# API keys here ~
reddit = praw.Reddit(client_id = keys['client_id'],
                     client_secret = keys['client_secret'],
                     username = keys['username'],
                     password = keys['password'],
                     user_agent = keys['user_agent'],
                     )

def preprocess(corpus):
    preprocess_logfile = open('./data/preprocess_logfile.txt', 'w', encoding = 'utf-8')
    clean_text = list()

    i = 0
    print('lemmatizing...(preprocessing)')
    for row in tqdm(corpus):
        # tokenize, clean, lemmatize
        tokens = word_tokenize(row)
        tokens = [token.lower() for token in tokens]
        tokens = [token for token in tokens if token.isalpha()]
        tokens = [token for token in tokens if token not in stopwords.words('english')]

        for i in range(len(tokens)):
            preprocess_logfile.write(tokens[i] + ' -> ')
            lemmanized_token = lemmatizer.lemmatize(tokens[i])
            preprocess_logfile.write(lemmanized_token + '\n')
            tokens[i] = lemmanized_token

        # make into one clean sentence
        clean_sentence = ''
        clean_sentence = ' '.join(token for token in tokens)
        clean_text.append(clean_sentence)

    preprocess_logfile.close()
    return clean_text

infile = open('./data/post_filtered_pickle', 'rb')
posts = pickle.load(infile)
infile.close()

TIMEOUT_AFTER_COMMENT_IN_SECS = .025

posts_list, comment_list = list(), list()

comment_logfile = open('./data/comment_logfile.txt', 'w', encoding = 'utf-8')
post_count = 1
print('fetching...')
for submission_id in tqdm(np.unique([ post['id'] for post in posts ])):
    # print('\n', '=' * 30, f'{post_count} posts out of {len(posts)}')
    # print(f'{submission_id}:\n')

    submission = reddit.submission(id=submission_id)
    posts_list.append(submission)
    submission.comments.replace_more(limit=None)

    comment_logfile.write('='*15 + '\n' + submission_id + '\n')

    comment_count = 1
    for comment in submission.comments.list():
        if comment.author != 'AutoModerator':
            # print(f'{comment_count} out of {len(submission.comments.list())}')

            comment_list.append(comment.body)
            comment_count += 1

            comment_logfile.write(str(comment) + ' : ' + comment.body + '\n')
        else:
            # print('automod ignored!', end = ' | ')
            # print(f'{comment_count} out of {len(submission.comments.list())}')
            comment_logfile.write(str(comment)+ ' (AutoModerator)' + ' : ' + comment.body + '\n')
            comment_count += 1

        if TIMEOUT_AFTER_COMMENT_IN_SECS > 0:
            time.sleep(TIMEOUT_AFTER_COMMENT_IN_SECS)

    post_count += 1

comment_logfile.close()

print()
print('post count:', len(posts_list))
print('comment count:', len(comment_list))

print()
clean_comment_list = preprocess(comment_list)

# making the CountVectorizer #######################################################################
cv = CountVectorizer(ngram_range=(1,1))
X = cv.fit_transform(clean_comment_list)
Xc = (X.T * X) # matrix manipulation
Xc.setdiag(0) # set the diagonals to be 0

names = cv.get_feature_names_out() # the entity names (i.e. keywords)
df = pd.DataFrame(data = Xc.toarray(), columns = names, index = names)

# reducing the size of the matrix (based on no. of mentions) #######################################################################
def reducer():
    inp = input('current size is ' + str(len(fdist)) + '. reduce matrix size?, size < 3000 recommended (y/n)\n')
    if inp == 'y':
        # cutoff point(based on the number of references) for reducing matrix
        con = 'n'
        while con == 'n':
            cutoff = int(input('input cutoff point(int): '))
            kill = [k for k, v in fdist.items() if v <= cutoff]
            con = input('size after reducing: ' + str(len(fdist) - len(kill)) + '\ncontinue? (y/n) ')

        print(colored('\nBEFORE', 'red'))
        print(df)

        df.drop(kill, inplace = True, axis = 0, errors = 'ignore')
        df.drop(kill, inplace = True, axis = 1, errors = 'ignore')

        print(colored('\n\nAFTER', 'green'))
        print(df)

        # print(list(set(df_matrix.index.tolist()) - set(df_matrix.columns.tolist())))
        print('nullcheck: ', end = '')
        print(df.isnull().values.any())

        df.to_csv('./data/gephi.csv', sep = ',')

    elif inp == 'n':
        df.to_csv('./data/gephi.csv', sep = ',')
    else:
        print('wrong input')
        reducer()

# fdist, rank.txt #######################################################################
temp = ''
for x in clean_comment_list: temp += x + ' '
fdist = dict(FreqDist(word_tokenize(temp)))

fdist = {k: v for k, v in sorted(fdist.items(), key = lambda item: item[1])}

rank = open('./data/rank.txt', 'w', encoding = 'utf-8')
[rank.write(k + ' : ' + str(v) + '\n') for k, v in fdist.items()]
rank.close()

fdist_pickle = open('./data/fdist', "wb")
pickle.dump(fdist, fdist_pickle)
fdist_pickle.close()

###############################################
reducer()
