from flask import Flask, render_template, json, request
import requests
import dstDataHandler as source
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

# @app.route("/realdata")
# def get_real_data_mock():
# 	yearmonth = '1802'
# 	url = "http://wdc.kugi.kyoto-u.ac.jp/dst_realtime/20{yymm}/dst{yymm}.for.request".format(yymm=yearmonth)
# 	r = requests.get(url, allow_redirects=True)
# 	hour_dst = format_month_dst(r.content)
# 	# print(hour_dst)

# 	response = app.response_class(
# 		response = json.dumps(hour_dst),
# 		status = 200,
# 		mimetype = 'application/json'
# 	)
	# return response

@app.route('/hourly/<year_month>')
def get_real_data(year_month):
	"""
	Get Dst index for every hour
	Parameters
	----------
	year_month : int
				 six digits integer indicating year and month (yyyymm)
				 of the period to obtain data up to present
	"""
	response = app.response_class(
		response = json.dumps(source.get_dst(year_month)),
		status = 200,
		mimetype = 'application/json'
	)
	return response


@app.route('/dailyaverage/<year_month>')
def get_avg_data(year_month):
	"""
	Get average Dst index per day
	Parameters
	----------
	year_month : int
				 six digits integer indicating year and month (yyyymm)
				 of the period to obtain data up to present
	"""
	response = app.response_class(
		response = json.dumps(source.get_dst(year_month, source.IndexType.DAY_AVG)),
		status = 200,
		mimetype = 'application/json'
	)
	return response

def run():
	app.run()
	
if __name__ == "__main__":
	run()
