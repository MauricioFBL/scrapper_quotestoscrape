from typing import get_args
import scrapy


class QuotesDpider(scrapy.Spider):
    title_u = ''
    tags_t = []
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/'
    ]
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FROMAT': 'json',
        'CONCURRENT_REQUESTS':24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['maufbl10@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'PEPE',
        'FEED_EXPORT_ENCODING': 'utf-8',
        # 'CLOSESPIDER_PAGECOUNT': # Un poco alto
    }


    def parse_quotes_authors(self, response, **kwargs):
        if kwargs:
            list_full = list(kwargs['quotes'])
            quotes = (response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())
            authors = (response.xpath('//small[@class="author" and @itemprop="author"]/text()').getall())
            list_qa = [({'quote':quote, 'author':author}) for quote,author in zip(quotes,authors)]
            list_full = list_full + list_qa
        next_page_link = response.xpath(
            '//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        if next_page_link:
            yield response.follow(
                next_page_link, callback=self.parse_quotes_authors,
                cb_kwargs={
                    'quotes':list_full
                }
            )
        else:
            yield {
                'Title':self.getTitle(),
                'Top tgs':self.getTags(),
                'quotes':list_full
            }

    def parse(self, response):
        print('*' * 10)
        print('\n\n')
        # print(response.status, response.headers)
        title = response.xpath('//h1/a/text()').get()
        print(f'Titulo: {title}')
        quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        authors = response.xpath(
            '//small[@class="author" and @itemprop="author"]/text()').getall()
        list_qa = [({'quote':quote, 'author':author}) for quote,author in zip(quotes,authors)]
        tags = response.xpath(
            '//div[contains(@class,"tags-box")]//span[@class = "tag-item"]/a/text()').getall()
        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            tags = tags[:top]
        print('\n\n')
        print('*' * 10)
        self.setTags(tags)
        self.setTitle(title)
        next_page_link = response.xpath(
            '//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        if next_page_link:
            yield response.follow(
                next_page_link, callback = self.parse_quotes_authors,
                cb_kwargs={
                    'quotes':list_qa
                }
            )
    
    def setTags(self,tags):
        self.tags_t = tags
        
    def getTags(self):
        return self.tags_t

    def setTitle(self,title):
        self.title_u = title
        
    def getTitle(self):
        return self.title_u

# scrapy crawl quotes -o quotes.json
# scrapy crawl quotes -o quotes.json
# scrapy crawl quotes -a top=4
