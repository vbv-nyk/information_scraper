import scrapy
# Country(country_id, name, continent, code)

class StatisticstimesSpider(scrapy.Spider):
    name = "statisticstimes"
    allowed_domains = ["statisticstimes.com"]
    start_urls = ["https://statisticstimes.com/geography/countries-by-continents.php"]

    def parse(self, response):
        id = 1
        for row in response.css("#table_id tbody tr"):
            yield {
                "id": id,
                "name": row.css(".name").xpath("text()")[0].get(),
                "continent": row.css(".name").xpath("text()")[1].get(),
                "code": row.css(".data1").xpath("text()")[1].get(),
            }
            id += 1
