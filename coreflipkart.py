from bs4 import BeautifulSoup as BS
import requests
headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"}
flipkart_url = "https://www.flipkart.com/search?q="

item_name = input("Enter an item to search: ")

flipkart_url += item_name

flipkart_page = requests.get(flipkart_url, headers=headers).text

flipkart_soup = BS(flipkart_page,"html5lib")

flipkart_set = []
flipkart_block = flipkart_soup.find_all("div", class_="_1UoZlX")
for block in flipkart_block:
    price = int("".join(block.find("div", class_="_1vC4OE _2rQ-NK").text[1:].split(",")))

    name=block.find("div", class_="_3wU53n").text
    if item_name.lower() not in name.lower() or price<5000 :
        continue
    a = ""
    if block.find("span", class_="_1GJ2ZM" ) is not None:
        a=block.find("span", class_="_1GJ2ZM" ).text

    flipkart_set.append((name + " " + a, price))

flipkart_set=list(set(flipkart_set))
flipkart_set.sort()
print("Flipkart: ")
print(len(flipkart_set))
for x in flipkart_set:
    print("%s -------> Rs.%s" % (x[0], x[1]))
    print()