from bs4 import BeautifulSoup
import requests

url = []
paragraphs = []
texts = []
paragraphBuf = ''

url.append(requests.get("https://habr.com/ru/post/335136/").content)
url.append(requests.get("http://wiki.amperka.ru/slot-box:three-automatic-animal-feeder").content)
url.append(requests.get("http://www.electronica52.in.ua/proekty-arduino/avtomaticheskaya-kormushka-dlya-zhivotnyh-na-esp8266-iot-i-blynk-").content)


for item in url:
    html = BeautifulSoup(item, 'lxml')
    html = html.find_all('p')
    paragraphs.append(html)

for i in range(len(paragraphs)):
    for paragraph in paragraphs[i]:
        paragraphBuf = paragraphBuf + (paragraph.get_text().replace('"','-'))
        if len(paragraph.get_text()) > 2:
            if len(paragraphBuf) > 150:
                texts.append(paragraphBuf)
                paragraphBuf = ''
