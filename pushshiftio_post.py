import math
import json
import requests
import itertools
import numpy as np
import time
import pickle
import tqdm

from datetime import datetime, timedelta
print('import complete')

def make_request(uri, max_retries = 5):

    def fire_away(uri):
        response = requests.get(uri)
        assert response.status_code == 200
        return json.loads(response.content)
    current_tries = 1
    while current_tries < max_retries:
        try:
            time.sleep(1)
            response = fire_away(uri)
            return response
        except:
            time.sleep(1)
            current_tries += 1
    return fire_away(uri)


def pull_posts_for(subreddit, start_at, end_at):

    def map_posts(posts):
        return list(map(lambda post: {
            'id': post['id'],
            'created_utc': post['created_utc'],
            'permalink': post['permalink'],
        }, posts))

    SIZE = 100 # maximum request amount to pushshift.io at once
    URI_TEMPLATE = r'https://api.pushshift.io/reddit/search/submission/?subreddit={}&after={}&before={}&limit={}&fields=id,created_utc,permalink'

    post_collections = map_posts( \
        make_request( \
            URI_TEMPLATE.format( \
                subreddit, start_at, end_at, SIZE))['data'])
    n = len(post_collections)
    while n == SIZE:
        time.sleep(1)
        last = post_collections[-1]
        new_start_at = last['created_utc'] - (10)

        more_posts = map_posts( \
            make_request( \
                URI_TEMPLATE.format( \
                    subreddit, new_start_at, end_at, SIZE))['data'])

        n = len(more_posts)
        post_collections.extend(more_posts)

    # remove duplicates
    res = []
    [res.append(x) for x in post_collections if x not in res]

    return res

############################################################################################################

days = 3
subreddit = 'citiesskylines'
end_at = math.ceil(datetime.utcnow().timestamp())
start_at = math.floor((datetime.utcnow() - \
                       timedelta(days=days)).timestamp())
print(f'from {start_at} to {end_at}, {days} days @ r/{subreddit}')

posts = pull_posts_for(subreddit, start_at, end_at)

print(len(posts))

f = open("./data/post_filtered_pickle", "wb")
pickle.dump(posts, f)
f.close()
