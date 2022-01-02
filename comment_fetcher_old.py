from textblob import TextBlob
from collections import Counter
import pickle
import numpy as np
import praw
import time

reddit = praw.Reddit(client_id = '',
                     client_secret = '',
                     username = '',
                     password = '',
                     user_agent = '',
                     )

with open('stop_words_english.txt', encoding = 'utf-8') as f:
    stopwords = f.readlines()
stopwords = [word.strip() for word in stopwords]

def get_nouns(inp):
    matches = ["'", 'http', 'https', '.com', 'thi', 'ymy', 'time', 'good', 'person']

    inp = TextBlob(inp.lower())#.correct()

    nouns = inp.words.singularize()
    nouns = [noun for noun in nouns if len(noun) > 2]
    nouns = [noun for noun in nouns if noun not in stopwords]
    nouns = [noun for noun in nouns if not any(x in noun for x in matches)]
    return nouns

'''
def count_up(inp):
    inp = sum(inp, [])
    count = Counter(inp)
    return count
'''

infile = open('post_filtered', 'rb')
posts = pickle.load(infile)
infile.close()

TIMEOUT_AFTER_COMMENT_IN_SECS = .025

posts_list = []
comment_list = []

f = open('logfile.txt', 'w', encoding = 'utf-8')
post_count = 1
for submission_id in np.unique([ post['id'] for post in posts ]):
    print()
    print('=' * 30, f'{post_count} posts out of {len(posts)}')
    print(f'{submission_id}:\n')

    submission = reddit.submission(id=submission_id)
    posts_list.append(submission)
    submission.comments.replace_more(limit=None)

    f.write('==============\n' + submission_id + '\n')

    comment_count = 1
    for comment in submission.comments.list():
        if not comment.author == 'AutoModerator':
            print(f'{comment_count} out of {len(submission.comments.list())}')
            comment_list.append(get_nouns(comment.body))
            f.write(str(comment) + ' : ' + comment.body + '\n')
        else:
            print('AutoMod ignored')

        comment_count += 1

        if TIMEOUT_AFTER_COMMENT_IN_SECS > 0:
            time.sleep(TIMEOUT_AFTER_COMMENT_IN_SECS)

    post_count += 1

print('\n')
print('post count:', len(posts_list))
print('comment count:', len(comment_list))

comment_list = [comment_list for comment_list in comment_list if comment_list]

wstr = " "
wstr = " "
for i in range(len(comment_list)):
    for j in range(len(comment_list[i])):
        wstr += comment_list[i][j]
        wstr += " "

text_file = open("wstr.txt", "w", encoding='UTF-8')
n = text_file.write(wstr)
text_file.close()
print('saved file')
