# import urllib
# from urllib import request
# proxy_handler = urllib.request.ProxyHandler({'http': '127.0.0.1:8087'})
# opener = urllib.request.build_opener(proxy_handler)
# urllib.request.install_opener(opener)
# url = 'http://t66y.com/thread0806.php?fid=16'
# head = {#'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         #'Accept-Encoding':'gzip, deflate, sdch',
#         #'Cache-Control':'max-age=0',
#         #'Cookie':'__cfduid=dad7f3cf66b89ec499ebf4cafe24feb011476081998; PHPSESSID=07h25cikerbnboc0llp4mqt9j1; CNZZDATA950900=cnzz_eid%3D2010687925-1476079549-http%253A%252F%252Ft66y.com%252F%26ntime%3D1476101342',
#         #'Host':'t66y.com',
#         #'Proxy-Connection':'keep-alive',
#         #'Referer':'http://t66y.com/thread0806.php?fid=8',
#         #'Upgrade-Insecure-Requests': 1,
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
#         }
#
# req = request.Request(url, headers=head)
# res = request.urlopen(req)
#
# reade = res.read().decode('gbk')
# print(reade)
import re

#<input src="https://www1.wi.to/2016/09/26/tVjWy.jpg" type="image" onclick="window.open('http://www.viidii.info/
a = '<input src="https://www1.wi.to/2016/09/26/tSofJ.jpg" type="image"'
#    <input src="http://i1.1100lu.xyz/1100/201604/19/szyk3sczukt.jpg" type="image" onclick="window.open('http://www.viidii.info/
#b = re.findall(r'<input src=[\'|\"](http://.+?[jpg|png])[\'|\"]',a)
b = re.findall(r'input src=[\'|\"](https://.+?[jpg|png])[\'|\"] type=[\'|\"]image',a)
print(b)