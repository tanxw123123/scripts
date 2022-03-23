#!/usr/bin/python3
import requests
import json
import re
import time
import hashlib
import os
def get_pull_url():
    URL = "https://demo.ioshuju.com/basketball/site/stream_list_new"
    html = requests.get(URL)
    html.encoding = 'gbk'
    Byte_Content = html.content
    # 2. 将返回的内容转换成字典
    Str_Content = str(Byte_Content, encoding = "utf-8")
    Json_content = json.loads(Str_Content)
    # 3. 从获取的字典内容中提取所需的data字段，获取的data字段结果为列表类型
    Data_List = Json_content['data']
    if isinstance(Data_List, list):
        pull_stream_list = []
        # 4. 循环data列表得到字典类型
        for Data_Dict in Data_List:
            for key in Data_Dict:
        # 5. 从获取到的字典中提取关键字为raw_url这个key的value值
                if "raw_url" in key:
                    for url_list in Data_Dict[key]:
        # 6. 循环列表提取拉流地址，获取到字典类型
                        for pull_stream_dict in url_list:
                            pull_stream_list.append(pull_stream_dict['url'])
    return pull_stream_list

#推流
Domain = "rtmp://推流域名/live/"
key = "鉴权key"
for pull_url in get_pull_url():
    print(pull_url)
    StreamName = re.split('/', pull_url)
    StreamName = re.split('\.', StreamName[-1])
    StreamName = StreamName[0]
    now_stamp = int(time.mktime(time.localtime()))
    time_exp = now_stamp + 86400
    tx_Time = hex(time_exp)
    if tx_Time.startswith('0x'):
        tx_Time = tx_Time[2:]
    str1 = key + StreamName + tx_Time
    m = hashlib.md5()
    m.update(str1.encode("utf-8"))
    txSecret = m.hexdigest()
    push_url = Domain + StreamName + "?txSecret=" + txSecret + "&txTime=" + tx_Time
    print(push_url)
    os.system("nohup ffmpeg -re -i %s -vcodec libx264 -acodec copy -f flv %s > nohup.out 2>&1 &" % (pull_url, push_url))

