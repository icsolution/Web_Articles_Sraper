import requests
import string
import os
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self):
        self.source_url = 'https://www.nature.com'
        self.number_pages = int(input())
        self.type = input()
        self.scrape_pages()

    def scrape_pages(self):
        main_directory = os.getcwd()
        for number in range(1, self.number_pages + 1):
            os.mkdir(f'Page_{number}')
            os.chdir(f'Page_{number}')
            url = self.source_url + '/nature/articles?searchType=journalSearch&sort=PubDate&page=' + str(number)
            parse = BeautifulSoup(self.get_page(url).text, 'html.parser')
            articles = parse.find_all('li', class_='app-article-list-row__item')
            for article in articles:
                article_type = article.find('span', class_="c-meta__type").text
                if article_type == self.type:
                    title = self.file_title(article.a.text)
                    body = self.file_body(article.a['href'])
                    print(body)
                    with open(f'{title}.txt', 'wb') as file:
                        file.write(body)
            os.chdir(main_directory)

    @staticmethod
    def get_page(url):
        return requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})

    @staticmethod
    def file_title(title):
        return title.translate(title.maketrans(' ', '_', string.punctuation))

    def file_body(self, link):
        url = self.source_url + link
        source = self.get_page(url).text
        try:
            text = BeautifulSoup(source, 'html.parser').find('div', class_="article-item__body").text
            return text.strip().replace('\n', '').encode()
        except:
            text = BeautifulSoup(source, 'html.parser').find('div', class_="c-article-body u-clearfix").text
            return text.strip().replace('\n', '').encode()


Scraper()

