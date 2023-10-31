import os
from gensim.models import Word2Vec

os.chdir(os.path.dirname(__file__))
# define your sentence corpus as a list of lists of words
corpus = [["I", "like", "apples"], ["She", "prefers", "oranges"],
          ["I", "love", "bananas"], ["He", "hates", "pineapples"]]

# define your Word2Vec model
model = Word2Vec(sentences=corpus, window=5, min_count=1, workers=4)

# check similarity between two words
similarity = model.wv.similarity('apples', 'bananas')
print("Similarity between 'apples' and 'bananas':", similarity)

# get the top 5 most similar words to a target word
similar_words = model.wv.most_similar('oranges', topn=5)
for word in similar_words:
    print(word)

model.save(os.path.join('models', 'test_model'))
model.wv.save_word2vec_format(os.path.join('models', 'word2vec_txt.txt'),
                              binary=False)
