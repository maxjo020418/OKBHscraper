from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
import collections
import re

file = open("wstr.txt", 'r', encoding = 'utf-8')
t = file.read()
t = t.replace('iry', 'irys').replace('kronius', 'kronii').replace('chao', 'chaos').replace('rusium', '').replace('artium', 'artia') \
.replace('matsurus', 'matsuri').replace('youtu', 'youtube').replace('segg', 'seggs').replace('kis', 'kiss').replace('retar', 'retard').replace('suipis', 'suipiss') \
.replace('kryptonh', '').replace('subject', '').replace('feedback', '').replace('savevideo', '').replace('u/', '').replace('link', '').replace('alway', 'always') \
.replace('content', '').replace('info', '').replace('view', '').replace('donate', '').replace('dmca', '').replace('removal', '').replace('request', '')
t = re.sub(r'url\=\/([a-zA-Z0-9_]+(\/[a-zA-Z0-9_]+)+)', '', t)
t = re.sub(r'v\=([a-zA-Z0-9_]+)', '', t)
t = re.sub(r't\=([a-zA-Z0-9_]+)', '', t)
t = t.replace('=', '').replace('v=', '').replace('t=', '')
file.close()

t = t.split()

glist = list()
for i in range(len(t)):
    if t[i].isalpha():
        glist.append(i)

ct = list()
for i in glist:
    ct.append(t[i])

print(ct)
ctdict = collections.Counter(ct)
ctdict = dict(sorted(ctdict.items(), key=lambda item: item[1], reverse = True))

text_file = open("rank.txt", "w", encoding='UTF-8')
for key, value in ctdict.items():
    text_file.write(str(key + ' : ' + str(value) + '\n'))
text_file.close()

ct = '\n'.join(ct)

###################################################################

mask = np.array(Image.open('Hololive_logo.png'))

####################################################################

#width = 50000, height = 50000,

wordcloud = WordCloud(random_state=1,
                      width = 10000, height = 10000,
                      background_color='black',
                      collocations=False,
                      mask = mask,
                      max_words = 1000
                      ).generate(ct)


# Plot
image_colors = ImageColorGenerator(mask)
plt.figure(figsize=[10,10])
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.savefig('wordcloud.png', dpi=2400)
plt.show()
