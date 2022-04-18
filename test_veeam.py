import psutil
import json
import time
import datetime


def get_proc_info(process_open, interval):
	process = psutil.Process(process_open.pid)
	process_info = {
		"name": process.name(),
		"time": [],
		"CPU_percent": [],
		"Working_Set_MB": [],
		"Private_Bytes_MB": [],
		"Handles": [],
		}
	while True:
		try:
			process_info["time"].append(datetime.datetime.now())
			process_info["CPU_percent"].append(process.cpu_percent())
			process_info["Working_Set_MB"].append(round(process.memory_info().wset / 10**6, 2))
			process_info["Private_Bytes_MB"].append(round(process.memory_info().private / 10**6, 2))
			process_info["Handles"].append(process.num_handles())
			time.sleep(interval)
		except psutil.NoSuchProcess:
			break
	return process_info


try:
	process_open = psutil.Popen(input('Path: ', ))
except FileNotFoundError:
	print("Input (path) is incorrect")
try:
	interval = float(input('Interval, sec: ', ))
except ValueError:
	print("Input (interval) is incorrect")	
	

with open('log.txt', 'w', encoding="utf-8") as log:
	json.dump(get_proc_info(process_open, interval), log, indent=2)
