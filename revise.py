import json
import random
f = open("hotel",'r',encoding='utf-8')
for line in f.readlines():
    dic = json.loads(line)
    if dic['price']=='0':
        dic['price'] = random.randint(100,300)    #将价格为零的数据进行修改
    t = dic['city'],dic['name'],dic['price'],dic['address']
    s = t.__str__()
    f = open("hotelData.txt",'a',encoding='utf-8')
    f.writelines(s.strip().strip('()').replace('\'',''))
    f.write("\n")
f.close