
from lxml import html
import requests
import re

aircraft_links = []
aircraft_data = []

address_stub = "https://www.doc8643.com"

page = requests.get("https://www.doc8643.com/aircrafts", headers={'User-Agent': 'Mozilla/5.0'})
# print(page)

tree = html.fromstring(page.content)
links = tree.xpath('//a/@href')

def remove_extra_links(list_object, value):
    while value in list_object:
        links.remove(value)
    return links

for i in range(2, 53):
    address = address_stub + "/aircrafts/" + str(i)
    page = requests.get(address, headers={'User-Agent': 'Mozilla/5.0'})
    tree = html.fromstring(page.content)
    more_links = tree.xpath('//a/@href')
    links = links + more_links

# print(f"links is {links}")

unnecessary_pages = ['/index', '/news', '/aircrafts', '/gallery', '/faq', '/contact']

for i in unnecessary_pages:
    aircraft_links_prelim = remove_extra_links(links, i)

pattern = "/aircrafts.*"

for i in aircraft_links_prelim:
    result = re.findall(pattern, i)
    if result:
        result = result
    else:
        aircraft_links.append(i)

# print(aircraft_links)

# looking to match https://www.doc8643.com/aircraft/A002
for i in aircraft_links:
    aircraft_page = requests.get(address_stub + str(i), headers={'User-Agent': 'Mozilla/5.0'})
    aircraft_tree = html.fromstring(aircraft_page.content)
    codes = aircraft_tree.xpath('//td/h1')
    code_values = [code.text_content() for code in codes]
    code_values = code_values[0:2]

    pobs = aircraft_tree.xpath('//div/div/div')
    pob_values = [pob.text_content() for pob in pobs]

    pob_values = pob_values[27:29]
    code_values = code_values + pob_values

    aircraft_data.append(code_values)

print(aircraft_data)