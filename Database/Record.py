import sqlite3
import json
import os

# 初始化数据库
database = sqlite3.connect('Database/Pixiv.db')
cur = database.cursor()

def add_painter(painter_uid:int):     # 检测画师是否存在
    # 画师-ID表查询
    painter = cur.execute(f'SELECT NAME FROM PAINTER WHERE UID={painter_uid}').fetchall()
    if painter == []:
        name = input('请输入画师的昵称:\n>>')
        cur.execute(f'INSERT INTO PAINTER (NAME,UID) VALUES("{name}",{painter_uid});')
        cur.execute(f'CREATE TABLE UID{painter_uid} (\
            ID      INT PRIMARY KEY,\
            ADRESS  TEXT);')
        print(f'画师「{name}」添加成功')
        os.makedirs(f'../images/{painter_uid}')
    else:
        print(f'画师「{painter[0][0]}」存在')

def add_image(UID:int, ID:int, adress:list):
    # 地址列表转化为JSON字符串
    adress_ = json.dumps(adress)
    # 添加图片
    image_information = cur.execute(f'SELECT * FROM UID{UID} WHERE ID={ID}').fetchall()
    if bool(image_information):
        if not image_information[0][1] == '[]':
            print(f'ID:{ID}已经存在')
        else:
            cur.execute(f'''UPDATE UID{UID} SET ADRESS='{adress_}' WHERE ID={ID}''')
            print(f'ID:{ID}添加成功')
    else:
        cur.execute(f'''INSERT INTO UID{UID} (ID,ADRESS) VALUES ({ID},'{adress_}');''')
        print(f'ID:{ID}添加成功')

def commit():
    database.commit()

def close():
    database.close()
