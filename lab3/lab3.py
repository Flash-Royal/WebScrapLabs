from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser
from nltk.corpus import stopwords
import re
from pymorphy2 import MorphAnalyzer
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

url = []
paragraphs = []
texts = []

url.append("https://wiki.briefly.ru/Ночной_Дозор_(Лукьяненко)")
url.append("https://briefly.ru/strugackie/piknik_na_obochine")
url.append("https://www.mirf.ru/book/majkl-suenvik-mat-zheleznogo-drakona/")
url.append("https://briefly.ru/tolkien/vlastelin_kolec/")
url.append("https://wiki.briefly.ru/Последнее_желание_(Сапковский)")
url.append("https://meduza.io/feature/2016/08/01/ves-garri-potter-maksimalno-korotko")
url.append("http://sochinite.ru/kratkie-soderzhaniya/raznye-avtory/chernovik")
url.append("https://kinopoduglom.ru/vampiry/sergej-lukyanenko-dnevnoj-dozor")
url.append("https://libking.ru/books/poetry-/dramaturgy/142938-arkadiy-i-boris-strugatskie-stalker.html")
# url.append("https://kratkoe.com/hroniki-narnii-kratkoe-soderzhanie/")

print('Чтение страниц...')
for item in tqdm(url):
    item = requests.get(item).content
    html = BeautifulSoup(item, 'lxml')
    html = html.find_all('p')
    paragraphs.append(html)

for i in range(len(paragraphs)):
    for paragraph in paragraphs[i]:
        if len(paragraph.get_text()) > 10:
                texts.append(((paragraph.get_text().replace('\xa0',' ')).replace('\n', '')).replace('\t', ''))



def lemmatize(paragraph):
    paragraph = re.sub(patterns,' ', str(paragraph))
    tokens = []
    for token in paragraph.split():
        if token:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            if token not in stopwords_ru:
                tokens.append(token)
    if len(tokens) > 2:
        return tokens
    return None

patterns = "[A-Za-z0-9!#$%&';()*+,./:;<=>?@[\]«»^_`{|}~—\";\-·©]"
stopwords_ru = stopwords.words('russian')

morph = MorphAnalyzer()
data_ready = []

print('Преобразование параграфов...')
for item in tqdm(texts):
    data_ready.append(lemmatize(item))
data_ready = list(filter(None, data_ready))


phrases = Phrases(data_ready, min_count=30, progress_per=10000)
bigram = Phraser(phrases)
sentences = bigram[data_ready]




model = Word2Vec(    min_count=5,
                     vector_size=1000,
                     alpha=0.03,
                     min_alpha=0.0007,
                     negative=20,
                     workers=8)
print('Обучение сети...')
model.build_vocab(sentences, min_count=1)  # prepare the model vocabulary
model.train(sentences, total_examples=model.corpus_count, epochs=200, report_delay=1)
model.save("word2vec.model")
print('Сеть обучена')
# print(model.prepare_weights())
