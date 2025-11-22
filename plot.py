import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

def create_scatter_plot(x_col, y_col):
    try:
        conn = sqlite3.connect("data.db")
        df = pd.read_sql_query("SELECT * FROM excel_starrydata", conn)
        conn.close()


        #軸に指定がないときは散布図を作らずに終了する
        if not x_col or not y_col:
            return None

        df = df[[x_col, y_col]].dropna()

        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x=x_col, y=y_col, s=10)
        plt.title(f"{x_col} vs {y_col}")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        #グラフをファイルに保存

        fig_path = "static/scatter.png"
        plt.savefig(fig_path)
        plt.close()

        return fig_path
    
    except Exception as e:
        print("散布図にエラーが発生しました：", e)
        return None