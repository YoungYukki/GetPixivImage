# GetPixivImage
获取P站图片  

---
## 准备工作
### 安装SQLite
>下载<a href="https://www.sqlite.org/download.html" target="_blank">SQLite</a>  
>这是<a href="https://www.runoob.com/sqlite/sqlite-installation.html" target="_blank">安装教程</a>  

### 新建一个数据库
首先命令行输入
```
sqlite3
```
然后进入sqlite的命令行操作,输入  
```
.read Pixiv.sql
```
此时就会建好一个名为Pixiv.db的数据库

---
## 启动
```
python main.py
```
>1. 先输入P站画师的UID  
>2. 再输入P站画师的昵称  
>3. 回车就可以下载所有图片了

---
## 关于代理的问题
我自己使用的是别的设备的代理  
下载图片的话一定要设置代理的  
直接用我的这个是一点用都没有的

---
可能会有点BUG
