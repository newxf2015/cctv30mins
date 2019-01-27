import datetime
import requests, json, re, sys, os, urllib, argparse, time
import parser
from  datetime import datetime
from bs4 import BeautifulSoup
import shutil
#爬取新闻30分钟的视频
# 设置文件保存根目录
path = os.getcwd() + r'\新闻30分'
#path = r'/home/gzyDesktop/yangshiPython/huanqiucaijinglianxian/output/ts'
dataurl='http://tv.cctv.com/lm/xw30f/day/{}.shtml'
# 获取当前日期
#now = datetime.datetime.now()
#year = (now.strftime('%y'))
#month = (now.strftime('%m'))
#day = (now.strftime('%d'))
# print(year,month,day)
dateurl_header= {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-US,en;q=0.9',
	'Referer': 'http://tv.cctv.com/lm/xw30f/',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
sess = requests.Session()
cur_dir=os.getcwd()
ts_temp='tmp'
# 根据videoCenterId将对应日期的节目下载到指定文件夹
def downloadVideo(videoCenterId,videotitle):
    dir=os.path.join(path,videotitle)
    isExists = os.path.exists(dir)
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        print("节目未下载，正在下载视频 %s" %videotitle)
        # 下载文件
        for i in range(1, 158):
            #Host: cntv.hls.cdn.apdcdn.com
            downloadUrl = r'http://cntv.hls.cdn.apdcdn.com/asp/hls/1200/0303000a/3/default/'+videoCenterId+r'/' + str(i) + r'.ts'
            filename=str(i).zfill(3)+ ".ts"
            fullpath=os.path.join(ts_temp,filename)
            print("%s-------%s" %(fullpath,downloadUrl))
            r = sess.get(url=downloadUrl,headers=dateurl_header,verify=False)
            with open(fullpath, "wb") as f:
                for chunk in r.iter_content(chunk_size=2048):
                    f.write(chunk)
                    f.flush()
        print("视频%s下载成功" %videotitle)
        merge_file(ts_temp,videotitle)
        os.chdir(cur_dir)
        time.sleep(0.5)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print("视频已下载")

def merge_file(dir,title):
    os.chdir(dir)
    newfile=title[-8:0]+r".mp4"
    newfile=os.path.join(path,newfile)
    #print("-----------%s" %newfile)
    cmd = "copy /b * %s" %newfile
    os.system(cmd)
    #filename=title[-8:0]
    #newfile=os.path.join(path,filename)
    #print("newfile=%s" %filename)
    #shutil.copyfile("tmp.mp4",newfile)
    #print("-------------")
    os.system('del /Q *.ts')
    #os.system('del /Q *.mp4')
def getVideoCenterId(vurl):
    #
    #新闻30分按照月份1号检索
    #jieshaoyeurl = "http://tv.cctv.com/lm/xw30f/"
    try:
        response = sess.get(url=vurl, headers=dateurl_header, verify=False)
        # 介绍页当前最后一个视频链接正则
        #print('%s----------' %response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        hrefs=soup.find_all('a',{'href':re.compile('.*?\.shtml')})
        lasturl=hrefs[len(hrefs) - 1]['href']
        #print("lasturl=-------------------------%s" %lasturl)
        response = sess.get(url=lasturl,headers=dateurl_header,verify=False)
        column_ids=re.findall(r'var column_id = \"(.*?)\";',response.text)
        column_id = column_ids[0]
        #print(column_id)
        itemid1items = re.findall(r'var itemid1=\"(.*?)\";', response.text)
        itemid1 = itemid1items[0]
        #print(itemid1)
        # http://api.cntv.cn/video/getVideoListByTopicIdInfo?videoid={itemid1}&topicid={column_id}&serviceId=cbox&type=0&t=jsonp&cb=setItem0=
        jiemudanUrl = r'http://api.cntv.cn/video/getVideoListByTopicIdInfo?videoid=' + itemid1 + r'&topicid=' + column_id + r'&serviceId=cbox&type=0&t=jsonp&cb=setItem0='
        #print("enumurl=%s" %jiemudanUrl)
        response = sess.get(url=jiemudanUrl,headers=dateurl_header,verify=False)
        #print("json=%s " %response.text)
        #jsons=response.text[15:-2]
        jsons=re.findall(r'setItem0=\((.*?)\);',response.text)
        #print("jsons=%s" %jsons[0])
        enumjsons=json.loads(jsons[0])
        for each in enumjsons['data']:
            #print("-----------%s----------------" %each)
            #fo.addVariable("videoCenterId","626a254ca6c543a9804691e8ada8cd57");//视频生产中心guid (必要值)

            videoCenterIdCompile = r'addVariable\(\"videoCenterId\",\"(.*?)\"\);'
            
            #videoCenterIdpattern = re.compile(videoCenterIdCompile, re.DOTALL)
            #video_url=http://tv.cctv.com/2019/01/24/VIDEX3Pl8IK9fnkjfJNKvI2G190124.shtml
            #print("-----------%s----------------" %each)
            if 'video_url' in each.keys():
                #print("videourl-----------------:%s" %each['video_url'])
                video_url=each['video_url']
                response = sess.get(url=video_url,headers=dateurl_header,verify=False)
                videoCenterIditems = re.findall(videoCenterIdCompile, response.text)
                videoCenterId = videoCenterIditems[0]
                downloadVideo(videoCenterId,each['video_title'])
    except:
        return ''
    # 最新节目url正则
    #newJiemuCompile = 'video_url\":\"(.*?)\",'
	
    #newJiemupattern = re.compile(newJiemuCompile, re.DOTALL)
    #newJiemuitems = re.findall(newJiemupattern, response.text)
    #print(response.text)
    #newJiemu = newJiemuitems[0]
    # print(newJiemu)

    #
    #至此最新节目的url已经获取到了
    #
    #判断当前节目是否是最新节目，如果不是则return
    #if(newJiemu.find(day+".shtml") == -1):
    #    return "300"
    #
    # 获取最新节目的videoCenterId，用于后续的下载
    #response = requests.get(newJiemu)

    # 最新节目url正则
    #videoCenterIdCompile = r'addVariable\("videoCenterId","(.*?)"\);'

    #videoCenterIdpattern = re.compile(videoCenterIdCompile, re.DOTALL)
    #videoCenterIditems = re.findall(videoCenterIdpattern, response.text)

    #videoCenterId = videoCenterIditems[0]
    # print(videoCenterId)
    #return videoCenterId
def startSearchUrl(start,end):
    starttime=datetime.strptime(start,'%Y%m')
    tm = starttime
    endtime=datetime.strptime(end,'%Y%m')
    time_start = time.mktime(starttime.timetuple())
    time_end = time.mktime(endtime.timetuple())
    print('starttime==============%s' %tm)
    print('endtime=================%s' %endtime)
    #print('tm=%d endtime%d' %(time_start,time_end))
    try:
        #开始月份 结束月份
        while time_start <= time_end:
            strtm = datetime.strftime(tm,'%Y%m%d')
            #print("strtm=%s---------" %strtm)
            month = int(datetime.strftime(tm,'%m'))
            year =  int(datetime.strftime(tm,"%Y"))
            #print("year=%d month===%d-----------------" %(year,month))
            url = dataurl.format(strtm)
            #print("url====%s" %(url))
            getVideoCenterId(url)
            month += 1
            if month > 12:
                month = 1
                year += 1
                strtm = str(year) + str(month)
                #将时间装换成月份
                tm = datetime.strptime(strtm,"%Y%m")
            sleep(1)
    except:
        return ''
	
if __name__ == '__main__':
	if len(sys.argv) == 1:
		sys.argv.append('--help')
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--startday', required=True, help=('下载新闻30mins 起始日期 时间格式 201801'))
	parser.add_argument('-e', '--endday', required=True, help=('下载新闻30mins,截止日期 时间格式 201809'))
	args = parser.parse_args()
	isExists=os.path.exists(path)
	if not isExists:
            os.makedirs(path)
	ts_temp=os.path.join(path,ts_temp)
	isExists = os.path.exists(ts_temp)
	if not isExists:
            os.makedirs(ts_temp)
	startSearchUrl(args.startday,args.endday)
	#Xg = Xigua(args.dir,args.keyword)
	#Xg.search_videos(args.keyword, args.pages)
	print('全部下载完成!')
