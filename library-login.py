from lxml import html
from typing import Dict
import requests
from base_url_session import BaseUrlSession


def get_options(base_url: str, options_url="") -> Dict[str,str]:
    """Returns the dictionary of account management options from the UofT
    Libraries website at base_url, with options_url as a relative link to
    the account management page.

    :param base_url: The url for accessing the Library website.
    :param options_url: The url for accessing account options.
     Default: empty string.
    :return: The dictionary with option names as keys and links to these options
    as values.
    """

    with BaseUrlSession(base_url= base_url) as session:
        page = session.get(options_url)
        tree = html.fromstring(page.content)

        # All option elements are stored in a list with class "gatelist_table"
        link_elements = tree.xpath('//ul[@class="gatelist_table"]/li/a')

        links = {}
        for link_element in link_elements:
            links[link_element.text_content()] = link_element.get("href")
        return links


if __name__ == "__main__":
    # Use case:
    base = "https://toroprod.library.utoronto.ca"
    options = "uhtbin/cgisirsi/x/x/0/1/488/X/BLASTOFF/"

    links = get_options(base, options)
    print(links)
