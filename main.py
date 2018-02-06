'''get *** from 1024'''

import os
import re
import urllib
from urllib import request

class Spide(object):
    def makeurl(self):
        #http://t66y.com/htm_data/16/1610/2083580.html
        #http://t66y.com/htm_data/8/1610/2099140.html  98122
        for i in range(1,999):#
            if i/10<1:
                url = 'http://t66y.com/htm_data/16/1610/209700'+ str(i)+'.html'
                yield url
            elif i/10<10:
                url = 'http://t66y.com/htm_data/16/1610/20970'+ str(i)+'.html'
                yield url
            else:
                url = 'http://t66y.com/htm_data/16/1610/2097'+ str(i)+'.html'
                yield url
    def download(self, url):
        proxy_handler = urllib.request.ProxyHandler({'http': '127.0.0.1:8087'})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
        req = request.Request(url, headers=head)
        res = request.urlopen(req)
        return res.read().decode('gbk')

    def save(self, html):
        n = 1
        photos = re.findall(r'<input src=[\'|\"](https*://.+?.[jpg|png|gif])[\'|\"] type=[\'|\"]image',html)
        name = re.findall(r'<title>(.+\[\w+])  草榴社區',html)
        if name[0] not in os.listdir('F:\images'):
            os.mkdir('F:\images\\'+name[0])
            fileno = range(len(photos))
            for i in fileno:
                photourl = photos[i]
                request.urlretrieve(photourl,'F:\images\\'+name[0]+'\\'+str(i)+'.jpg')
                print('%d saved'%n,photourl)
                n += 1

if __name__ == '__main__':
    print('操作指南：\n')
    if 'images' not in os.listdir('F:'):
        os.mkdir('F:\images')
    n = 0
    spider = Spide()
    urlmaker = spider.makeurl()
    while True:
        try:
            url = next(urlmaker)
            print(url)
            html = spider.download(url)
            spider.save(html)
            n += 1
        except:
            print('1 error')
