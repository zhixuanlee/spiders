'''get house information from web'''

import gzip
from urllib import request
import re

import pymysql
from xlwt import Workbook


class Manager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
        self.a = 1


    def add(self, url):
        if url in self.new_urls or url in self.old_urls:
            return
        elif url is not None and len(url) != 0:
            self.new_urls.add(url)
            self.a += 1


    def hasnew(self):
        if len(self.new_urls) != 0:
            return True
        else:
            print('no new')
            print(self.new_urls)



    def get(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def adds(self,new_urls):
        for i in new_urls:
            self.add(i)


class Downloader(object):
    def download(self,url):
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
        req = request.Request(url,headers=head)
        res = request.urlopen(req)
        readed = res.read()
        readed = gzip.decompress(readed)
        if res.getcode() == 200:
            return readed
        else:return


class Parser(object):
    def parse(self, info, thisurl):
        data = info.decode('gbk')
        new_urls = self.geturl(data)
        new_data = self.getdata(data)
        new_data['url'] = thisurl
        return new_urls,new_data


    def geturl(self, data):
        new_urls = set()
        pattern1 = re.compile(r'(http://\w{10,}\.fang\.com/)')
        #pattern2 = re.compile(r'(http://\w+\.fang\.com/house/\w+/housedetail\.htm)')
        for i in re.findall(pattern1, data):
            new_urls.add(i)
        #for i in re.findall(pattern2, data):
            #new_urls.add(i)
        return new_urls


    def getdata(self, data):
        datas = {}
        datas['price'] = re.findall(r'<span class="prib cn_ff">(\d+) </span>元/平方米', data)
        datas['name'] = re.findall(r'<a class=".+" id=".+" href="http://\w+\.fang\.com/" title="(.+)" target="_blank', data)
        datas['loc1'] = re.findall(r'<script type="text/javascript">\s+var city = "(.+)";\s+</script>', data)
        datas['loc2'] = re.findall(r'<li><a target="_blank" href="http://\w+\.\w+\.fang\.com/house/\w+/\w+/" title="(.+)">', data)
        datas['addr'] = re.findall(r'<p><strong>楼盘地址：</strong>&nbsp;&nbsp;<span title="(.+)">', data)
        datas['type'] = re.findall(r'<p><strong>主力户型：</strong>&nbsp;\s+<a href=".+" target="_blank">\s+(.+\)).+\s+</a>&nbsp;&nbsp;\s+<a href=".+" target="_blank">\s+(.+\)).+\s+<a', data)
        if len(datas['type'] ) != 0:
            datas['types'] = datas['type'][0][0] +','+ datas['type'][0][1]
        else:datas['types'] =[]
        datas['score'] = re.findall(r'var score_array_total = "(.+)";////', data)
        return datas


class Outputer(object):
    def __init__(self):
        self.data = []


    def output(self):
        # wb = Workbook()
        # ws = wb.add_sheet('info',cell_overwrite_ok=True)
        # for i in range(len(self.data)):
        #     ws.write(i, 0, self.data[i]['name'])
        #     ws.write(i, 1, self.data[i]['score'])
        #     ws.write(i, 2, self.data[i]['price'])
        #     ws.write(i, 3, self.data[i]['loc1'])
        #     ws.write(i, 4 ,self.data[i]['loc2'])
        #     ws.write(i, 5, self.data[i]['addr'])
        #     ws.write(i, 6, self.data[i]['types'])
        #     ws.write(i, 7, self.data[i]['url'])
        # wb.save('楼盘信息.xls')
        a = 1
        conn = pymysql.connect(host='localhost', user='root', passwd='a13309385258', db='sys',charset='utf8')
        cur = conn.cursor()
        sql = 'insert into house (id, name, rate, price, city, zone, addrs, type, url) VALUES (?,?,?,?,?,?,?,?,?)'
        for i in range(len(self.data)):
            if len(self.data[i]['name']) != 0:
                print(self.data[i])
                try:
                    cur.execute(sql, (a,
                                   self.data[i]['name'][0],
                                   self.data[i]['score'][0],
                                   self.data[i]['price'][0],
                                   self.data[i]['loc1'][0],
                                   self.data[i]['loc2'][0],
                                   self.data[i]['addr'][0],
                                   self.data[i]['url'],
                                   self.data[i]['types']))
                    conn.commit()
                finally:
                    conn.close()

    def add(self, result):
        if result is None:
            return
        else:
            self.data.append(result)


class Spider(object):
    def __init__(self):
        self.manager = Manager()
        self.downloader = Downloader()
        self.parser = Parser()
        self.outputer = Outputer()

    
    def craw(self, url):
        count = 1
        self.manager.add(url)
        while self.manager.hasnew():
            try:
                new_url = self.manager.get()
                print(count,new_url)
                info = self.downloader.download(new_url)
                new_urls,result = self.parser.parse(info,new_url)
                self.outputer.add(result)
                self.manager.adds(new_urls)
                count += 1
                if count>5:
                    break
            except:
                print('craw failed')
        self.outputer.output()


if __name__ == '__main__':
    spider = Spider()
    url = 'http://newhouse.cd.fang.com/house/s/pixian/c23/?ctm=1.cd.xf_search.lpsearch_type.4'
    spider.craw(url)
