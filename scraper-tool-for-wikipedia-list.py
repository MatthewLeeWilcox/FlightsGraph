# Scrapes the ICAO airline code and corresponding airline name from Wikipedia 
# April Ainsworth

from lxml import html
import requests
import re
import pandas as pd

aircraft_links = []
icao_codes_and_names = []

address_stub = "https://en.wikipedia.org/wiki/List_of_airline_codes"

page = requests.get("https://en.wikipedia.org/wiki/List_of_airline_codes", headers={'User-Agent': 'Mozilla/5.0'})
print(page)

tree = html.fromstring(page.content)

icao = tree.xpath('//tr/td[position()<4]')

for i in range(len(icao)):
    if i % 3 == 0: # compile and append at the beginning of every third element
        icao_short = icao[i:i+3] # make a list of three elements
        code_value = [code.text_content() for code in icao_short]
        icao_codes_and_names.append(code_value)

df = pd.DataFrame(icao_codes_and_names, columns = ['IATA_airline_code', 'ICAO_airline_code', 'airline_name']) 
df.to_pickle("icao_codes_and_names.pkl")