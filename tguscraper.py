from base_scraper import *
from selenium.webdriver.common.by import By
from base_db import DBHandler
import time
import config
import matplotlib.pyplot as plt
from mplfinance import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpdates


class TGUScraper(ScrapperSelenium):

    def __init__(self, h_url, db_name=None, con=None):
        super(TGUScraper, self).__init__()
        self.historical_data_url = h_url
        self.db = DBHandler(db_name, con)
        self.show_modes = {
            'chart': self.show_chart,
            'line': self.plot_data
        }

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
        self.db.create_table(config.table_name, config.create_command)
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

    def insert_page_to_db(self, tbl, table, save_as_csv):
        tbl = tbl.split('\n')
        df = pd.DataFrame(columns=[config.price_keywords, 'Date'])
        for line in tbl:
            if line[0] != '0':
                line = line.replace('/', '-')
                line = line.replace(',', '.').split(' ')
                row = f'{line[0]},{line[1]},{line[2]},{line[3]},\'{line[6]}\',\'{line[7]}\''
                self.db.insert_row(table, row)
                df = df.append(float(line[0]), float(line[1]), float(line[2]), float(line[3]), line[7],
                               ignore_index=True)
        if save_as_csv is not None:
            df.to_csv(save_as_csv, index=False)

    @staticmethod
    def show_chart(data):
        plt.style.use('dark_background')
        # extracting Data for plotting
        df = pd.read_csv(f'{data}.csv')
        df = df[['OPEN', 'LOW', 'HIGH',
                 'CLOSE', 'DateF']]
        # convert into datetime object
        df['DateF'] = pd.to_datetime(df['DateF'])
        # apply map function
        df['DateF'] = df['DateF'].map(mpdates.date2num)
        # creating Subplots
        fig, ax = plt.subplots()
        # plotting the data
        candlestick_ohlc(ax, df.values, width=0.6,
                         colorup='green', colordown='red',
                         alpha=0.8)
        # allow grid
        ax.grid(True)

        # Setting labels
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')

        # setting title
        plt.title('Dollar to Rial')

        # Formatting Date
        date_format = mpdates.DateFormatter('%d-%m-%Y')
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        fig.tight_layout()
        # show the plot
        plt.show()

    @staticmethod
    def plot_data(data, price_keyword):
        assert price_keyword in config.price_keywords
        # plotting a line graph
        df = pd.read_csv(f'{data}.csv')
        plt.plot(df["DateF"], df[price_keyword])
        plt.show()
