from flask import Flask, render_template, json
import requests
app = Flask(__name__)

@app.route("/index")
def index():
	return render_template("index.html")
	# return "Hello World!"

@app.route("/demo")
def demo():
	return render_template("demo.html")

@app.route("/data")
def get_data():
	f = open("data/data.json", "r")
	data = f.read()
	response = app.response_class(
		response = json.dumps(data),
		status = 200,
		mimetype = 'application/json'
	)
	return response

@app.route("/realdata")
def get_real_data():
	yearmonth = '1802'
	url = "http://wdc.kugi.kyoto-u.ac.jp/dst_realtime/20{yymm}/dst{yymm}.for.request".format(yymm=yearmonth)
	r = requests.get(url, allow_redirects=True)
	hour_dst = format_month_dst(r.content)
	# print(hour_dst)

	response = app.response_class(
		response = json.dumps(hour_dst),
		status = 200,
		mimetype = 'application/json'
	)
	return response

def format_month_dst(month_dst_raw):
	day_dst_raw = month_dst_raw.split('\n')[:-3]
	# ['DST1802*01RRX020   0   5   3   ...', '...' ]
	day_dst_split = map(lambda row: row.split(), day_dst_raw)
	# [['DST1802*01RRX020', '0', '5', '3', ...], [...]]
	hour_dst = []
	map(lambda row: hour_dst.extend(map_hour_dst(row)), day_dst_split)
	# ['2018/02/01 1', 3]
	return hour_dst

# row is expected in the format: 
# ['DST1802*01RRX020', '0', '5', '3', ...]
def map_hour_dst(row):
	hour_dst = []
	for i in range(24):
		date = "{yy0}{yy1}/{mm}/{dd} {h}".format(yy0=row[0][14:16], yy1=row[0][3:5], mm=row[0][5:7], dd=row[0][8:10], h=i)
		dst = int(row[i+2])
		hour_dst.append([date, dst])
	return hour_dst

if __name__ == "__main__":
	app.run()