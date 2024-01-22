import scrapy
from scrapy_playwright.page import PageMethod
import json

# Population(population_id, country_id, year, total_population, population_density)

class WorlddataSpider(scrapy.Spider):
    name = "worlddata"
    allowed_domains = ["www.worlddata.info"]
    countries = json.load(open("countries.json"))

    def start_requests(self):
        urls = []

        yield scrapy.Request(
            url="https://www.worlddata.info/unemployment-rates.php",
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
        rows = response.xpath('//tbody/tr')
        for row in rows:
            country_name = row.xpath("td/a/text()").get()
            if(not country_name):
                continue

            unemp_rate = row.xpath("td/text()").get()
            country_name_to_id = {country['name']: country['id'] for country in self.countries}
            country_id = country_name_to_id.get(country_name.strip())

            yield {

                "country_id": country_id,
                "unemp_rate": unemp_rate
            }