import requests
from lxml import html
from datetime import datetime


class Parser:
    default_url = 'https://prometey.digital/blog/'
    card_xpath = '//div[@class="grid-container"]/a'
    detailed_date_xpath = '//div[@class="post-meta fs-14"]/span'
    detailed_title_xpath = '//div[@class="mt-auto"]/h1'

    def get_detailed(self):
        raw = requests.get(self.default_url).text
        root = html.fromstring(raw)
        return [e.attrib['href'] for e in root.xpath(self.card_xpath)]

    def follow(self, url):
        raw = requests.get(url).text
        root = html.fromstring(raw)

        title = root.xpath(self.detailed_title_xpath)[0].text.strip()
        date_published_str = root.xpath(self.detailed_date_xpath)[0].attrib['title']
        date_published = datetime.strptime(date_published_str, '%d.%m.%Y %H:%M')

        return {
            'title': title,
            'url': url,
            'date': date_published
        }


if __name__ == '__main__':
    p = Parser()
    urls = p.get_detailed()
    for u in urls:
        print(p.follow(u))
