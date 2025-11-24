import pandas as pd
import sqlite3
import time
import os
import gdown
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

FILE_ID = "1tXaq961lBxWtHi4HV2kKXrfFOVB_ZTjZ"
URL = f"https://drive.google.com/uc?id={FILE_ID}"
OUTPUT = "starrydata_curves.csv"

class ExcelUpdateHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("starrydata_samples.xlsx"):
            print("Excelファイルが更新されました。データベースを更新します")
            try:
                df = pd.read_excel("starrydata_samples.xlsx")
                conn = sqlite3.connect("data.db")
                df.to_sql("excel_starrydata", conn, if_exists="replace", index=False)
                conn.close()
                print("更新完了しました")
            except Exception as e:
                print("更新中にエラーが発生しました", e)

def update_csv_from_drive():
    """Google Driveから最新CSVを取得"""
    try:
        gdown.download(URL, OUTPUT, quiet=True, fuzzy=True)
        print("DriveからCSVを更新しました")
    except Exception as e:
        print("CSV更新に失敗しました:", e)

def start_watchdog():
    path = "."
    event_handler = ExcelUpdateHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()
    try:
        while True:
            # Excelファイル監視はwatchdogが担当
            # DriveのCSVは定期的に更新
            update_csv_from_drive()
            time.sleep(3600)  # 1時間ごとに更新
    except KeyboardInterrupt:
        observer.stop()
    observer.join()