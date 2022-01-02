# OKBHscraper

Originally made as a joke project for r/okbuddyhololive

###### packages needed(pip)
- numpy
- pandas
- pickle
- praw
- termcolor
- nltk
- sklearn
- tqdm
- requests

Download [WordCloud](https://github.com/amueller/word_cloud) directly into OKBHscraper NOT using pip.

###### how to use
(you don't need to use the `_old.py` files, `gephi_csv.py` and `reducer.py`)
1. specify subreddit and the len of time form now to scrape in `pushshiftio_post.py`
2. place your reddit API key in `comment_fetcher.py`
3. first run `pushshiftio_post.py` and run `comment_fetcher.py`
4. if you want to use gephi use the `gephi.csv` inside the `data` folder
5. run `grapher.py` to make wordcloud graphs(it will also save an image fot that)
