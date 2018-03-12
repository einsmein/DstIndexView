from datetime import datetime
import requests
from enum import Enum

class IndexType(Enum):
	HOUR_ALL = 1 << 0
	DAY_AVG = 1 << 1

def get_dst(year_month, flag=IndexType.HOUR_ALL):
	"""
	Explanation: Get dst index for every hour from `year_month` until the previous month
	Parameters
	----------
	year_month: int
			yyyymm indicating start of the period to obtain dst index
	flag : IndexType
			specifies if it returns dst index for every hours, or daily average where
			default is set to the first option

	Returns a list of lists of two elements 
			["yyyy/mm/dd h", dst_index] if flag = DstFlag.HOUR_ALL
			["yyyy/mm/dd", dst_index] if flag = DstFlag.DAY_AVG
	"""

	result = []
	yyyy = int(year_month[:4])
	mm = int(year_month[4:])
	current_yyyy = datetime.now().year
	current_mm = datetime.now().month - 1

	ym = yyyy*100 + mm
	current_ym = current_yyyy*100 + current_mm

	while (ym <= current_ym):
		url = "http://wdc.kugi.kyoto-u.ac.jp/dst_realtime/{yy0}{yy1}{mm}/dst{yy1}{mm}.for.request".format(yy0=str(ym)[:2],yy1=str(ym)[2:4],mm=str(ym)[4:6])
		print("url: " + url)
		r = requests.get(url, allow_redirects=True)
		result.extend(format_month_dst(r.content, flag))

		if ym % 100 == 12:
			ym += 100 - 11
		else:
			ym += 1
	return result

def format_month_dst(month_dst_raw, flag=IndexType.HOUR_ALL):
	"""
	Format data from a dst index file. File example can be found at dst_sample.txt
	"""
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
	map(lambda row: hour_dst.extend(map_hour_dst(row, flag)), day_dst_split)
	# ['2018/02/01 1', 3]
	return hour_dst

def map_hour_dst(row, flag):
	"""
	Row is expected in the format ['DST1802*01RRX020', '0', '5', '3', ...]
	"""
	all_dst = []
	if flag == IndexType.HOUR_ALL:
		for i in range(24):
			date = "{yy0}{yy1}/{mm}/{dd} {h}".format(yy0=row[0][14:16], yy1=row[0][3:5], mm=row[0][5:7], dd=row[0][8:10], h=i)
			dst = int(row[i+1])
			all_dst.append([date, dst])
		return all_dst
	elif flag == IndexType.DAY_AVG:
		date = "{yy0}{yy1}/{mm}/{dd}".format(yy0=row[0][14:16], yy1=row[0][3:5], mm=row[0][5:7], dd=row[0][8:10])
		dst = int(row[24])
		all_dst.append([date, dst])
		return all_dst
