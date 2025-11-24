import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from flask import current_app

# 散布図用の CSV ファイル（Google Drive 直リンクなど）
CSV_URL = "https://drive.google.com/file/d/1tXaq961lBxWtHi4HV2kKXrfFOVB_ZTjZ/view?usp=drive_link"  # ←ここを散布図用CSVに変更

def get_scatter_columns():
    """
    散布図用CSVから列名を返す
    """
    try:
        df = pd.read_csv(CSV_URL, nrows=1)  # 1行だけ読む
        return list(df.columns)
    except Exception as e:
        print("列名取得に失敗しました:", e)
        return []

def create_scatter_plot(x_col, y_col, sample_size=8000):
    """
    指定された列を使って散布図を作成し、static フォルダに保存する
    """
    try:
        df = pd.read_csv(CSV_URL)
        df = df[[x_col, y_col]].dropna()

        if len(df) == 0:
            print("データが空です")
            return None

        # サンプリング（メモリ対策）
        sample_size = min(sample_size, len(df))
        df_sample = df.sample(n=sample_size, random_state=1)

        # static ディレクトリを作成
        static_dir = os.path.join(current_app.root_path, "static")
        os.makedirs(static_dir, exist_ok=True)

        # 散布図を作成
        plt.figure(figsize=(14, 10))
        sns.scatterplot(data=df_sample, x=x_col, y=y_col, alpha=0.5, s=8)
        plt.title(f"{x_col} vs {y_col} (sample {sample_size})", fontsize=16)
        plt.xlabel(x_col, fontsize=14)
        plt.ylabel(y_col, fontsize=14)
        plt.xticks(rotation=45)

        # 軸ごとにユニークなファイル名を生成
        filename = f"scatter_{x_col}_{y_col}.png"
        output_path = os.path.join(static_dir, filename)
        plt.savefig(output_path)
        plt.close()

        return filename

    except Exception as e:
        print("散布図にエラーが発生しました：", e)
        return None