import yfinance as yf
import math
import numpy as np
import pandas as pd
import datetime as dt
from symbol_request import list_ftp_update, read_symbol
import pyodbc
from tqdm.auto import tqdm

# Global variable
SERVER = 'localhost'
DATABASE = 'digital'
USERNAME = 'sa'
PASSWORD = 'abcd1234!'
DRIVE = "{ODBC Driver 18 for SQL Server}"


class DataController():
    def __init__(self) -> None:
        
        if self.check_db_need_update():
            list_ftp_update()
            self.symbol_list = read_symbol()

        else:
            self.symbol_list = read_symbol()

    def database_connection(self):
        """
        Initate the DB connection for query execution
        
        Arg:
            None
        
        Return:
            cursor: pyodbc.connect.cursor: object to execute the SQL query
            cnxn: pyodbc.connect: connection to commit the query
        """
        # information needed for SQL database connection
        cnxn = pyodbc.connect(f'driver={DRIVE};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}')
        cursor = cnxn.cursor()
        return cursor, cnxn
    
    def check_db_need_update(self) -> bool:
        """
        # TODO: Docstring
        """
        cursor, cnxn = self.database_connection()
        # TODO: pull the max date directly
        tsql = "SELECT * FROM stock_hist"
        self.df_hist = pd.read_sql(tsql, cnxn)

        # close the connection after data pulling
        cursor.close()
        cnxn.close()
        
        db_max_date = max(self.df_hist['date']).strftime("%Y-%m-%d")
        yesterday = (dt.datetime.today() - dt.timedelta(days= 1)).strftime("%Y-%m-%d")
        if  db_max_date != yesterday:
            return True
        else:
            return False
    
    def symbol_performance_loop(self):
        """
        #TODO: Docstring
        """
        # Get the date for datapulling
        # TODO: Make it as instance from the class
        start_date = (max(self.df_hist['date']) + dt.timedelta(days = 1)).strftime("%Y-%m-%d")
        end_date = dt.datetime.today().strftime("%Y-%m-%d")

        # Loop the symbol and pulling the performance from yfinance
        for symbol in tqdm(self.symbol_list):
            try:
                temp_df = yf.download(symbol, start = start_date, end = end_date).reset_index()
                temp_df['Symbol'] = symbol
                final_df = pd.concat([final_df, temp_df]).reset_index(drop = True)
            except AttributeError:
                continue
        # Create connection to DB
        cursor, cnxn = self.database_connection()

        # Get the column name for insertion
        cursor.execute("SELECT * FROM stock_hist LIMIT 100")
        final_df.columns = [column[0] for column in cursor.description]

        # Insert the data into DB
        for _, row in final_df.iterrows():
            cursor.execute("""
            INSERT INTO stock_hist (date, open_p, high_p, low_p, close_p, adj_close, volume, symbol) VALUES (?,?,?,?,?,?,?,?)
        """, row.date, row.open_p, row.high_p, row.low_p, row.close_p, row.adj_close, row.volume, row.symbol)
        
        cnxn.commit()
        # Close the connection
        cursor.close()
        cnxn.close()
        


if __name__ == "__main__":
    pass