import scrapy
from scrapy_playwright.page import PageMethod
import json



class WorldbankHealthexpSpider(scrapy.Spider):
    name = "worldbank_healthexp"
    allowed_domains = ["data.worldbank.org"]
    start_urls = ["https://data.worldbank.org/indicator/SH.XPD.CHEX.GD.ZS?end=2021"]
    countries = json.load(open("countries.json"))

    def start_requests(self):

        yield scrapy.Request(
            url="https://data.worldbank.org/indicator/SH.XPD.CHEX.GD.ZS?end=2021",
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
                    "value": country.css("div")[3].xpath("text()").get()
                }
                id += 1


