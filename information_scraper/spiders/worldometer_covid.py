import scrapy

from scrapy_playwright.page import PageMethod
import json

class WorldometerCovidSpider(scrapy.Spider):
    name = "worldometer_covid"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/coronavirus/"]
    countries = json.load(open("countries.json"))

    def start_requests(self):
        urls = [
        ]
        yield scrapy.Request(
            url="https://www.worldometers.info/coronavirus/",
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
        # yield{
        #     "response": response.xpath('').extract()
        # }
        for row in response.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr[@role]'):

            current_rows = row.css("td")
            country_name = current_rows[1].css("a::text").get()
            date = response.css(".news_date ::text").get()
            total_cases = current_rows[2].css("::text").get()
            active_cases = current_rows[8].css("::text").get()
            deaths = current_rows[4].css("::text").get()

            id = 1
            country_name_to_id = {country['name']: country['id'] for country in self.countries}
            country_id = country_name_to_id.get(country_name)
            if country_id:
                yield {
                    "country_id": country_id,
                    "country_name": country_name,
                    "date_recorded": date,
                    "total_cases": total_cases,
                    "active_cases": active_cases,
                    "deaths": deaths.strip()
                }
                id += 1