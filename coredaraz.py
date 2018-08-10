from bs4 import BeautifulSoup as BS
import requests

daraz_url = "https://www.daraz.com.np/catalog/?q="
item_name = input("Enter an item to search: ")

daraz_url += item_name

daraz_page = requests.get(daraz_url).text

daraz_soup = BS(daraz_page,"html5lib")

daraz_set = []
count = 0
for name, price in zip(daraz_soup.find_all("span", class_="name"), daraz_soup.find_all("span", class_="price ")):

    if not name.text.startswith(item_name):
        break
    daraz_set.append((name.text, price.find_all("span")[-1].text[1:]))
    count += 1

daraz_set.sort()
print("Daraz: ")
for x in daraz_set:
    print("%s -------> Rs.%s" % (x[0], x[1]))
    print()
