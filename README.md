CCTV30min
通过网络爬虫爬取中央新闻30分视频 将cctv30mins.py文件拷贝到运行目录 传入参数说明
-s 从YYYYMM 开始下载起始月份的视频
-e 截止到YYYYMM 结束月份的视频

数据源 http://tv.cctv.com/lm/xw30f/

监控网络请求的工具Fiddler，Chrome 浏览器

脚本只是为了熟悉Python语言，请勿将爬取视频作为商业盈利

Python 版本 -v 3.7

运行报module 请自行下载依赖库 pip3.7 install modulename

因为没加入线程，我的电脑配置比较低，下载可能停顿，那是CPU 100% 不是卡死

可自行加相关的机制避免，也可加入线程 降低CPU的使用率

