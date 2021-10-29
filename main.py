from sitecheck import Site

site = ""
with open('./sites.txt') as f:
    site = f.read()

siteSeoChecker = Site(site)
siteSeoChecker.run()