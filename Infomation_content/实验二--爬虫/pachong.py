# -*- coding:UTF-8 -*-

import json
import time
import requests

proxcy = {
    'http': 'http://27.188.64.70:8060',
    'https': 'https://218.249.45.162:35586'
}

url = 'https://mp.weixin.qq.com/mp/profile_ext'

headers = {
    'Connection': 'keep - alive',
    'Accept': '* / *',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11t Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1170 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/997 MicroMessenger/7.0.10.1580(0x27000AFE) Process/toolsmp NetType/WIFI Language/zh_CN ABI/arm64',
    'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI5NDY1MjQzNA==&devicetype=android-25&version=27000afe&lang=zh_CN&nettype=WIFI&a8scene=59&session_us=gh_119d9e89b19e&pass_ticket=okXVapHY0oqNLzygYo5pb03bu6CbjN17xfVq63Crc2bk9saSxEE3Rtv0OuqKzO8e&wx_header=1',
    'Accept-Encoding': 'br, gzip, deflate'
}

cookies = {
    'devicetype': 'ndroid-25',
    'lang': 'zh_CN',
    'pass_ticket': 'okXVapHY0oqNLzygYo5pb03bu6CbjN17xfVq63Crc2bk9saSxEE3Rtv0OuqKzO8e',
    'version': '27000afe',
    'wap_sid2': 'CPbg2rYDElxheE5JVXRCNUxTSk56aWhXTkZtYWkzclhuWThiVGszc3lQOEtDVDd0VVYxU01sUExycW1IQ05Hb2xEUXpUc0VueWltWTZOSHh4N05mTHFmX05nRy1CeDBFQUFBfjCioMzzBTgNQJVO',
    'wxuin': '920039542'
}


def get_page(offset):
    params = {
        'action': 'getmsg',
        '__biz': 'MzI5NDY1MjQzNA==',
        'f': 'json',
        'offset': '{}'.format(offset),
        'count': '10',
        'is_ok': '1',
        'scene': '126',
        'uin': '777',
        'key': '777',
        'pass_ticket': 'okXVapHY0oqNLzygYo5pb03bu6CbjN17xfVq63Crc2bk9saSxEE3Rtv0OuqKzO8e',
        'appmsg_token': '1053_OB%2FAiHR0TNm2O5fj8PCCxa_N_ATSi5wDk7rSFQ~~',
        'x5': '0',
        'f': 'json',
    }

    return params


def get_info(offset):
    response = requests.get(url, proxies=proxcy, headers=headers, params=get_page(offset), cookies=cookies)
    data = json.loads(response.text)
    flag = data['can_msg_continue']
    next_page = data['next_offset']

    lis = data['general_msg_list']
    info = json.loads(lis)['list']
    for data in info:
        try:
            if data['app_msg_ext_info']['copyright_stat'] == 11:
                msg_info = data['app_msg_ext_info']
                title = msg_info['title']
                content_url = msg_info['content_url']
                # 自己定义存储路径
                print('获取到原创文章：%s ： %s' % (title, content_url))
                with open('article.txt', 'a', encoding='utf-8') as f:
                    f.write('文章标题：'+title+'   '+'网址:'+content_url+'\n')

        except:
            print('不是图文')
    if flag == 1:
        time.sleep(1)
        get_info(next_page)
    else:
        print("error")


if __name__ == '__main__':
    get_info(0)
