# GeekBook
a python script for download books from GeekBook as well as getting books' detail info and storing into database.(项目主要是一个用来从geekbook网站上下载所有书的脚本，并且获取所有书的详细信息存入数据库)


### Project structure(大致的项目结构)
```
 |-GeekBook
 	|-data
 		|-cookie4geek.data  //存放cookie
  		|-detailurl.txt     //跑脚本生成的文件 存储所有书的详情页的地址和分类
 	|-scripts
 		|-detector.py       //检测下载损毁的书 并删除 好方便重新下 
 		|-spider.py         //生成供下载时读取的详情链接文件detailurl，并将书的详细信息(封面，简介，作者等)存入数据库 方便后台管理
 		|-worker.py         //根据spider抓到的详情链接文件detailurl 多线程下载图书 并存放到指定分类的目录
 	|-test
 		|-log_test.py       //用于测试
 	|-util
 		|-log_util.py       //用于记录日志
 	|-conf.py               //一些配置
 |-.gitignore               //过滤一些无需上传git的文件
 |-README.MD
 |-setup.py
```

## 生成GeekBook网站所有书的详情页链接的文件，并将详情存入数据库
```
git clone git@github.com:giraffe0813/GeekBook.git
cd GeekBook/scripts
python spider.py
```

## 根据获取的详情页链接多线程下载书 并存储到指定分类目录

```
cd GeekBook/scripts
python worker.py
```

