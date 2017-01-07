import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from netutils import generate_request_header

if __name__ == "__main__":

    url = 'https://groceries.asda.com/site-map'

    #for standard get without javascript
    #response = requests.get(url,headers=generate_request_header())
    #html = response.content

    try:
        driver = webdriver.PhantomJS()
        driver.get(url)
        #e.g. javascript actions required to call more data (twitter feed)
        #for script in js_calls:
        #    driver.execute_script(script)
        html = driver.page_source
    except WebDriverException, e:
        pass #do nothing

    soup = BeautifulSoup(html,"lxml")
    contents = soup.findAll(name="div",attrs={"class":"SM_Section"}) #findall gets all eleemnts, find just returns first element. Returns all elements under SM_section class

    regex = 'https\:\/\/groceries\.asda\.com\/(cat|dept).*'

    for c in contents: #c is just loop through each element, assign variable c for each element
        a_list = c.findAll(name="a") #fnd all where tag name = a
        for a in a_list:
            cat = a.text #part of bs library
            if a.has_attr("href"):
                link = a["href"] #access element of dictionary or use .get
                search = re.search(regex,link)  #re is regex package that searches for regex in string
                                                #search.endpost etc. to find where the string ends etc.
                if search: #if something  has been found, true
                    print link,cat