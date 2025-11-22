import pandas as pd
import sqlite3

def initialize_database():
    try:
        print("Excelファイルを読み込み中...")
        df = pd.read_excel("starrydata_samples.xlsx")
        print("読み込んだデータ：")
        print(df)  # ← ここで中身を確認

        for col in df.columns:
            try:
                if df[col].apply(lambda x: isinstance(x, (int, float))).any():
                    if df[col].apply(lambda x: isinstance(x, int) and x > 9223372036854775807).any():
                        print(f"列'{col}' に大きい整数があるため、文字列に変換します")
                        df[col] = df[col].astype(str)

                    elif df[col].dtype == 'object':
                        df[col] = df[col].astype(str)
            except Exception as e:
                print(f"列'{col}'の処理中のエラー：", e)


        conn = sqlite3.connect("data.db")
        df.to_sql("excel_starrydata", conn, if_exists="replace", index=False)
        conn.close()
        print("起動時にExcelを読み込み、テーブルを作成しました。")
    except Exception as e:
        print("初期化中にエラーが発生しました：", e)

def search_database(query):
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        # テーブルの列名を取得
        cursor.execute("PRAGMA table_info(excel_starrydata);")
        columns = [info[1] for info in cursor.fetchall()]

        # 全列に対して LIKE 検索を組み立てる
        conditions = " OR ".join([f"{col} LIKE ?" for col in columns])
        sql = f"SELECT * FROM excel_starrydata WHERE {conditions}"

        # パラメータを列数分用意
        params = ['%' + query + '%'] * len(columns)

        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print("検索中にエラーが発生しました:", e)
        return []

def get_columns():
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(excel_starrydata);")
        columns = [info[1] for info in cursor.fetchall()]
        conn.close()
        return columns
    except Exception as e:
        print("列名取得中にエラーが発生しました:", e)
        return []
    