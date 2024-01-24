import scrapy
from scrapy_playwright.page import PageMethod
import json
# Population(population_id, country_id, year, total_population, population_density)

class TradingeconomicsSpider(scrapy.Spider):
    name = "tradingeconomics"
    allowed_domains = ["tradingeconomics.com"]
    start_urls = ["https://www.worldometers.info/coronavirus/"]
    countries = json.load(open("countries.json"))

    def start_requests(self):

        yield scrapy.Request(
            url="https://tradingeconomics.com/country-list/inflation-rate?continent=world",
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
        # Czechia
        for rows in response.xpath("//tbody/tr"):
            country_name = rows.xpath("td/a/text()").get()
            inflat_rate = rows.xpath("td/text()")[1].get()

            if country_name == "Czech Republic":
                country_name = "Czechia"



            country_name_to_id = {country['name']: country['id'] for country in self.countries}
            country_id = country_name_to_id.get(country_name.strip())

            if(inflat_rate == '%'):
                inflat_rate = rows.xpath("td/span/text()")[0].get()

            if country_id:
                yield {
                    "economic_id": id,
                    "country_name" : country_name.strip(),
                    "inflat_rate": inflat_rate,
                    "country_id": country_id
                }
                id += 1
