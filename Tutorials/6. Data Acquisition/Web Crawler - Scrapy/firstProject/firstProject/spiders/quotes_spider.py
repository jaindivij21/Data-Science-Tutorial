import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"  # name of the spider

    def start_requests(self):
        # all the URLs to crawl
        urls = [
            'http://quotes.toscrape.com/page/1/',
        ]
        # generator that takes urls and gives back a response to the parse function
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # parse function that handles the reponse
    def parse(self, response):
        # get the page number from the URL (1,2,3,....)
        page = response.url.split("/")[-2]
        # create the filename with the page number, quotes-1.html, quotes-2.html, etc.
        filename = 'quotes-%s.html' % page

        # run a loop to get all the quotes, yield the response into a json file
        for q in response.css("div.quote"):
            text = q.css('span.text::text').get()
            author = q.css('small.author::text').get()
            tags = q.css('a.tag::text').getall()

            yield {
                'text': text,
                'author': author,
                'tags': tags,
            }   # TO RUN: > scrapy crawl quotes -o quotes.json

        # find the next page button to recursively scrape the entire website recursively
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
