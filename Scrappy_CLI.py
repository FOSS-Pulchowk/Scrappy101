from objectwebsite import Website

websites=[]
websites.append(Website(url="https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=", name="Amazon.in"))
websites.append(Website(url="https://www.flipkart.com/search?q=", name="Flipkart.com"))

item_name = input("Enter an item to search: ")

for x in websites:
    x.loadinfo(item_name)

amazon_block=websites[0].soup.select("div.a-fixed-left-grid-col.a-col-right")
if not len(amazon_block):
    amazon_block=websites[0].soup.find_all("div",class_="s-item-container")

for block in amazon_block:
    if block.find("span", class_="a-color-price") is None:
        continue
    price=float("".join(block.find("span", class_="a-color-price").text[2:].split(",")))
    name=block.find("h2").text
    if item_name.lower() not in name.lower() or price<5000 :
        continue
    websites[0].set.append((name, price))



flipkart_block = websites[1].soup.find_all("div", class_="_1UoZlX")
if len(flipkart_block):
    for block in flipkart_block:
        if block.find("div", class_="_1vC4OE _2rQ-NK") is None:
            continue
        price = float("".join(block.find("div", class_="_1vC4OE _2rQ-NK").text[1:].split(",")))

        name=block.find("div", class_="_3wU53n").text
        if item_name.lower() not in name.lower() or price<5000 :
            continue
        a = ""
        if block.find("span", class_="_1GJ2ZM" ) is not None:
            a=block.find("span", class_="_1GJ2ZM" ).text

        websites[1].set.append((name + " " + a, price))


else:
    flipkart_block = websites[1].soup.find_all("div", class_="_3liAhj _1R0K0g")
    for block in flipkart_block:
        if block.find("div", class_="_1vC4OE") is None:
            continue
        name=block.find("a", class_="_2cLu-l").text
        price = float("".join(block.find("div", class_="_1vC4OE").text[1:].split(",")))
        if item_name.lower() not in name.lower() or price<5000:
            continue

        a = ""
        if block.find("span", class_="rIHMVr" ) is not None:
            a=block.find("span", class_="rIHMVr" ).text
        websites[1].set.append((name + " " + a, price))

for x in websites:
    x.printinfo()