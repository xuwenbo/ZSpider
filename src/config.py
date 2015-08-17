#!/usr/bin/python
# coding:utf-8


SUFFIX_LIST = ['bmp', 'gif', 'jpeg', 'psd', 'png', 'swf', 'jpg', 'ico','tiff', 'psd', 'svg', 'pcx', 'wmf', 'dxf', 'tga'
               'txt', 'pdf', 'wps', 'dat', 'xml', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', ''
               'wav', 'mp3', 'flac', 'wma', 'aac', 'vqf', 'ape', 'mid', 'ogg'
               'mp4', 'avi', 'rmvb', 'mkv', 'rm', '3gp', 'wma', 'flash', 'swf', 'flv', 'mov', 'mpg', 'mpeg', 
               'zip', 'rar', 'tar.gz', '7z', 'iso', 'jar', 'tar', 'bz2',
               'exe', 'msi', 'js', 'css', 'rpm', 'deb', 'apk'
]

USER_AGENTS = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1',
    'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201'
]

FETCH_TIME_INTERVAL = 1

CONNECT_TIME_OUT = 15
