# Description
这是一个用来爬取 [CNTV国家大剧院音乐频道](http://www.ncpa-classic.com/) 上面的音乐专辑的爬虫

# Requirements
* Python2.7 64bits (version above 3 not been tested)
* requests library

# Usage
theater.py url

# Example
    theater http://ncpa-classic.cntv.cn/2013/07/16/VIDA1373960896399814.shtml  
    # 这样的代码会在运行目录下产生一个文件夹，文件夹的名字为专辑的名字。
    # 在该文件夹下保存该专辑所有的音乐(码率：192Kbps)
    # 并且还有一个pickle.dat文件用来存储断点续传的信息，该文件可以删除

# Remark
CNTV的CDN比较奇怪，有时候会下载失败，下载失败重试几遍就好了，用pickle来保存断点续传的信息就是为了解决长着问题