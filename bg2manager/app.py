from flask import Flask, render_template 


app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/input", methods=["POST", "GET"])
def input():
	return render_template("input.html")

if __name__ == '__main__':
	app.run(debug=True)
