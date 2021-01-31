import scrapy
from scrapy.spiders import CrawlSpider, Rule
from ..items import Book
from scrapy.linkextractors import LinkExtractor


class BooksSpider(CrawlSpider):
    name = "books"
    allowed_domains = ['books.toscrape.com']
    start_urls = ["http://books.toscrape.com/"]
    rules = [
        Rule(LinkExtractor(allow='http://books.toscrape.com/catalogue/', 
                            restrict_xpaths="//*[@id='default']/div/div/div/div/section/div[2]/ol", 
                            unique=True,
                            ),
                    callback="parse_book"),
        Rule(LinkExtractor(allow='http://books.toscrape.com/',
                                restrict_xpaths="//*[@id='default']/div/div/div/div/section/div[2]/div/ul",
                            )
                        )
    ]

    def start_requests(self):
        urls = [
            'http://books.toscrape.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url,
                                callback=self.parse
                                )

    def parse_book(self, response):
        domain = "http://books.toscrape.com/"
        if response.xpath("//*[@id='content_inner']/article/div[1]/div[2]/h1/text()").extract():
            domain = "http://books.toscrape.com/"
            tool_item = Book()
            tool_item['title_book'] = response.xpath("//*[@id='content_inner']/article/div[1]/div[2]/h1/text()").extract()[0]
            # Get the image URL
            url_image_relative = response.xpath("//*[@id='product_gallery']/div/div/div/img/@src").extract()[0]
            tool_item['image_urls'] = [response.urljoin(url_image_relative)]
            yield tool_item
        else:
            print("\n\n\n\nNot found book\n\n\n\n")

    def parse(self, response):
        relative_url_first_page = response.xpath("//*[@id='default']/div/div/div/div/section/div[2]/div/ul/li[2]/a/@href").extract()
        if relative_url_first_page:
            yield scrapy.Request(url = response.url + relative_url_first_page[0])
        
        
    def errback(self, failure):
        print("\n\n\n")
        print(failure.request.url)
        print("\n\n\n")