from gensim.models import Word2Vec

model = Word2Vec.load("word2vec.model")
word = model.wv.most_similar(positive = ['гарри', 'кольцо'], negative = ['шар'])
print(word)
