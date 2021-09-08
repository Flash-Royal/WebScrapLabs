import re
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import nltk
from mysql.connector import connect, Error
import gensim
import matplotlib.pyplot as plt
from gensim import corpora
import matplotlib.pyplot as plt
import pyLDAvis.gensim_models
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors
from gensim.models.ldamulticore import LdaMulticore
from multiprocessing import Process, freeze_support
from gensim.models.coherencemodel import CoherenceModel

userName = 'root'
userPassword = '1234'

def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    """
    Подсчет c_v когерентности для различного количества тем
    dictionary : Gensim словарь
    corpus : Gensim корпус
    texts : Список текста
    limit : Максимальное количество тем
    model_list : Список LDA моделей
    coherence_values :Когерентности, соответствующие модели LDA с количеством тем
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model=LdaMulticore(corpus=corpus,id2word=dictionary, num_topics=num_topics)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
    return model_list, coherence_values



def lemmatize(doc):
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            if token not in stopwords_en:
                tokens.append(token)
    if len(tokens) > 2:
        return tokens
    return None


if __name__ == '__main__':

    cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]

    try:
        with connect(
            host = "localhost",
            user = userName,
            password = userPassword,
            database = "ips2",
        ) as connection:
            eventsTable = """
                select textD from ips2.Texts
            """

            with connection.cursor() as cur:
                cur.execute(eventsTable)
                result = cur.fetchall()

    except Error as e:
        print(e)

    texts = []
    for item in result:
        texts.append(list(item))

    # print(texts)

    patterns = "[0-9!$#%!&'()\"+-/*<=>^?@[\]_`{|}~]"
    stopwords_en = stopwords.words("russian")

    stopwords_en.extend(['а','к','для','и','прямо','в','не','с','через','как','он','она','они','что','где'])

    morph = MorphAnalyzer()

    # print(texts)
    data = []
    for text in texts:
        # print(text[0])
        data.append(lemmatize(text[0]))

    # print(data)

    id2word = corpora.Dictionary(data)
    corpus = [id2word.doc2bow(text) for text in data]
    ldaModel1 = gensim.models.ldamodel.LdaModel(corpus = corpus, id2word = id2word, num_topics = 5, random_state = 100, update_every = 1, chunksize = 10, passes = 1, alpha = 'symmetric', per_word_topics = True)
    print(ldaModel1.print_topics())

    data1 = pyLDAvis.gensim_models.prepare(ldaModel1, corpus, id2word, mds = 'mmds')
    pyLDAvis.save_html(data1, 'lda.html')

    cloud = WordCloud(stopwords=stopwords_en,
    background_color='white',
    width=2500,
    height=1800,
    max_words=10,
    colormap='tab10',
    color_func=lambda *args, **kwargs: cols[i],
    prefer_horizontal=1.0)
    topics = ldaModel1.show_topics(formatted=False)
    fig, axes = plt.subplots(2, 2, figsize=(10,10), sharex=True, sharey=True)
    for i, ax in enumerate(axes.flatten()):
        fig.add_subplot(ax)
        topic_words = dict(topics[i][1])
        cloud.generate_from_frequencies(topic_words, max_font_size=300)
        plt.gca().imshow(cloud)
        plt.gca().set_title('Topic' + str(i), fontdict=dict(size=16))
        plt.gca().axis('off')
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.axis('off')
    plt.margins(x=0, y=0)
    plt.tight_layout()
    plt.show()

    freeze_support()
    model_list, coherence_values = compute_coherence_values(dictionary=id2word, corpus=corpus,
    texts=data, start=2, limit=10, step=2)
    #
    # for m, cv in zip(x, coherence_values):
    #     print("Num Topics =", m, " has Coherence Value of", round(cv, 10))

    limit=10; start=2; step=2;
    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Количество тем")
    plt.ylabel("Согласованность")
    plt.legend(("coherence_values"), loc='best')
    plt.show()
