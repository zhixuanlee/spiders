'''get images from web'''

import os
import urllib
from time import sleep
from urllib import request
import re


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

    def get(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def adds(self, new_urls):
        for i in new_urls:
            self.add(i)


class Downloader(object):
    def download(self, url):
        proxy_handler = urllib.request.ProxyHandler({'http': '127.0.0.1:8087'})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
        req = request.Request(url, headers=head)
        res = request.urlopen(req)
        reade = res.read().decode('gbk')
        if res.getcode() == 200:
            return reade
        else:
            return


class Parser(object):
    def parse(self, info, thisurl):
        data = info
        new_urls = self.geturl(data)
        new_data = self.getdata(data)
        return new_urls, new_data

    def geturl(self, data):
        new_urls = set()
        pattern = re.compile(r'<a href="(htm_data/\d/\d+/\d+\.html)" target="_blank" id="">.+</a>')
        for i in re.findall(pattern, data):
            j = 'http://t66y.com/'+i
            print(j)
            new_urls.add(j)
        return new_urls

    def getdata(self, html):
        links = set()
        link = re.findall(r'<input src="(http://.+\.jpg)" type="image"', html)
        for i in link:
            links.add(i)
        i = 0
        while len(links) != 0:
            try:
                thisurl = links.pop()
                thisurl2 = re.findall(r'http://.+/\d+/\d+/\d+/(\w+)\.jpg', thisurl)
                filename = thisurl2[0] + '.jpg'
                if filename not in os.listdir('F:\images'):
                    request.urlretrieve(thisurl, 'F:\\images\\' + thisurl2[0] + '.jpg')
                    i += 1
            except:
                 print('something wrong')
        print('保存%d张' % i)
        return i



class Spider(object):
    def __init__(self):
        self.manager = Manager()
        self.downloader = Downloader()
        self.parser = Parser()


    def craw(self, url):
        count = 1
        sums = 0
        self.manager.add(url)
        while self.manager.hasnew():
            #try:
                new_url = self.manager.get()
                print(count,new_url)
                info = self.downloader.download(new_url)
                new_urls, result = self.parser.parse(info, new_url)
                sums += result
                self.manager.adds(new_urls)
                count += 1
                if count > 30:
                    break
            #except:
                #print('failed')
        print('%dphotos saved' % sums)



if __name__ == '__main__':

    if 'images' not in os.listdir('F:'):
        os.mkdir('F:\images')
    spider = Spider()
    url = 'http://t66y.com/thread0806.php?fid=8'
    spider.craw(url)
    print('大功告成，去F盘找images吧  哈哈哈哈哈')
    sleep(2)
