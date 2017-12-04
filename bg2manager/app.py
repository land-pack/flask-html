from flask import Flask, render_template 
from flask import request
from pymongo import MongoClient


client = MongoClient('mongodb://crazy_bet_rw:crazy_bet_rw@10.0.1.191:27017/crazy_bet')
db = client.crazy_bet

c  = db.t_backpack_template


app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/input", methods=["POST", "GET"])
def input():
    ret = c.find()
    for i in ret:
        print i
    if request.method == 'POST':
        data = request.values
        for k, v in data.items():
            print 'key ==>', k, 'value ==>', v 
        recharge_conf = data.get("recharge_conf")
        print 'recharge_conf', recharge_conf
        #TODO save it on mongodb
    return render_template("input.html")

if __name__ == '__main__':
	app.run(debug=True)
