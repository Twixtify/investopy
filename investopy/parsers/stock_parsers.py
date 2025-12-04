import ast

from bs4 import BeautifulSoup
from pandas import DataFrame

from investopy.config import HTML_PARSER, STOCK_COLUMNS
from .base_parser import BaseParser


class PrivataAffarer(BaseParser):
    def parse_content(self, html: str) -> DataFrame:
        soup = BeautifulSoup(html, HTML_PARSER)
        # Get main div
        table = soup.find('div', attrs={'class': 'p-table'})
        # Extract table titles
        data_fields = self.get_table_fields(table)
        # Extract table body
        table_body = table.find('tbody', attrs={'class': "page-load-spinner js-table-spinner"})
        # Remove unwanted fields
        for tr in table_body.find_all('tr', attrs={"class": "child-header"}):
            tr.decompose()
        # Find all rows
        rows = table_body.find_all('tr')
        # Save data
        df_rows = []
        for row in rows:
            tmp = {}
            for field in data_fields:
                tmp[field] = row.find('td', attrs={'data-field': field}).text.replace('\n', '')
            df_rows.append(tmp)
        return DataFrame(df_rows)

    @staticmethod
    def get_table_fields(table_soup: BeautifulSoup) -> list[str]:
        row = table_soup.find('thead').find('tr')
        table_headers = row.find_all('th')
        title = []
        for header in table_headers:
            title.append(header['data-field'])
        return title

class IBIndexStocks(BaseParser):
    def parse_content(self, html: str) -> DataFrame:
        cleaned = html.replace('null', 'None')
        products = ast.literal_eval(cleaned)
        df_rows = []
        for product in products:
            stock = product['productName']
            weight = product['price']
            df_rows.append({STOCK_COLUMNS[0]: stock, STOCK_COLUMNS[1]: weight})
        return DataFrame(df_rows, columns=STOCK_COLUMNS)
