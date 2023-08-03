from flask import Flask
import datetime
import psutil
import platform
import os
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def index():
    svmem = psutil.virtual_memory()
    load1, load5, load15 = psutil.getloadavg()
    cpu_temp = os.popen("vcgencmd measure_temp").readline()
    cpu_temp = cpu_temp.replace("temp=","")
    sys_data = {}
    tempplateData = {}
    sys_data['Time'] = datetime.datetime.now().strftime("%d-%b-%Y , %I : %M : %S %p")
    sys_data['System'] = platform.system()
    sys_data['Release'] =  platform.release()
    sys_data['version'] = platform.version()
    sys_data['machine'] = platform.machine()
    sys_data['processor'] = platform.processor()
    sys_data['Total Cores'] = psutil.cpu_count(logical=True)
    sys_data['CPU Usage'] = psutil.cpu_percent(4)
    sys_data['Total Memory'] = svmem.total
    sys_data['RAM Used GB'] = psutil.virtual_memory()[3]
    sys_data['Used Memory'] = svmem.used
    sys_data['CPU Temp'] = cpu_temp
    
    tempplateData = {
        'time' : sys_data['Time'],
        'system' : sys_data['System'],
        'release' : sys_data['Release'],
        'version' : sys_data['version'],
        'machine' : sys_data['machine'],
        'processor' : sys_data['processor'],
        'total_cores' : sys_data['Total Cores'],
        'cpu_usage' : sys_data['CPU Usage'],
        'cpu_temp' : sys_data['CPU Temp'],        
        'ram_usage' : sys_data['RAM Used GB'],
        'total_memory' : sys_data['Total Memory'],
    }
    return render_template('index.html', **tempplateData)
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')