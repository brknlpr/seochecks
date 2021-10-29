from models.links import Link
from models.seochecks import SeoChecks
from advertools import sitemaps
from bs4.element import SoupStrainer
import requests
from bs4 import BeautifulSoup
import advertools as adv
import json

class Site():
    def __init__(self, site) -> None:
        self.sitemaps = []
        if site:
            advsitemap = adv.sitemap_to_df(site)
            for url in advsitemap["loc"]:
                self.sitemaps.append(url)

    def checkStatus(self, htmlResult):
        #for url in self.sitemaps:
        #status = requests.get(url)
        return htmlResult.status_code
            #print(status.status_code)

    def getTitle(self, soup):
        return soup.find("title").text
        
    def getDescription(self, soup):
        desc = soup.find("meta", {'name':'description'})
        return desc.get('content') if desc != None else ''

    def getImages(self, soup):
        self.images = {}
        imgs = soup.find_all("img")
        for img in imgs:
            self.images[img.get('src')] = img.get('alt')
        return self.images

    def getLinks(self, soup):
        self.links = []
        lnks = soup.find_all("a")
        for a in lnks:
            self.links.append(Link(a.get('href'), a.get('rel') if a.has_attr('rel') else "no rel", a.text))
        return self.links

    """
    H1 H2 H3 taglerin sırası doğru mu değil mi ekle
    """

    def run(self):
        self.results = []
        for url in self.sitemaps[:2]:
            htmlResult = requests.get(url)
            soup = BeautifulSoup(htmlResult.content, "html.parser")
            seoChecks = SeoChecks(url, self.checkStatus(htmlResult),self.getTitle(soup),self.getDescription(soup),self.getImages(soup), self.getLinks(soup))
            self.results.append(seoChecks)
        jsonStr = json.dumps(self.results, default=lambda o: o.__dict__, indent=4)
        with open('./results.txt', 'a', encoding='utf-8') as w:
            w.write(jsonStr)