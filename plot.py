import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os
from flask import current_app

def create_scatter_plot(x_col, y_col):
    try:
        conn = sqlite3.connect("data.db")
        df = pd.read_sql_query("SELECT * FROM excel_starrydata", conn)
        conn.close()

        if not x_col or not y_col:
            return None

        df = df[[x_col, y_col]].dropna()

        sample_size = min(1000, len(df))
        df_sample = df.sample(n=sample_size, random_state=1)

        os.makedirs(os.path.join(current_app.root_path, "static"), exist_ok=True)
        


        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df_sample, x=x_col, y=y_col, alpha=0.3, s=2)
        plt.title(f"{x_col} vs {y_col} (sample {sample_size})")
        plt.xlabel(x_col)
        plt.ylabel(y_col)

        fig_path = os.path.join(
                current_app.root_path,
                "static",
                "scatter_sample.png"
            )
        plt.savefig(fig_path)
        plt.close()

        print("保存先:", fig_path, "存在する？", os.path.exists(fig_path))
        return fig_path

    except Exception as e:
        print("散布図にエラーが発生しました：", e)
        return None