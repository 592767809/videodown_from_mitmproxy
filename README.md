
# 基于mitmproxy的下载方法

## 一、安装环境
### 1.你须要安装谷歌浏览器，测试使用的是谷歌浏览器，其他浏览器自行测试
### 2.例如安装浏览器的路径为（C:\Program Files (x86)\Google\Chrome\Application），那么打开cmd窗口，输入中括号中的内容【"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --proxy-server=127.0.0.1:8080 --ignore-certificate-errors】，如果可以打开浏览器，说明第一步完成
### 3.你必须要安装python环境，建议使用与我相同的3.7版本
### 4.安装python环境后，你必须安装mitmproxy模块（pip install mitmproxy）
### 5.打开cmd窗口，输入中括号的内容【mitmdump --version】，可以正常显示版本，说明第二步完成
### 6.根据其他需要安装第三方模块（包括但不限于pypiwin32, requests）
### 7.下载项目代码并解压，例如解压后的路径为（D:\videodown_from_mitmproxy-main），那么打开cmd窗口，输入中括号中的内容【mitmdump -q -p 8080 -s "D:\videodown_from_mitmproxy-main\main.py"】，如果显示（脚本初始化成功），说明第三步完成
### 8.你需要安装m3u8批量下载器，并在使用前打开下载软件，否则在拦截到视频地址后无法发送下载请求https://www.52pojie.cn/thread-1374045-1-1.html

## 二、优点
### 1.你无需考虑cookie的问题
### 2.无需逆向接口加密参数
### 3.配合python脚本可以完成多元化操作
### 4.可以配合模拟器拦截app端的数据


## 三、缺点
### 1.你需要先进行正确的环境配置，才能使用本工具