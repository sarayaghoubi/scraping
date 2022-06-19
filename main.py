from tguscraper import TGUScraper as Tgu
import psycopg2

if __name__ == '__main__':

    conn = psycopg2.connect(database='tgu', user='postgres', password='1372', host='127.0.0.1', port='5432')
    conn.autocommit = True
    selenium = Tgu("https://www.tgju.org/profile/{s}/history", None, conn)
    selenium.historical_data_wrapper('price_dollar_rl', '1400/03/01', '1401/03/25')
