#!/usr/bin/python
# coding:utf-8

'''zspider模块用于接受参数输入并启动爬虫程序'''

import optparse
import scheduler

# 修改import， 添加注释， 调整格式，
# 定时打印程序信息
# 添加动态分配线程，辅助解析线程、下载线程，即改进线程池
# 完成页面关键字解析

def main():
    '''获取输入参数并传递给爬虫程序'''
    parser = optparse.OptionParser(version = '%prog 1.0')
    parser.add_option('-u', '--url', dest = 'url', default = 'http://www.sina.com.cn', help = 'start the domain name')
    parser.add_option('-t', '--thread', dest = 'threadNum', default = 10, help = 'Number of threads')
    parser.add_option('-d', '--depth', dest = 'depth', default = 2, help = 'Crawling depth')
    parser.add_option('-l', '--loglevel', dest = 'loglevel', default = 3, help = 'Log level')
    parser.add_option('-k', '--key', dest = 'keywords', default = '', help = 'Search keywords' )
    parser.add_option('--model', dest = 'model', default = 0, help = 'Crawling mode: Static 0, Dynamic 1')
    parser.add_option('--dbfile', dest = 'dbName', default = 'spider.db', help = 'Database name')
    parser.add_option('--testself', dest = 'test', default = 0, help = 'Test self')

    (options, args) = parser.parse_args()

    startUrl = [options.url]
    threadNum = int(options.threadNum)
    depth = int(options.depth)
    loglevel = int(options.loglevel)
    keywords = options.keywords
    model = int(options.model)
    dbName = options.dbName
    test = int(options.test)

    '''
    print 'url:%s, threadNum:%d, depth:%d, loglevel:%d, keywords:%s, model:%d, dbName:%s' % (
    startUrl, threadNum, depth, loglevel, keywords, model, dbName)
    '''
    # 创建爬虫并启动程序
    spider = scheduler.Scheduler(dbName, threadNum, loglevel, startUrl, depth, keywords, model)
    spider.start()


if __name__ == '__main__':
    main()


