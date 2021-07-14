from bs4 import BeautifulSoup
import requests
from .models import Post
from django.contrib.auth.models import User


class Parser:
    def __init__(self):
        self.data = []

    def get_html(self, url):
        r = requests.get(url)
        return r.text

    def get_all_links(self):
        soup = BeautifulSoup(self.get_html('https://news.ycombinator.com/'), 'lxml')
        ads = soup.findAll('a', class_='storylink')
        for ad in ads:
            try:
                link = ad.get('href')
            except:
                print('Fail')
            try:
                title = ad.get_text(strip=True)
            except:
                print('Fail text')

            article = {
                'title': title,
                'link': link,
            }
            self.data.append(article)


def scrap():
    p = Parser()
    p.get_all_links()
    for d in p.data:
        try:
            Post.objects.create(
                title=d['title'],
                url=d['link'],
                creator=User.objects.get(id=1),
            )
        except:
            continue