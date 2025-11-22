from flask import Flask, render_template, request, send_file
from database import initialize_database, search_database, get_columns
from plot import create_scatter_plot
from database import get_columns
import threading
from watchdog_runner import start_watchdog
import os

app = Flask(__name__)
initialize_database()
threading.Thread(target = start_watchdog, daemon = True).start()

@app.route("/", methods = ["GET", "POST"])
def index():
    columns = get_columns()

    results = None
    if request.method == "POST":
        query = request.form.get("query")
        if query:

            results = search_database(query)
    return render_template("index.html", results=results, columns=columns)

@app.route("/scatter", methods = ["POST"])
def scatter():
    x_col = request.form["x_col"]
    y_col = request.form["y_col"]
    fig_path = create_scatter_plot(x_col, y_col)

    if fig_path and os.path.exists(fig_path):
        return send_file(fig_path, mimetype="image/png")
    elif not fig_path:
        return "散布図は作成されませんでした"
    else:
        return "散布図は作成されませんでした(軸が未入力です)"

@app.route("/clear", methods=["POST"])
def clear():
    columns =   get_columns()  
    # results を空にして index.html を再表示
    return render_template("index.html", results=[], columns=columns)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

