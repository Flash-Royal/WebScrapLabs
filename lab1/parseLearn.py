from bs4 import BeautifulSoup
import requests

url = []
paragraphs = []
texts = []

strText = ''
url.append(requests.get("https://wiki.briefly.ru/Ночной_Дозор_(Лукьяненко)").content)
url.append(requests.get("https://briefly.ru/strugackie/piknik_na_obochine").content)
url.append(requests.get("https://www.mirf.ru/book/majkl-suenvik-mat-zheleznogo-drakona/").content)
url.append(requests.get("https://briefly.ru/tolkien/vlastelin_kolec/").content)
url.append(requests.get("https://tesall.ru/tutorials/mir-witcher/1180-spoileri").content)
url.append(requests.get("https://meduza.io/feature/2016/08/01/ves-garri-potter-maksimalno-korotko").content)
url.append(requests.get("http://sochinite.ru/kratkie-soderzhaniya/raznye-avtory/chernovik").content)


for item in url:
    html = BeautifulSoup(item, 'lxml')
    html = html.find_all('p')
    paragraphs.append(html)

for i in range(len(paragraphs)):
    for paragraph in paragraphs[i]:
        if len(paragraph.get_text()) > 10:
                texts.append((((paragraph.get_text().replace('\xa0',' ')).replace('\n', '')).replace('\t', '')).replace('"','-'))
