
import mitmproxy.http
import json
import requests
import base64
import zlib
import funcutils
from urllib import parse

# mitmdump -q -p 8080 -s main.py

port = funcutils.getport()
if not port:
    exit(0)
print('脚本初始化成功')

def request(flow: mitmproxy.http.HTTPFlow):
    pass

def response(flow: mitmproxy.http.HTTPFlow):
    if 'cache.video.iqiyi.com/dash' in flow.request.url:
        # 拦截爱奇艺视频
        print('爱奇艺：已拦截数据')
        try:
            data = json.loads(flow.response.content.decode())
        except:
            print('爱奇艺：数据初始化异常')
            return
        try:
            for video in data['data']['program']['video']:
                if 'm3u8' in video.keys():
                    m3u8text = video['m3u8']
                    if '#EXTM3U' in m3u8text:
                        # 表示非加密视频
                        # 获取标题
                        url = 'https://pcw-api.iqiyi.com/video/video/baseinfo/' + str(data['data']['tvid'])
                        response = requests.get(url).json()
                        title = response['data']['name']+'_'+str(video['bid'])
                        data = json.dumps({
                            'data': m3u8text
                        })
                        postdata = title + ',base64:' + base64.b64encode(data.encode('GBK')).decode()
                        funcutils.posttocute(postdata, port)
                        return
                    else:
                        # 加密视频逻辑
                        return
            print('爱奇艺：未找到有效的视频数据')
        except:
            print('爱奇艺：数据分析异常')
            return

    elif 'vd.l.qq.com/proxyhttp' in flow.request.url:
        # 拦截腾讯视频
        request_payload = json.loads(flow.request.content.decode())
        if request_payload['buid'] == 'vinfoad':
            print('腾讯视频：已拦截数据')
            try:
                data = json.loads(zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(flow.response.get_content(False)).decode())
            except:
                print('腾讯视频：数据初始化异常')
                return
            try:
                data = json.loads(data['vinfo'])
                title = data['vl']['vi'][0]['ti']
                if 'ckc' in data['vl']['vi'][0].keys():
                    # 加密视频逻辑
                    return
                else:
                    # 表示非加密视频
                    videoid = int(data['vl']['vi'][0]['keyid'].split('.')[-1])
                    bid = ''
                    for each in data['fl']['fi']:
                        if each['id'] == videoid:
                            bid = each['resolution']
                            break
                    m3u8url = data['vl']['vi'][0]['ul']['ui'][-1]['url']
                    title = title + '_' + bid
                    postdata = title + ',' + m3u8url
                    funcutils.posttocute(postdata, port)
                    return
            except:
                print('腾讯视频：数据分析异常')
                return
 
    elif 'acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/' in flow.request.url:
        # 拦截优酷视频
        print('优酷：已拦截数据')
        requestquery = parse.parse_qs(parse.urlparse(flow.request.url).query)
        requestcallback = requestquery['callback'][0]
        requestdata = json.loads(requestquery['data'][0])
        encryptR_client = json.loads(requestdata['biz_params'])['encryptR_client']
        try:
            data = json.loads(flow.response.text[len(requestcallback)+2:-1])['data']['data']
        except:
            print('优酷：数据初始化异常')
            return
        try:
            title = data['show']['stage']
            if title < 10:
                title = '0' + str(title)
            else:
                title = str(title)
            title = data['show']['title'] + ' ' + title
        except:
            try:
                title = data['show']['stage'] + ' ' + data['video']['title']
            except:
                title = data['video']['title']
        if data['video']['drm_type'] == 'default':
            # 表示非加密视频
            videolist = data['stream']
            videolist.sort(key=lambda n: n['size'])
            m3u8url = videolist[-1]['m3u8_url']
            postdata = title + ',' + m3u8url
            funcutils.posttocute(postdata, port)
            return
        else:
            # 加密视频逻辑
            return

