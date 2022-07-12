import requests
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

def get_id(painert_uid:int):
    res = requests.get(url=f'https://www.pixiv.net/ajax/user/{painert_uid}/profile/all?lang=zh',\
        headers=headers, proxies=local_proxies)
    try:
        illuest_dict = res.json()['body']['illusts']
        ID_list1 = [id for id in illuest_dict.keys()]
    except AttributeError:
        print(f'画师UID:{painert_uid}并没有发布过插画')
        ID_list1 = []
    try:
        manga_dict = res.json()['body']['manga']
        ID_list2 = [id for id in manga_dict.keys()]
    except AttributeError:
        print(f'画师UID:{painert_uid}并没有发布过漫画')
        ID_list2=[]
    ID_list = ID_list1+ID_list2
    Record.add_painter(painter_uid=painert_uid)
    for id in ID_list:
        print('[GetID]',end='-->')
        Record.add_image(UID=painert_uid, ID=id, adress=[])
    Record.commit()