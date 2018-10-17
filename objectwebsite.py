from bs4 import BeautifulSoup as BS
import requests


class Website:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"}
    def __init__(self, url, name):
        self.url=url.replace(" ", "%20")
        self.name=name
    def loadinfo(self):
        print("\nLoading %s " %self.name)
        self.page = requests.get(self.url, headers=self.headers).text
        print("Done!!")
        self.soup = BS(self.page, "html5lib")
        self.set=[]

    def printinfo(self):
        print("\n%s: " %self.name)
        if len(self.set):
            self.set = list(set(self.set))
            self.set.sort()
            for x in self.set:
                print("%s -------> Rs.%s" % (x[0], x[1]))
                print()
        else:
            print("Sorry, we couldn't find it in %s" %self.name)

    def sortalpha(self):
        if len(self.set):
            self.set = list(set(self.set))
            self.set.sort()


