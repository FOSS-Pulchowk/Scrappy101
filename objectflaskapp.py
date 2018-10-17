from flask import Flask, render_template, request
from objectwebsite import Website

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("input.html")


@app.route("/price", methods=["POST"])
def price():
    item_name = request.form.get("name")
    websites = []
    websites.append(Website(url= "https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=" + item_name,
                            name="Amazon.in"))
    websites.append(Website(url= "https://www.flipkart.com/search?q=" + item_name, name="Flipkart.com"))

    for x in websites:
        x.loadinfo()

    amazon_block = websites[0].soup.select("div.a-fixed-left-grid-col.a-col-right")
    if not len(amazon_block):
        amazon_block = websites[0].soup.find_all("div", class_="s-item-container")

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
        websites[0].set.append((name, price))

    flipkart_block = websites[1].soup.find_all("div", class_="_1UoZlX")
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

            websites[1].set.append((name + " " + a, price))


    else:
        flipkart_block = websites[1].soup.find_all("div", class_="_3liAhj _1R0K0g")
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
            websites[1].set.append((name + " " + a, price))

    for x in websites:
        x.sortalpha()

    return render_template("price.html", amazon=websites[0].set, flipkart=websites[1].set, amazon_url=websites[0].url,
                           flipkart_url=websites[1].url)


if __name__ == "__main__":
    app.run(debug=True)
