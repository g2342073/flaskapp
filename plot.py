import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from flask import current_app

def scatter_plot(x_col, y_col, sample_size=8000):
    try:
        url = "https://drive.google.com/uc?id=1tXaq961lBxWtHi4HV2kKXrfFOVB_ZTjZ"
        df = pd.read_csv(url)
        df = df[[x_col, y_col]].dropna()


        if len(df) == 0:
            print("データが空です")
            return None


        sample_size = min(sample_size, len(df))
        df_sample = df.sample(n=sample_size, random_state=1)

        os.makedirs(os.path.join(current_app.root_path, "static"), exist_ok=True)
        


        plt.figure(figsize=(14, 10))
        sns.scatterplot(data=df_sample, x=x_col, y=y_col, alpha=0.5, s=8)
        plt.title(f"{x_col} vs {y_col} (sample {sample_size})", fontsize=16)
        plt.xlabel(x_col, fontsize=14)
        plt.ylabel(y_col, fontsize=14)
        plt.xticks(rotation=45)
        plt.show()


    except Exception as e:
        print("散布図にエラーが発生しました：", e)
        return None