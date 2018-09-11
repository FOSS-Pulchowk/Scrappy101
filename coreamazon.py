from bs4 import BeautifulSoup as BS
import requests
headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"}
amazon_url = "https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="
item_name = input("Enter an item to search: ")

amazon_url += item_name

amazon_page = requests.get(amazon_url, headers=headers).text

amazon_soup = BS(amazon_page,"html5lib")

amazon_set = []
amazon_block=amazon_soup.select("div.a-fixed-left-grid-col.a-col-right")
if not len(amazon_block):
    amazon_block=amazon_soup.find("div",class_="s-item-container")

for block in amazon_block:
    try:
        price=int("".join(block.find("span", class_="a-color-price").text[2:].split(",")))
    except:
        continue
    name=block.find("h2").text
    if item_name.lower() not in name.lower() or price<200 :
        continue
    amazon_set.append((name, price))

print("Amazon: ")
if len(amazon_set):
    amazon_set = list(set(amazon_set))
    amazon_set.sort()
    for x in amazon_set:
        print("%s -------> Rs.%s" % (x[0], x[1]))
        print()
else:
    print("Sorry, we couldn't find it in Amazon.in")