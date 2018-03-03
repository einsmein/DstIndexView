from flask import Flask, render_template, json, request
import requests
from datetime import datetime
app = Flask(__name__)

@app.route("/index")
def index():
	return render_template("index.html")
	# return "Hello World!"

@app.route("/demo")
def demo():
	yearmonth = request.args.get('yearmonth')
	print(yearmonth)
	return render_template("demo.html", year_month = yearmonth)#"{yyyy}{mm}".format(yyyy=year,mm=month), start_date="{yyyy}-{mm}-01".format(yyyy=year,mm=month))

# @app.route("/data")
# def get_data():
# 	f = open("data/data.json", "r")
# 	data = f.read()
# 	response = app.response_class(
# 		response = json.dumps(data),
# 		status = 200,
# 		mimetype = 'application/json'
# 	)
# 	return response

@app.route("/realdata")
def get_real_data_mock():
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

@app.route('/realdata/<year_month>')
def get_real_data(year_month):
	all_dst_index = []
	yyyy = int(year_month[:4])
	mm = int(year_month[4:])
	print(yyyy, mm)
	# yyyy = int(yearmonth[:4])
	# mm = int(yearmonth[4:])
	current_yyyy = datetime.now().year
	current_mm = datetime.now().month - 1

	ym = yyyy*100 + mm
	current_ym = current_yyyy*100 + current_mm

	while (ym <= current_ym):
		url = "http://wdc.kugi.kyoto-u.ac.jp/dst_realtime/{yy0}{yy1}{mm}/dst{yy1}{mm}.for.request".format(yy0=str(ym)[:2],yy1=str(ym)[2:4],mm=str(ym)[4:6])
		print("url: " + url)
		r = requests.get(url, allow_redirects=True)
		all_dst_index.extend(format_month_dst(r.content))

		if ym % 100 == 12:
			ym += 100 - 11
		else:
			ym += 1


	# while (yyyy <= current_yyyy):
	# 	while (mm < current_mm):
	# 		if mm < 10:
	# 			month = '0{}'.format(mm)
	# 		else:
	# 			month = str(mm)
	# 		url = "http://wdc.kugi.kyoto-u.ac.jp/dst_realtime/{yy0}{yy1}{mm}/dst{yy1}{mm}.for.request".format(yy0=str(yyyy)[:2],yy1=str(yyyy)[2:4],mm=month)
	# 		print("url: " + url)
	# 		r = requests.get(url, allow_redirects=True)
	# 		all_dst_index.extend(format_month_dst(r.content))
	# 		if mm == 12:
	# 			mm = 1
	# 			break
	# 		else:
	# 			mm += 1
	# 	yyyy += 1


	response = app.response_class(
		response = json.dumps(all_dst_index),
		status = 200,
		mimetype = 'application/json'
	)
	return response

def format_month_dst(month_dst_raw):
	day_dst_raw = month_dst_raw.split('\n')[:-3]
	# ['DST1802*01RRX020   0   5   3   ...', '...' ]
	day_dst_split = map(lambda row: 
			[row[:20],
			 row[20:24], row[24:28], row[28:32], row[32:36], row[36:40], row[40:44],
			 row[44:48], row[48:52], row[52:56], row[56:60], row[60:64], row[64:68],
			 row[68:72], row[72:76], row[76:80], row[80:84], row[84:88], row[88:92],
			 row[92:96], row[96:100], row[100:104], row[104:108], row[108:112], row[112:116],
			 row[116:]], 
		 day_dst_raw)
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