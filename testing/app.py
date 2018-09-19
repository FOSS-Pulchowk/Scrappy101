from flask import Flask, render_template, request
from bs4 import BeautifulSoup as BS
import requests


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("input.html")

@app.route("/price", methods=["POST"])
def price():
    item_name = request.form.get("name")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"}
    amazon_url = "https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="
    flipkart_url = "https://www.flipkart.com/search?q="

    amazon_url += item_name
    flipkart_url += item_name

    print("\nLoading Amazon.in..........")
    amazon_page = requests.get(amazon_url, headers=headers).text
    print("Done!!\n")

    print("Loading Flipkart.com")
    flipkart_page = requests.get(flipkart_url, headers=headers).text
    print("Done!!\n")

    amazon_soup = BS(amazon_page, "html5lib")
    flipkart_soup = BS(flipkart_page, "html5lib")

    amazon_set = []
    flipkart_set = []

    amazon_block = amazon_soup.select("div.a-fixed-left-grid-col.a-col-right")
    if not len(amazon_block):
        amazon_block = amazon_soup.find_all("div", class_="s-item-container")

    for block in amazon_block:
        if block.find("span", class_="a-color-price") is None:
            continue

        try:
            price = float("".join(block.find("span", class_="a-color-price").text[2:].split(",")))
        except:
            continue
        name = block.find("h2").text
        if item_name.lower() not in name.lower() or price < 500:
            continue
        amazon_set.append((name, price))

    flipkart_block = flipkart_soup.find_all("div", class_="_1UoZlX")
    if len(flipkart_block):
        for block in flipkart_block:
            if block.find("div", class_="_1vC4OE _2rQ-NK") is None:
                continue
            try:
                price = float("".join(block.find("div", class_="_1vC4OE _2rQ-NK").text[1:].split(",")))
            except:
                continue

            name = block.find("div", class_="_3wU53n").text
            if item_name.lower() not in name.lower() or price < 500:
                continue
            a = ""
            if block.find("span", class_="_1GJ2ZM") is not None:
                a = block.find("span", class_="_1GJ2ZM").text

            flipkart_set.append((name + " " + a, price))


    else:
        flipkart_block = flipkart_soup.find_all("div", class_="_3liAhj _1R0K0g")
        for block in flipkart_block:
            if block.find("div", class_="_1vC4OE") is None:
                continue
            name = block.find("a", class_="_2cLu-l").text
            try:
                price = float("".join(block.find("div", class_="_1vC4OE").text[1:].split(",")))
            except:
                continue

            if item_name.lower() not in name.lower() or price < 500:
                continue

            a = ""
            if block.find("span", class_="rIHMVr") is not None:
                a = block.find("span", class_="rIHMVr").text
            flipkart_set.append((name + " " + a, price))

    if len(amazon_set):
        amazon_set = list(set(amazon_set))
        amazon_set.sort()

    if len(flipkart_set):
        flipkart_set = list(set(flipkart_set))
        flipkart_set.sort()
    
    return render_template("price.html",amazon=amazon_set, flipkart=flipkart_set, amazon_url=amazon_url, flipkart_url=flipkart_url)

if __name__ == "__main__":
    app.run(debug=True)
