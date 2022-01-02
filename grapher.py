import numpy as np
import matplotlib.pyplot as plt
import pickle

from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator

infile = open('./data/fdist', 'rb')
fdist = pickle.load(infile)
infile.close()

# remove unwanted keywords
KILL = ['http']
for k in KILL:
    try:
        del fdist[k]
    except:
        pass

mask = np.array(Image.open('./masks/Hololive_logo.png'))

wordcloud = WordCloud(random_state=1,
                      width = 10000, height = 10000,
                      background_color='black',
                      collocations=False,
                      mask = mask,
                      max_words = 1000
                      ).generate_from_frequencies(fdist)


# Plot
image_colors = ImageColorGenerator(mask)
plt.figure(figsize=[10,10])
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear") # wordcloud.recolor(color_func = lambda *args, **kwargs: "black") for single color
plt.axis("off")
plt.savefig('wordcloud.png', dpi=2500)
plt.show()
