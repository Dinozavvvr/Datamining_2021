# Created by dinar at 22.03.2021
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
# from urllib3.exceptions import HTTPError
from fake_useragent import UserAgent
from lazy_streams import stream


class PageParser:

    def __init__(self, link: str):
        self.link = link
        self.domain_name = self.get_domain_name()
        self.ua = UserAgent()
        try:
            self.html = self.get_page()
            self.bs_p = BeautifulSoup(self.html, 'html.parser')
        except RuntimeError as e:
            raise RuntimeError(e)

    def get_items_with_tag(self, tag) -> list:
        return self.bs_p.find_all(tag)

    def get_all_href(self, add_domain=False, delete_anchor=False, remove_files=False):
        hr_list = stream(self.bs_p.find_all('a')).map(lambda a: a.get('href')).to_list()
        return self.__additional_checks(hr_list,
                                        add_domain,
                                        delete_anchor,
                                        remove_files)

    def __additional_checks(self, links: list, add_domain=False, delete_anchor=False, remove_files=False):
        pattern = re.compile(r'.*#.*$')
        pattern_for_files = re.compile(r'.*\.(jpg|jpeg|svg|png|pdf)$')

        i = 0
        while i < len(links):
            if delete_anchor:
                if pattern.match(str(links[i])):
                    links.remove(links[i])
                    continue
            if remove_files:
                if pattern_for_files.match(str(links[i])):
                    links.remove(links[i])
                    continue
            if add_domain:
                links[i] = self.__add_domain(str(links[i]))
            i += 1

        return links

    def __add_domain(self, link):
        pattern = re.compile(r'^http[s]?://.*')
        if pattern.search(link) is None:
            return self.domain_name + link
        return link

    def get_pretty(self):
        return self.bs_p.prettify()

    def get_domain_name(self):
        parsed_uri = urlparse(self.link)
        return '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

    def get_page(self):
        try:
            r = requests.get(self.link, timeout=2, headers={'User-Agent': self.ua.chrome})
            return r.text
        except RuntimeError as e:
            raise RuntimeError(e)
