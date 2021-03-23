
import win32gui
import win32process
import os
import re
import requests
import base64

def getport():
    handle = win32gui.FindWindow('WTWindow', 'M3U8批量下载器【by:逍遥一仙】  V1.4.7')
    if handle:
        tid, pid = win32process.GetWindowThreadProcessId(handle)
        for each in os.popen('netstat -ano | findstr ' + str(pid)).read().split('\n'):
            if 'LISTENING' in each:
                port = re.findall('(?<=:)\d+', each)[0]
                return port
    else:
        print('M3U8批量下载器程序版本过低，或者程序未打开')
        return ''

def posttocute(postdata, port):
    url = 'http://127.0.0.1:' + str(port) + '/'
    data = {
        "data": base64.b64encode(postdata.encode('GBK')).decode()
    }
    try:
        response = requests.post(url, data=data).json()
        if response['message'] == 'success':
            print('推送成功')
        else:
            print('推送失败')
            print(response)
    except:
        print('推送失败')