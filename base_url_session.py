""" Courtesy of jaraco and sigmavirus24:
https://github.com/requests/toolbelt/blob/f5c86c51e0a01fbc8b3b4e1c286fd5c7cb3aacfa/requests_toolbelt/sessions.py
"""

import requests

from urllib.parse import urljoin


class BaseUrlSession(requests.Session):
    base_url = None

    def __init__(self, base_url=None):
        if base_url:
            self.base_url = base_url
        super(BaseUrlSession, self).__init__()

    def request(self, method, url, *args, **kwargs):
        """Send the request after generating the complete URL."""
        url = self.create_url(url)
        return super(BaseUrlSession, self).request(
            method, url, *args, **kwargs
        )

    def create_url(self, url):
        """Create the URL based off this partial path."""
        return urljoin(self.base_url, url)
