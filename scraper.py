import copy
import re
import string

import itertools
import requests
from bs4 import BeautifulSoup
from bs4 import ResultSet
from bs4 import Tag
from requests import ConnectionError
from selenium.common.exceptions import WebDriverException
from selenium import webdriver

from configs import SOURCES_CONFIGS
from datautils import create_database, insert_row
from netutils import generate_request_header
from utils import print_progress


class Scraper:
    def scrape(self, schema, output, table_name=None):

        # Validate schema format
        self._check_schema(schema)

        # Get schema information
        url_info = schema.get("url_info")
        listing_info = schema.get("listing_info")
        detail_info = schema.get("detail_info")

        # Save url parameter information including url?
        save_url_info = detail_info.get("save_url_info", False)

        # Create list of headers for creating sqlite database
        headers = detail_info.get("fields").keys()
        if save_url_info:
            headers.append("url")
            if detail_info.get("save_html", False):
                headers.append("html")
            for key in url_info.get("params").keys():
                headers.append(key)

        # If table name not defined, take it from name or by default 'scrape'
        if not table_name:
            table_name = schema.get("name", "scrape")

        print "Creating database '{}' with table '{}' and {} columns.".format(output, table_name, headers)
        create_database(output, table_name, headers)

        print "Generating URLs..."
        # Generate URLs from combining url parameters
        listing_urls = self._construct_urls(url_info)
        print "\tGenerated {} top level urls.".format(len(listing_urls))
        progress = 0
        for listing_url_details in listing_urls:
            progress += 1
            listing_url = listing_url_details.get("url")
            print "Crawling {} ({}/{}) for detail page urls...".format(listing_url, progress, len(listing_urls))
            detail_urls = self._scrape_detail_urls(listing_url, listing_info)
            print "\tfound {} detail page urls.".format(len(detail_urls))

            detail_progress = 0
            successful = 0
            for detail_url in detail_urls:
                detail_progress += 1
                print_progress(detail_progress, len(detail_urls))
                details = self._scrape_details(detail_url, detail_info)

                if not details:
                    continue
                successful += 1
                if save_url_info:
                    details = dict(details.items() + listing_url_details.items())
                    details["url"] = detail_url
                    table_row = []
                    for h in headers:
                        table_row.append(details.get(h))
                    insert_row(output, table_name, table_row)
            print "{}/{} successfully matched criteria.".format(successful, len(detail_urls))

    def _scrape_details(self, detail_url, detail_info):
        unit_container = detail_info.get("unit_container", [("html", "")])
        save_html = detail_info.get("save_html", False)
        fields_info = detail_info.get("fields")
        load_js = detail_info.get("javascript")
        js_calls = detail_info.get("javascript_calls")
        html = None
        if load_js:
            try:
                driver = webdriver.PhantomJS()
                driver.get(detail_url)
                for script in js_calls:
                    driver.execute_script(script)
                html = driver.page_source
            except WebDriverException, e:
                return
        else:
            try:
                html = requests.get(detail_url, headers=generate_request_header()).content
            except ConnectionError:
                return

        unit_html = self._scrape_tag_contents(unit_container, html)

        if not len(unit_html):
            return None

        unit_html = unit_html[0]

        fields = {}
        if save_html:
            fields["html"] = html
        for field, info in fields_info.iteritems():
            tags = info.get("tags")
            replace_content = info.get("replace", [])
            ignore = info.get("ignore", [])
            content = self._scrape_tag_contents(tags, unit_html)
            if len(content):
                content = content[0]
            else:
                content = ""

            prior = content

            for i in ignore:
                srch = re.search(i, content)
                if srch:
                    if len(srch.group()) == len(content):
                        return None

            for find, replace in replace_content:
                if find == '':
                    content = content.strip()
                else:
                    content = re.sub(find, replace, content)
            # print "\t\t\t\t{}\t->\t{}".format(prior.encode("utf-8"), content.encode("utf-8"))
            fields[field] = content
        return fields

    def _scrape_detail_urls(self, listing_url, listing_info):
        detail_urls = []
        url_tags = listing_info.get("details_url")
        next_page_tags = listing_info.get("next_page")
        url_prefix = listing_info.get("url_prefix", "")
        load_js = listing_info.get("javascript", False)
        js_calls = listing_info.get("javascript_calls", [])
        replace_list = listing_info.get("replace", [])

        while True:
            if load_js:
                try:
                    driver = webdriver.PhantomJS()
                    driver.get(listing_url)
                    for script in js_calls:
                        driver.execute_script(script)
                    html = driver.page_source
                except WebDriverException, e:
                    continue
            else:
                try:
                    html = requests.get(listing_url, headers=generate_request_header()).content
                except ConnectionError:
                    continue
            scrape_content = self._scrape_tag_contents(url_tags, html)
            for content in scrape_content:
                for find, replace in replace_list:
                    content = re.sub(find, replace, content)
                if not self._is_url(content):
                    content = "{}{}".format(url_prefix, content)

                if self._is_url(content):
                    detail_urls.append(content)

            next_page_url = self._scrape_tag_contents(next_page_tags, html)

            if not len(next_page_url):
                break

            next_page_url = next_page_url[0]
            if not self._is_url(next_page_url):
                next_page_url = "{}{}".format(url_prefix, next_page_url)
            if self._is_url(next_page_url):
                listing_url = next_page_url
            else:
                break

        return detail_urls

    def _format(self, url):

        # Parse all PROPER()
        match = re.search("PROPER\(.*?\)", url)
        while match:
            start = match.start()
            end = start + len(match.group())

            head = url[:start]
            body = "{}{}".format(string.upper(url[start + 7]), string.lower(url[start + 8: end - 1]))
            space_char = None
            space_char = '-' if body.find("-") >= 0 else space_char
            space_char = '_' if body.find("_") >= 0 else space_char

            if space_char:
                parts = body.split(space_char)
                for idx, part in enumerate(parts):
                    parts[idx] = "{}{}".format(string.upper(part[0]), string.lower(part[1:]))
                body = space_char.join(parts)

            tail = url[end:]
            url = "{}{}{}".format(head, body, tail)

            match = re.search("PROPER\(.*?\)", url)

        # Parse all UPPER
        match = re.search("UPPER\(.*?\)", url)
        while match:
            start = match.start()
            end = start + len(match.group())

            head = url[:start]
            body = string.upper(url[start + 6: end - 1])

            tail = url[end:]
            url = "{}{}{}".format(head, body, tail)

            match = re.search("UPPER\(.*?\)", url)

        # Parse LOWER()
        match = re.search("LOWER\(.*?\)", url)
        while match:
            start = match.start()
            end = start + len(match.group())

            head = url[:start]
            body = string.lower(url[start + 6: end - 1])

            tail = url[end:]
            url = "{}{}{}".format(head, body, tail)

            match = re.search("LOWER\(.*?\)", url)

        return url

    def _construct_urls(self, url_info):
        url_format = url_info.get("format")
        url_params = url_info.get("params")

        url_fields = []
        for param, values in url_params.iteritems():
            url_fields.append(values)

        param_combinations = list(itertools.product(*url_fields))

        urls = []
        for comb in param_combinations:
            params = {}
            for idx, param in enumerate(comb):
                params[url_params.keys()[idx]] = param
            url = url_format.format(**params)
            url = self._format(url)
            params["url"] = url
            urls.append(params)
        return urls

    def _check_schema(self, schema):

        # Defined list of required fields and their types in the last index of the tuple
        required_fields = [
            ("detail_info", "fields", dict),
            ("listing_info", "details_url", list),
            ("url_info", "format", str),
            ("url_info", "params", dict),
        ]

        # Check for required fields including type
        for i in required_fields:
            attr_type = i[-1]
            element = schema.get(i[0])
            for attr in i[1:-1]:
                element = element.get(attr, None)
                if element == None:
                    raise ValueError("Missing attribute {} in schema.".format(attr))

            if not isinstance(element, attr_type):
                raise ValueError(
                    "Invalid attribute type {}. Expected {} got {}.".format(element, attr_type, type(element)))

        # Check if URL format matches to included parameter list in url_info schema
        url_format = schema.get("url_info").get("format")
        required_params = re.findall(r"\{.*?\}", url_format)

        required_params = set([param[1:-1] for idx, param in enumerate(required_params)])

        inputted_params = set(schema.get("url_info").get("params").keys())
        url_diff = required_params - inputted_params
        if len(url_diff) != 0:
            raise ValueError(
                "URL parameter mismatch. Additional parameter '{}' found in URL that is not included in 'params' field.\n"
                "\tEnsure all params included in URL are contained in 'params' attribute".format(
                    "', '".join(url_diff).strip()))

    def _scrape_tag_contents(self, tags, html):

        tag_list = copy.deepcopy(tags)
        if isinstance(html, Tag):
            soup = html
        else:
            soup = BeautifulSoup(html, "lxml")
        results = []
        content_tag, content_attr = tag_list.pop()
        if not len(tag_list):
            return list(soup.findAll(name=content_tag, attrs=content_attr))
        first_tag, first_attr = tag_list.pop(0)
        element_list = soup.findAll(name=first_tag, attrs=first_attr)

        for tag, attr in tag_list:
            temp = ResultSet([], ())
            for element in element_list:
                if isinstance(attr, dict):
                    temp += element.findAll(name=tag, attrs=attr)
                elif isinstance(attr, unicode) or isinstance(attr, str):
                    if element.has_attr(attr):
                        temp.append(element[attr])

            element_list = temp

        for element in element_list:
            if content_tag == "regex":
                pattern = content_attr
                text = element
                if not isinstance(text, str):
                    text = element.text
                if text:
                    match = re.findall(pattern, text)
                    if match:
                        results.append(match[0])
            elif content_attr is None or content_attr == "":
                if content_tag is None or content_tag == "":
                    text = element
                else:
                    text = element.find(content_tag)
                if text:
                    results.append(text.text)
            elif content_tag is None or content_tag == "":
                if element.has_attr(content_attr):
                    results.append(element[content_attr])
            else:
                info_container = element.findAll(name=content_tag)
                for container in info_container:
                    if isinstance(content_attr, dict):
                        results.append(container)
                    elif info_container.has_attr(content_attr):
                        results.append(container[content_attr])
        return results

    def _is_url(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        match = regex.match(url)
        return True if match else None


if __name__ == "__main__":
    test_config = SOURCES_CONFIGS.get("nutritiondata")

    scraper = Scraper()
    scraper.scrape(test_config, "nutritiondata.sqlite")
