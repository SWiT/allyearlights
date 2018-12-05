from flask import Flask
from flask import render_template
import os
import json

app = Flask(__name__)

@app.route("/")
def main():
    dirpath = os.path.dirname(os.path.realpath(__file__))
    with open(dirpath + '/schedule.json') as f:
        schedule = json.load(f)
        f.close()

    return render_template('index.html', title='AllYearLights', schedule=schedule)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)