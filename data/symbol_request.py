import ftplib
import pandas as pd
import shutil
import os

SYMBOL_SOURCE_PATH = "symbol_source"

def list_ftp_update():
    ftp_server = ftplib.FTP("ftp.nasdaqtrader.com")
    ftp_server.login()
    ftp_server.encoding = "utf-8"

    filenames = ["nasdaqlisted.txt", "otherlisted.txt"]

    ftp_server.cwd('Symboldirectory')
    ftp_server.dir()

    for filename in filenames:
        with open(filename, "wb") as file:
            ftp_server.retrbinary(f"RETR {filename}", file.write)

    ftp_server.quit()
    
    for filename in filenames:
        shutil.move(filename, f"symbol_source/{filename}")

def read_symbol():
    df = pd.read_csv(os.path.join(SYMBOL_SOURCE_PATH,"nasdaqlisted.txt"), sep = "|")
    print(f"File download at: {df.iloc[-1]['Symbol']}")
    return df

