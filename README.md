# ZSpider


## 基本功能
zspider.py -u url  -t thradNumber  -d deep  -l loglevel(1-5)  -k keyword  --model downloadModel(0/1)  --dbfile    dbName  --testself

### 参数说明

-u 指定爬虫开始地址

-t 指定线程池大小，多线程爬取页面，可选参数，默认10

-d 指定爬虫深度

-l 日志记录文件记录详细程度，数字越大记录越详细，可选参数，默认zspider.log

-k 页面内的关键词，获取满足该关键词的网页，可选参数，默认为所有页面

--model 下载模式，0为静态下载，1为动态下载

--dbfile 存放结果数据到指定的数据库（sqlite）文件中

--testself 程序自测，可选参数

## 模块使用

* 下载模块： requests 、splinter 、phantomjs

* 解析模块： lxml 、urlparse 、hashlib 、re
    
* 存储模块： sqlite3
    
* 线程池模块： threading 
    
* 其它模块： Queue 、optparse 、logging
    

## 系统设计

![](https://github.com/zhjl120/ZSpider/raw/master/img/zspider-framework.png)
## 核心模块
![](https://github.com/zhjl120/ZSpider/raw/master/img/zspider-uml-core.png)
## 线程池模块
![](https://github.com/zhjl120/ZSpider/raw/master/img/zspider-uml-threadpool.png)

##测试

新浪首页： python zspider.py -u http://www.sina.com.cn -t 15 -d 3 -l 3 <br />
<br />
统计：<br />
![](https://github.com/zhjl120/ZSpider/raw/master/img/test-1.png)
<br />运行：<br />
![](https://github.com/zhjl120/ZSpider/raw/master/img/test-2.PNG)
<br />数据库：<br />
![](https://github.com/zhjl120/ZSpider/raw/master/img/test-3.png)
<br /> <br />
测试最终结果：爬取新浪首页三级深度，共抓取页面958187个，耗时近7天。 测试并未达到预期的完成三级深度（由于周末用笔记本打lol，结果以CPU温度过高死机而终）。



