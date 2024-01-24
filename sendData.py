import requests
import json

# Specify the URL of your backend API
backend_url = "http://localhost:3000"

# Path to your JSON file
countriesJSON = "./information_scraper/spiders/countries.json"
covidJSON = "./information_scraper/spiders/covid.json"
gdpJSON = "./information_scraper/spiders/gdp.json"
healthExpJSON = "./information_scraper/spiders/health_exp.json"
inflationJSON = "./information_scraper/spiders/inflation_rate.json"
populationJSON = "./information_scraper/spiders/population.json"
unempJSON = "./information_scraper/spiders/unemp_rate.json"

# Open and read the JSON file
with open(countriesJSON, 'r') as file:
    countriesData = json.load(file)

# Open and read the JSON file
with open(covidJSON, 'r') as file:
    covidData = json.load(file)

# Open and read the JSON file
with open(gdpJSON, 'r') as file:
    gdpData = json.load(file)

# Open and read the JSON file
with open(healthExpJSON, 'r') as file:
    healthExpData = json.load(file)

# Open and read the JSON file
with open(populationJSON, 'r') as file:
    populationData = json.load(file)

# Open and read the JSON file
with open(inflationJSON, 'r') as file:
    inflationData = json.load(file)

# Open and read the JSON file
with open(unempJSON, 'r') as file:
    unempData = json.load(file)


# print(countriesData, covidData, gdpData, healthExpData, populationData, inflationData, unempData)
# Send a POST request with the JSON data


# Create a dictionary to store combined data
combinedData = {}

# Merge inflation data based on country_id
for item in inflationData:
    country_id = item['country_id']
    if country_id not in combinedData:
        combinedData[country_id] = {}
    combinedData[country_id]['country_name'] = item['country_name']
    combinedData[country_id]['unemployment_rate'] = '00'
    combinedData[country_id]['inflation_rate'] = float(item['inflat_rate'])

# Merge unemployment data based on country_id
for item in unempData:
    country_id = item['country_id']
    unemp_rate_str = item['unemp_rate'].strip('%')

    if country_id in combinedData:
        combinedData[country_id]['unemployment_rate'] = unemp_rate_str


# Print or use combinedData as needed
# for country_id, data in combinedData.items():
#     print(
#         f"Country ID: {country_id}, Country Name: {data['country_name']}, Inflation Rate: {data['inflation_rate']}, Unemployment Rate: {data.get('unemployment_rate', 'N/A')}")


# Set the headers to indicate JSON data
headers = {'Content-Type': 'application/json'}

countriesData = json.dumps(countriesData)
covidData = json.dumps(covidData)
gdpData = json.dumps(gdpData)
healthData = json.dumps(healthExpData)
ecData = json.dumps(combinedData)
populationData = json.dumps(populationData)

print(populationData)
# Send a POST request to the Node.js server
response = requests.post(backend_url + '/insertCountries', data=countriesData, headers=headers)
print(response)
response = requests.post(backend_url + '/insertEC', data=ecData, headers=headers)
print(response)
response = requests.post(backend_url + '/insertCovid', data=covidData, headers=headers)
print(response)
response = requests.post(backend_url + '/insertPopulation', data=populationData, headers=headers)
print(response)
response = requests.post(backend_url + '/insertGDP', data=gdpData, headers=headers)
print(response)

response = requests.post(backend_url + '/insertHC', data=healthData, headers=headers)
print(response)

