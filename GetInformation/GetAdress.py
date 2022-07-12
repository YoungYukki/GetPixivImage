import time
import random
import requests
import sqlite3
from Database import Record

# 本地代理
local_proxies = {
    'http':'socks5://192.168.1.10:65533',
    'https': 'socks5://192.168.1.10:65533'   
}

# 头文件
headers = {
    'cookie':open('GetInformation/cookie.txt', encoding='utf-8').read(),
    'referer':'https://www.pixiv.net/',
    'user-agent':open('GetInformation/user-agent.txt', encoding='utf-8').read()
}
def get_image_id(painter_uid):
    database = sqlite3.connect('Database/Pixiv.db')
    cur = database.cursor()
    IDs = cur.execute(f'''SELECT ID FROM UID{painter_uid} WHERE ADRESS='[]';''').fetchall()
    database.close()
    number = 0
    print('[GetAdress]')
    for image_ID in IDs:
        get_adress(ID=image_ID[0], painter_uid=painter_uid)
        # 延时
        number += 1
        if number%5 == 0:
            time.sleep(random.uniform(5.0,8.0))
        else:
            time.sleep(random.uniform(2.0,5.0))
    Record.commit()


def get_adress(ID, painter_uid, error_number=0): # 获取图片下载地址
    try:
        res = requests.get(url=f'https://www.pixiv.net/ajax/illust/{ID}/pages?lang=zh', headers=headers, proxies=local_proxies)
        # 获取图片下载地址
        urls = [res.json()['body'][number]['urls']['original'] for number in range(len(res.json()['body']))]
        print(f'[GetAdress]-->{urls}',end='')
        Record.add_image(UID=painter_uid, ID=ID, adress=urls)
    except requests.exceptions.SSLError:
        error_count += 1
        if error_count >= 10:
            print('被ban次数过多,跳过')
            print(ID)
        else:
            print(f'第{error_number}次出错,正在重试...')
            time.sleep(10)
            get_adress(ID=ID, painter_uid=painter_uid, error_count=error_count)
    
