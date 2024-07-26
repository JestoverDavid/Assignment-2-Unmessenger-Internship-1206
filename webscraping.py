import scrapy

class ImdbSpiderSpider(scrapy.Spider):
    name = "imdb_spider"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={'User-Agent': self.user_agent}, callback=self.parse)

    def parse(self, response):
        rows = response.css('table.chart.full-width tr')

        for row in rows:
            title = row.css('td.titleColumn a::text').get()
            year = row.css('td.titleColumn span.secondaryInfo::text').get()
            rating = row.css('td.imdbRating strong::text').get()

            if title and year and rating:
                yield {
                    'title': title,
                    'year': year.strip('()'),
                    'rating': rating
                }
