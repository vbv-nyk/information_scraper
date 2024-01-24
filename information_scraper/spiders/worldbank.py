import time

import json
import scrapy
from scrapy_playwright.page import PageMethod
# GDP(gdp_id, country_id, year, value)

class WorldbankSpider(scrapy.Spider):
    name = "worldbank"
    allowed_domains = ["data.worldbank.org"]
    countries = json.load(open("countries.json"))

    def start_requests(self):
        urls = [
        ]
        for i in range(2010, 2022):
            urls.append(f"https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?end={i+1}&name_desc=false&start={i}")

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta=dict(
                    playwright=True,
                    playwright_include_page=False,
                    playwright_page_coroutines=[
                        PageMethod("wait_for_load_state", "load"),
                    ]
                )
            )

    def parse(self, response):
        id = 1


        for country in response.xpath('//div[@class="item"]'):
            country_name = country.css(".country-name").xpath("text()").get()
            country_name_to_id = {country['name']: country['id'] for country in self.countries}
            country_id = country_name_to_id.get(country_name.strip())

            if country_id:
                yield {
                    "id": id,
                    "country_id": country_id,
                    "name": country_name,
                    "year": country.css("div")[2].xpath("text()").get(),
                    "value": country.css("div")[3].xpath("text()").get()
                    }
                id += 1

