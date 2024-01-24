import time
import json
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy_playwright.page import PageMethod

# GDP(gdp_id, country_id, year, value)

class WorldometerSpider(scrapy.Spider):
    name = "worldometer"
    allowed_domains = ["www.worldometers.info"]

    countries = json.load(open("countries.json"))
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        for country in response.css('tr td a'):
            yield scrapy.Request("https://www.worldometers.info"+country.css("::attr('href')").get(), self.load_country_data_parse, meta={
                'name': country.css("::text").get()
            })



    def load_country_data_parse(self, response):
        id = 1
        country_name_to_id = {country['name']: country['id'] for country in self.countries}

        country_id = country_name_to_id.get(response.meta['name'])

        for rows in response.xpath("/html/body/div[2]/div[3]/div/div/div[5]/table/tbody").css("tr"):
            if country_id:
                yield {
                    "population_id": id,
                    "year": rows.css("tr td::text")[0].get(),
                    "country_id": country_id,
                    "country_name": response.meta['name'],
                    "population": rows.css("td strong::text").get(),
                    "population_density": rows.css("td::text")[7].get()
                }
                id += 1


