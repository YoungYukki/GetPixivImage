from GetInformation import GetID, GetAdress
from Database import Record
import time
import random
import os
import sqlite3
import requests
import json

def download_images(painter_uid:int):
    # 获取已经下载的图片
    files = os.listdir(f'../images/{painter_uid}')
    # 打开数据库获取图片下载地址
    database = sqlite3.connect('Database/Pixiv.db')
    cur = database.cursor()
    adresses_cur = cur.execute(f'SELECT ADRESS FROM UID{painter_uid}')
    count = 0
    for adresses_json in adresses_cur:
        adresses = json.loads(adresses_json[0])
        for adress in adresses:
            file_name = os.path.basename(adress)    # 获取文件名
            if file_name in files:
                print(f'{file_name}已经下载')
            else:
                data= download(adress)
                with open(f'../images/{painter_uid}/{file_name}', 'wb') as temp:
                    temp.write(data)
                print(f'[Download]-->{file_name}下载完成')
                count += 1
                if count%5 == 0:
                    time.sleep(random.uniform(5.0,8.0))
                else:
                    time.sleep(random.uniform(2.0,5.0))


def download(adress, error_number=0):
    headers = {
        'cookie':open('GetInformation/cookie.txt', encoding='utf-8').read(),
        'referer':'https://www.pixiv.net/',
        'user-agent':open('GetInformation/user-agent.txt', encoding='utf-8').read()
    }
    # 本地代理
    local_proxies = {
        'http':'socks5://192.168.1.10:65533',
        'https': 'socks5://192.168.1.10:65533'   
    }
    try:
        res = requests.get(url=adress, headers=headers, proxies=local_proxies)
        ret = res.content
    except requests.exceptions.SSLError:
        error_number += 1
        if error_number >= 10:
            print('被ban次数过多,跳过')
            print(adress)
        else:
            print(f'第{error_number}次出错,正在重试...')
            time.sleep(10)   
            ret = download(adress, error_number)
    return ret
        
if __name__ == '__main__':
    painter_uid = int(input('请输入你要添加的画师的UID:\n>>'))
    GetID.get_id(painter_uid)
    GetAdress.get_image_id(painter_uid)
    download_images(painter_uid)
    Record.close()