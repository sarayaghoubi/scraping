from base_scraper import *


# class tgu_price_reader(scrapper_pure):
#     def __init__(self):
#         super(tgu, self).__init__()
#
#     def parse_json(self,output):
#        # q = pd.DataFrame()
#         pass

class TGUScraper(scrapper_sel):
    def __init__(self,h_url):
        super(TGUScraper, self).__init__()
        self.historical_data_url = h_url

    def historical_data_wrapper(self, symbol, date_from, date_to):
        self.driver.get(self.historical_data_url.format(s=symbol))
        date_from_id = 'history-from'
        date_to_id = 'history-to'
        price_list_id = 'table-list'
        self.driver.find_element_by_id(date_from_id).send_keys(date_from)
        self.driver.find_element_by_id(date_to_id).send_keys(date_to)
        table = self.driver.find_element_by_id(price_list_id)
        f = table.get_attribute('outerHTML')
        n_pages = self.driver.find_element_by_id('DataTables_Table_0_paginate')
        f2 = n_pages.get_attribute('outerHTML')
        print("hello")
