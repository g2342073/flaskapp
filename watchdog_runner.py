import pandas as pd
import sqlite3
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
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
                print("更新中にエラーが発生しました",e)

#watchdogをバックグラウンドで起動する

def start_watchdog():
    path = "."
    event_handler = ExcelUpdateHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()