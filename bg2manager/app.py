
import os
import datetime
import json
import ujson
from flask import Flask, render_template, redirect, url_for
from flask import request
from pymongo import MongoClient
import redis

mongo_url = os.getenv("OFFLINE_MONGODB")
redis_url = os.getenv("OFFLINE_REDIS")

mongo_client = MongoClient(mongo_url)
db =mongo_client.crazy_bet
c  = db.t_backpack_template

redis_client = redis.Redis(host=redis_url)


app = Flask(__name__)


@app.route("/")
@app.route("/index")
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


@app.route("/send", methods=["GET","POST"])
def send_prize():
    ret = c.find({}, {"_id":1,"prize_name":1, "prize_num":1, "prize_type":1})



    if request.method == 'POST':
        id_to_prize_info = {str(i.get('_id')):{"prize_num":i.get("prize_num"), "prize_type":i.get("prize_type"), "_id": str(i.get("_id"))} for i in ret}
        data = request.values
        data, _ = data.items()[0]
        data = json.loads(data)
        print 'table ==>', data.get("table")
        print 'uids ==>', data.get("uids")
        print 'title ==>', data.get("title")
        print 'content ==>', data.get("content")
        print 'link ==>', data.get("url")
        _table = data.get("table")
        print 'map -->', id_to_prize_info
        print '_table -->', type(_table)
        new_table = [id_to_prize_info.get(i.get("type").strip()) for i in _table]
        print 'new_table -->', new_table
        data.update({"table":new_table})
        redis_client.rpush('REDIS:BACKPACK:PRIZE:PUSH:QUEUE', ujson.dumps(data))
        redis_client.publish('REDIS:BACKPACK:PRIZE:PUSH:NEW', 1)
        #return redirect(url_for('index'))

    return render_template("send.html", wel_select=ret)


@app.route("/history", methods = ["GET", "POST"])
def history():
    return render_template("history.html")





if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True)
