# DstIndexView
Web tool to display graphs of Dst index by hours and by dates
`dst_sample.txt` shows sample data received from [here](http://wdc.kugi.kyoto-u.ac.jp/dst_realtime/) whose format is documented [here](http://wdc.kugi.kyoto-u.ac.jp/dstae/format/dstformat.html)


### Quick run
Clone this repository and execute (pip is required)
 ```
 python run.py
 ```
The script installs necessary modules and run the server which can be access on localhost:5000.
Select the starting month of the period and submit.
The first graph shows Dst index of every hour from selected month up to present, while the second graph shows average index per day for the same period.

If you have a problem running run.py script, manually install the packages and run the server

 ```
 pip install flask
 pip install requests
 pip install --upgrade pip enum34
 python server.py

```

### Dependencies
server: flask, requests, enum
client: jquery, echarts, bootstrap
 

##### To-do 
- Add script to install dependencies and run server
- Add monthly average graph
- Revisit echarts (datazoom, responsive screen size)
