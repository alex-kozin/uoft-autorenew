from lxml import html
import requests
from base_url_session import BaseUrlSession

base = "https://toroprod.library.utoronto.ca"
options = "uhtbin/cgisirsi/x/x/0/1/488/X/BLASTOFF/"


def get_option_links(base_url: str, options_url):
    with BaseUrlSession(base_url= base_url) as session:
        page = session.get(options_url)
        tree = html.fromstring(page.content)
        links = tree.xpath('//ul[@class="gatelist_table"]/li/a/@href')

        for i in range(len(links)):
            if not links[i].startswith("http"):
                links[i] = session.base_url + links[i]
        return links
