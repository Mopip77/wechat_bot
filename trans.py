import json
import random
import requests

from hashlib import md5
from urllib.parse import quote



def trans_from_text(text, toLang):

    appid = '20180728000189779' #你的appid
    secretKey = 'ZcCcFOQu3fsgx162cq5N' #你的密钥

    host = 'http://api.fanyi.baidu.com'
    myurl = '/api/trans/vip/translate'
    fromLang = 'auto'
    toLang = toLang #en,zh
    salt = random.randint(32768, 65536)

    sign = appid+text+str(salt)+secretKey
    sign = md5(sign.encode('utf-8')).hexdigest()
    myurl = host+myurl+'?appid='+appid+'&q='+quote(text)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    res = requests.get(myurl)
    doc = json.loads(res.text)
    if not doc['trans_result']:
        return 0
    else:
        res = ''
        for line in doc['trans_result']:
            res += line['dst']# + '\n'
        return res

