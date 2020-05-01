import jieba
import jieba.posseg as pseg
from search import search
#jieba自定义词典
#jieba.load_userdict("userdict.txt")

#建立语义槽
dict = {'city':'',
         'price':[],
         'abovePrice':[],
         'belowPrice':[],
         'address':'',
         'hotel':'',
         'require': ''}

while(True):
 a = input()

#填城市名
 f = open('city.txt', 'r', encoding='utf-8')
 for i in f.readlines():
    line = i.strip("\ufeff").strip("\n")
    if line in a:
        dict['city'] = line
 #print(dict)
 f.close()

#填地址
 if dict['city'] == "北京":
     f = open('bj_address.txt', 'r', encoding='utf-8')
     for i in f.readlines():
         line = i.strip("\ufeff").strip("\n")
         if line in a:
             dict['address'] = line
     # print(dict)
     f.close()
 elif dict['city'] == "上海":
     f = open('sh_address.txt', 'r', encoding='utf-8')
     for i in f.readlines():
         line = i.strip("\ufeff").strip("\n")
         if line in a:
             dict['address'] = line
     # print(dict)
     f.close()

#填酒店
 f = open('hotel.txt', 'r',encoding='utf-8')
 for i in f.readlines():
    line = i.strip("\ufeff").strip("\n")
    if line in a:
        dict['hotel'] = line
 #print(dict)
 f.close()
#填价格
# 建立词列表
 words = []
# 句子，并分词
 f = pseg.cut(a)
# 构建词列表
 for i in f:
    words.append((i.word, i.flag))
 for i in range(len(words)):
    if words[i][0]=="-" or words[i][0]=="到":
        dict['price'] = [int(words[i-1][0]),int(words[i+1][0])]
    if words[i][0] == "左右"or words[i][0]=="上下" :
        dict['price'] = [int(words[i-2][0])]
    if words[i][0] == "大概" :
        dict['price'] = [int(words[i+1][0])]
    if words[i][0] == "低于" :
        dict['belowPrice'] = [int(words[i+1][0])]
    if words[i][0] == "以下" :
        dict['belowPrice'] = [int(words[i-2][0])]
    if words[i-1][0] == "不" and words[i][0] == "超过" :
        dict['belowPrice'] = [int(words[i+1][0])]
    if (words[i-1][0] == "不要" or words[i-1][0] == "别"or words[i-1][0] == "不")and words[i][0] == "高于" :
        dict['belowPrice'] = [int(words[i+1][0])]
    if words[i][0] == "高于":
        dict['abovePrice'] = [int(words[i+1][0])]
    if words[i][0] == "以上":
        dict['abovePrice'] = [int(words[i-2][0])]
 #print(dict)

#要求判断
 for i in range(len(words)):
    if words[i][0]=="有":
        dict['require'] ="True"
    elif words[i][0]=="没有" :
        dict['require'] ="False"
    elif words[i][0] == "没有了":
        dict['require'] = "False"
    elif words[i][0] == "没了":
        dict['require'] = "False"
    elif words[i][0] == "没":
        dict['require'] = "False"
    elif words[i][0] == "无":
        dict['require'] = "False"
 #print(dict)

#对话判断及槽填充
 if dict['city'] == ''or (dict['city'] == ''and ((dict['price'] or dict['belowPrice'] or dict['abovePrice'] )!= []))or (dict['city'] == ''and dict['address'] != '')\
    or(dict['city'] == '' and ((dict['price'] or dict['belowPrice'] or dict['abovePrice'] ) == [] )and dict['address'] == ''):
    print("请问您要订哪个城市呢？")
 if dict['city'] != '' and dict['address'] == '':
     print("好的，您要具体订在哪附近的呢？")
 if dict['city']!= '' and dict['address'] !='' and ((dict['price'] or dict['belowPrice'] or dict['abovePrice'] ) == []):
    print("好的，您能接受的价位是多少呢？")
 if dict['city']!= '' and ((dict['price'] or dict['belowPrice'] or dict['abovePrice'] ) != []) and dict['address'] !='' and dict['require'] == '':
    print("您还有什么要求吗？（如指定连锁酒店名称，修改价格、地点等）")
    #最小槽填充
 if dict['city'] != '' and ((dict['price'] or dict['belowPrice'] or dict['abovePrice'] ) != []) and dict['require'] != '' and dict['address'] !='':
    # 进行查询并结束会话
    print("好的，查询结果如下：")

    print(search(dict))
    break