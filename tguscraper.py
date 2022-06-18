from base_scraper import *
from selenium.webdriver.common.by import By
from base_db import DBHandler
import time
import config


class TGUScraper(ScrapperSelenium):

    def __init__(self, h_url, db_name=None, con=None):
        super(TGUScraper, self).__init__()
        self.historical_data_url = h_url
        self.db = DBHandler(db_name, con)

    def historical_data_wrapper(self, symbol, date_from, date_to):
        self.driver.get(self.historical_data_url.format(s=symbol))
        date_from_id = config.date_from_id
        date_to_id = config.date_to_id
        price_list_id = config.price_list_id
        dt = self.fetch_element(By.ID, date_from_id)
        dt.send_keys(date_from)
        self.fetch_element(By.ID, date_to_id).send_keys(date_to)
        paginate_buttons = self.fetch_element(By.ID, config.btns_id)
        next_btn = self.fetch_element(By.ID, config.btn_next)
        list_of_buttons_str = paginate_buttons.text
        total_pages = self.total_pages(list_of_buttons_str)
        self.db.create_table(config.table_name, config.table.create_command)
        for i in range(total_pages):
            table = self.fetch_element(By.ID, price_list_id)
            table_str = table.text
            self.insert_page_to_db(table_str, config.table_name)
            self.driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(2)
            next_btn = self.fetch_element(By.ID, config.btn_next)

    @staticmethod
    def total_pages(string):
        next_btn = string.index('بعدی')
        etc_str = string.index('…') + 1
        return int(string[etc_str:next_btn])

    def insert_page_to_db(self, tbl, table):
        tbl = tbl.split('\n')
        for line in tbl:
            if line[0] != '0':
                self.db.insert_row(table, line.replace(' ', ','))
