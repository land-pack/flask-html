import os
import datetime
from flask import Flask, render_template 
from flask import request
from pymongo import MongoClient

url = os.getenv("OFFLINE_MONGODB")
client = MongoClient(url)
db = client.crazy_bet

c  = db.t_backpack_template


app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")


def to_dict(obj):
    return {k:v for k, v in obj.items() }

@app.route("/input", methods=["POST", "GET"])
def input():
    if request.method == 'POST':
        data = request.values
        data = to_dict(data)
        print 'data ==>', data
        data.update({
            "created": datetime.datetime.now()
        })
        c.insert(data)
    return render_template("input.html")


@app.route("/list")
def list_page():
    lst = []
    ret = c.find()
    data = [
        {
            "index":i.get("_id", 'ss'),
            "name": i.get("prize_name", 'ss'),
            "type": i.get("welfare_type", 'xx'),
            "created":i.get("created", "2019-9-")
        }
        for i in ret
    ]
    return render_template("list.html", data=data)


if __name__ == '__main__':
	app.run(debug=True)
