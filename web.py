import importlib.util
import os
def module_exists(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None
if module_exists("flask"):
    print("模块存在")
else:
    print("模块不存在")
    os.system("pip install flask")
from flask import Flask, render_template
import sqlite3
app = Flask(__name__)
Webdb = os.getcwd()
Webdb = Webdb + '\\Db\\web.db'
@app.route("/")
def index():
    conn = sqlite3.connect(Webdb)
    cursor = conn.cursor()
    data = cursor.execute("SELECT status FROM status").fetchall()
    con = sqlite3.connect("web.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT starttime, endtime, status, rid FROM log")
    tabel = cur.fetchall()
    return render_template("status.html", data=data, tabel=tabel)

if __name__ == '__main__':
    app.run()
