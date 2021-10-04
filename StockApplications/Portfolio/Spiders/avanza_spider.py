import re
import threading

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from StockApplications.Portfolio.config import ID, STOCK, BUY, SELL, LATEST_PRICE


class AvanzaSpider(threading.Thread):
    def __init__(self, _id, url, options):
        """
        Constructor of StockSpider
        :param url: Supplied stock on Avanza.
        :param options: What options to track on Avanza
        """
        threading.Thread.__init__(self)
        self.id = _id
        self.url = url
        self.options = options
        self.stock_soup = None
        self.stock_name = None
        self.driver = None
        self.stock_values_list = {}

    def init_spider(self):
        self.init_driver()
        self.stock_soup = self.get_soup(self.url)
        self.stock_name = self.stock_soup.find_all('h1')[0].text.strip()

    def init_driver(self, path_driver=r"C:\drivers\chromedriver.exe"):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(executable_path=path_driver, chrome_options=options)

    def get_soup(self, url):
        self.driver.get(url)
        timeout = 0
        try:
            element_present = ec.presence_of_element_located((By.CLASS_NAME, "u-page-container"))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException as te:
            raise te
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup

    def get_latest_stock_value(self):
        value = None
        try:
            tag = self.stock_soup.find_all("span", attrs={"class": re.compile(r'\blatest\b')})[0].text.split()[0]
            float(tag.replace(',', '.'))
            value = tag
        except (ValueError, IndexError) as e:
            print(e)
            print(self.__class__, ": No values found on %s" % self.url)
        return value

    def run(self):
        self.init_spider()
        self.stock_values_list[ID] = self.id
        self.stock_values_list[STOCK] = self.stock_name
        for option in self.options:
            if option == BUY:
                # TODO: Implement get-highest-stock-value
                pass
            if option == SELL:
                # TODO: Implement get-lowest-stock-value
                pass
            if option == LATEST_PRICE:
                self.stock_values_list[LATEST_PRICE] = self.get_latest_stock_value()
        print("Success! ({id}) {stock} : {price}".format(id=self.id,
                                                         stock=self.stock_name,
                                                         price=self.stock_values_list.get(LATEST_PRICE)))
        self.driver.quit()
