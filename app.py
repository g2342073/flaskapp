from flask import Flask, render_template, request, send_file
from database import initialize_database, search_database, get_columns
from plot import create_scatter_plot
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
    filename = create_scatter_plot(x_col, y_col)

    if filename:
        static_path = os.path.join(app.root_path, "static", filename)
        if os.path.exists(static_path):
            return send_file(static_path, mimetype="image/png")
        else:
            return "画像ファイルが見つかりませんでした"
    else:
        return "散布図は作成されませんでした(軸が未入力です)"


@app.route("/clear", methods=["POST"])
def clear():
    columns =   get_columns()  
    # results を空にして index.html を再表示
    return render_template("index.html", results=[], columns=columns)

@app.route("/healthz")
def healthz():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

