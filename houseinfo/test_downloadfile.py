import ssl
from urllib import request

ssl._create_default_https_context = ssl._create_unverified_context
url = 'https://nj02all01.baidupcs.com/file/01be1e6ca43bc4cb9bc9c8794959a6e3?bkt=p-e3edf44cf185bbc94697f646960ee481&fid=2872370364-250528-1151179284&time=1475841402&sign=FDTAXGERLBH-DCb740ccc5511e5e8fedcff06b081203-d%2BV7jpaqvqF0%2FLbbpZ9iEop19T8%3D&to=nj2hb&fm=Nan,B,T,t&sta_dx=39303703&sta_cs=1&sta_ft=zip&sta_ct=7&sta_mt=7&fm2=Nanjing,B,T,t&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=1400277b88ea24a9b0ace5e143530936f00f8bd3816800000257ba17&sl=79364174&expires=8h&rt=sh&r=675930852&mlogid=6513264962529850137&vuk=2047410676&vbdid=2898764778&fin=No.466%20-%20Misa%20Kikoden%20%E3%81%8D%E3%81%93%E3%81%86%E3%81%A7%E3%82%93%E3%81%BF%E3%81%95%20%2885p%29.zip&fn=No.466%20-%20Misa%20Kikoden%20%E3%81%8D%E3%81%93%E3%81%86%E3%81%A7%E3%82%93%E3%81%BF%E3%81%95%20%2885p%29.zip&slt=pm&uta=0&rtype=1&iv=0&isw=0&dp-logid=6513264962529850137&dp-callid=0.1.1&hps=1&csl=100&csign=NxJhCoW942ooELsS5X57SL2bOjU%3D'
head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
req = request.Request(url,headers=head)
res = request.urlopen(req)
print(data = res.read().decode('utf-8'))
data = res.read().decode('utf-8')
with open('F:\data.zip','w',encoding='utf-8') as f:
    f.write(data)
