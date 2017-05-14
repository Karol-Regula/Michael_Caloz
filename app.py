from flask import Flask, render_template, request, redirect, url_for
import utils
from utils import database, accounts

app = Flask(__name__)


@app.route("/")
def placeholder0():
  data = database.getSampleData()
  return render_template('test.html', variable = data)


if __name__ == "__main__":
    app.debug = True
    # app.config.from_object("config")
    # app.secret_key = app.config["SECRET_KEY"]
    app.run()
