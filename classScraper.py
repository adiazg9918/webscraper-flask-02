import csv
from bs4 import BeautifulSoup
from selenium import webdriver


class Scraper:

    def __init__(self, search_term):
        self.search_term = search_term.replace(' ', '+')
        self.driver = webdriver.Chrome()
        self.records = []

    def get_url(self):
        self.template = 'https://www.amazon.com.mx/s?k={}&__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_1'
        self.url = self.template.format(self.search_term)
        self.url += '&page={}'
        return self.url

    def navigate(self):
        self.driver.get(self.url)

    def extract_record(self, item):
        self.atag = item.h2.a
        self.description = self.atag.text.strip()
        self.url = 'https://www.amazon.com.mx' + self.atag.get('href')
        self.review_count = ''

        try:
            self.price_parent = item.find('span', 'a-price')
            self.price = self.price_parent.find('span', 'a-offscreen').text
        except AttributeError:
            return

        try:
            self.rating = item.i.text

        except AttributeError:
            self.rating = ''

        self.result = (self.description, self.price,
                       self.rating, self.url)

        return self.result

    def get_data(self):
        for page in range(1, 3):
            self.driver.get(self.url.format(page))
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            self.results = self.soup.find_all(
                'div', {'data-component-type': 's-search-result'})

            for item in self.results:
                self.record = self.extract_record(item)
                if self.record:
                    self.records.append(self.record)
        self.driver.close()

    def to_csv(self):
        with open('proxies.csv', 'w', encoding='UTF-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                ['Description', 'Price', 'Rating', 'Link'])
            writer.writerows(self.records)


if __name__ == '__main__':
    scraper = Scraper('alexa')
    scraper.get_url()
    scraper.navigate()
    scraper.get_data()
    scraper.to_csv()
