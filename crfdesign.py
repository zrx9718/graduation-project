import jieba.posseg as pseg
from .search import search
from .dm import call_crf

# 建立语义槽
dict = {'city': '',
        'price': [],
        'abovePrice': [],
        'belowPrice': [],
        'address': '',
        'hotel': '',
        'require': '',
        "message": ''}

def test():
    while (True):
        a = input()
        result = call_crf(a)
        # print(result)

        # 填城市名
        if result[0] != '':
            dict['city'] = result[0]
        else:
            f = open('chat/CRF/city.txt', 'r', encoding='utf-8')
            for i in f.readlines():
                line = i.strip("\ufeff").strip("\n")
                if line in a:
                    dict['city'] = line
            f.close()
        # print(dict)

        # 填地址
        if result[1] != '':
            dict['address'] = result[1]
        else:
            if dict['city'] == "北京":
                f = open('chat/CRF/bj_address.txt', 'r', encoding='utf-8')
                for i in f.readlines():
                    line = i.strip("\ufeff").strip("\n")
                    if line in a:
                        dict['address'] = line
                # print(dict)
                f.close()
            elif dict['city'] == "上海":
                f = open('chat/CRF/sh_address.txt', 'r', encoding='utf-8')
                for i in f.readlines():
                    line = i.strip("\ufeff").strip("\n")
                    if line in a:
                        dict['address'] = line
                # print(dict)
                f.close()
            # print(dict)
        # 填酒店
        if result[2] != '':
            dict['hotel'] = result[2]
        else:
            f = open('chat/CRF/hotel.txt', 'r', encoding='utf-8')
            for i in f.readlines():
                line = i.strip("\ufeff").strip("\n")
                if line in a:
                    dict['hotel'] = line
            f.close()
            # print(dict)

        # 填价格
        # 建立词列表
        words = []
        # 句子，并分词
        f = pseg.cut(a)
        # 构建词列表
        for i in f:
            words.append((i.word, i.flag))
        for i in range(len(words)):
            if words[i][0] == "-" or words[i][0] == "到":
                dict['price'] = [int(words[i - 1][0]), int(words[i + 1][0])]
            elif words[i][0] == "左右" or words[i][0] == "上下":
                dict['price'] = [int(words[i - 2][0])]
            elif words[i][0] == "大概" or words[i][0] == "大约":
                dict['price'] = [int(words[i + 1][0])]
            elif words[i][0] == "低于":
                dict['belowPrice'] = [int(words[i + 1][0])]
            elif words[i][0] == "以下":
                dict['belowPrice'] = [int(words[i - 2][0])]
            elif words[i - 1][0] == "不" and words[i][0] == "超过":
                dict['belowPrice'] = [int(words[i + 1][0])]
            elif (words[i - 1][0] == "不要" or words[i - 1][0] == "别" or words[i - 1][0] == "不") and words[i][0] == "高于":
                dict['belowPrice'] = [int(words[i + 1][0])]
            elif words[i][0] == "高于":
                dict['abovePrice'] = [int(words[i + 1][0])]
            elif words[i][0] == "以上":
                dict['abovePrice'] = [int(words[i - 2][0])]
        # print(dict)

        # 要求判断
        for i in range(len(words)):
            if words[i][0] == "有":
                dict['require'] = "True"
            elif words[i][0] == "没有":
                dict['require'] = "False"
            elif words[i][0] == "没有了":
                dict['require'] = "False"
            elif words[i][0] == "没了":
                dict['require'] = "False"
            elif words[i][0] == "没":
                dict['require'] = "False"
            elif words[i][0] == "无":
                dict['require'] = "False"
        # print(dict)

        # 对话判断及槽填充
        if dict['city'] == '' or (
                dict['city'] == '' and ((dict['price'] or dict['belowPrice'] or dict['abovePrice']) != [])) or (
                dict['city'] == '' and dict['address'] != '') \
                or (dict['city'] == '' and ((dict['price'] or dict['belowPrice'] or dict['abovePrice']) == []) and dict[
            'address'] == ''):
            print("请问您要订哪个城市呢？")
        if dict['city'] != '' and dict['address'] == '':
            print("好的，您要具体订在哪附近的呢？")
        if dict['city'] != '' and dict['address'] != '' and (
                (dict['price'] or dict['belowPrice'] or dict['abovePrice']) == []):
            print("好的，您能接受的价位是多少呢？")
        if dict['city'] != '' and ((dict['price'] or dict['belowPrice'] or dict['abovePrice']) != []) and dict[
            'address'] != '' and dict['require'] == '':
            print("您还有什么要求吗？（如指定连锁酒店名称，修改价格、地点等）")
            # 最小槽填充
        if dict['city'] != '' and ((dict['price'] or dict['belowPrice'] or dict['abovePrice']) != []) and dict[
            'require'] != '' and dict['address'] != '':
            # 进行查询并结束会话
            print("好的，查询结果如下：")

            print(search(dict))
            break

def talk(dic_talk):

    result = call_crf(dic_talk["message"])
    # 填城市名
    if result[0] != '':
        dic_talk['city'] = result[0]
    else:
        f = open('chat/CRF/city.txt', 'r', encoding='utf-8')
        for i in f.readlines():
            line = i.strip("\ufeff").strip("\n")
            if line in dic_talk["message"]:
                dic_talk['city'] = line
        f.close()
    # 填地址
    if result[1] != '':
        dic_talk['address'] = result[1]
    else:
        if dic_talk['city'] == "北京":
            f = open('chat/CRF/bj_address.txt', 'r', encoding='utf-8')
            for i in f.readlines():
                line = i.strip("\ufeff").strip("\n")
                if line in dic_talk["message"]:
                    dic_talk['address'] = line
            # print(dic_talk)
            f.close()
        elif dic_talk['city'] == "上海":
            f = open('chat/CRF/sh_address.txt', 'r', encoding='utf-8')
            for i in f.readlines():
                line = i.strip("\ufeff").strip("\n")
                if line in dic_talk["message"]:
                    dic_talk['address'] = line
            f.close()
    # 填酒店
    if result[2] != '':
        dic_talk['hotel'] = result[2]
    else:
        f = open('chat/CRF/hotel.txt', 'r', encoding='utf-8')
        for i in f.readlines():
            line = i.strip("\ufeff").strip("\n")
            if line in dic_talk["message"]:
                dic_talk['hotel'] = line
        f.close()
        # print(dic_talk)

    # 填价格
    # 建立词列表
    words = []
    # 句子，并分词
    f = pseg.cut(dic_talk["message"])
    # 构建词列表
    for i in f:
        words.append((i.word, i.flag))
    for i in range(len(words)):
        if words[i][0] == "-" or words[i][0] == "到":
            dic_talk['price'] = [int(words[i - 1][0]), int(words[i + 1][0])]
        elif words[i][0] == "左右" or words[i][0] == "上下":
            dic_talk['price'] = [int(words[i - 2][0])]
        elif words[i][0] == "大概"or words[i][0] == "大约":
            dic_talk['price'] = [int(words[i + 1][0])]
        elif words[i][0] == "低于":
            dic_talk['belowPrice'] = [int(words[i + 1][0])]
        elif words[i][0] == "以下":
            dic_talk['belowPrice'] = [int(words[i - 2][0])]
        elif words[i - 1][0] == "不" and words[i][0] == "超过":
            dic_talk['belowPrice'] = [int(words[i + 1][0])]
        elif (words[i - 1][0] == "不要" or words[i - 1][0] == "别" or words[i - 1][0] == "不") and words[i][0] == "高于":
            dic_talk['belowPrice'] = [int(words[i + 1][0])]
        elif words[i][0] == "高于":
            dic_talk['abovePrice'] = [int(words[i + 1][0])]
        elif words[i][0] == "以上":
            dic_talk['abovePrice'] = [int(words[i - 2][0])]
    # print(dic_talk)

    # 要求判断
    for i in range(len(words)):
        if words[i][0] == "有":
            dic_talk['require'] = "True"
        elif words[i][0] == "没有":
            dic_talk['require'] = "False"
        elif words[i][0] == "没有了":
            dic_talk['require'] = "False"
        elif words[i][0] == "没了":
            dic_talk['require'] = "False"
        elif words[i][0] == "没":
            dic_talk['require'] = "False"
        elif words[i][0] == "无":
            dic_talk['require'] = "False"
    # print(dic_talk)

    # 对话判断及槽填充
    if dic_talk['city'] == '' or (
            dic_talk['city'] == '' and ((dic_talk['price'] or dic_talk['belowPrice'] or dic_talk['abovePrice']) != [])) or (
            dic_talk['city'] == '' and dic_talk['address'] != '') \
            or (dic_talk['city'] == '' and ((dic_talk['price'] or dic_talk['belowPrice'] or dic_talk['abovePrice']) == []) and dic_talk[
        'address'] == ''):
        #print("请问您要订哪个城市呢？")
        dic_talk["message"]="请问您要订哪个城市呢？"

    if dic_talk['city'] != '' and dic_talk['address'] == '':
        #print("好的，您要具体订在哪附近的呢？")
        dic_talk["message"] ="好的，您要具体订在哪附近的呢？"
    if dic_talk['city'] != '' and dic_talk['address'] != '' and (
            (dic_talk['price'] or dic_talk['belowPrice'] or dic_talk['abovePrice']) == []):
        #print("好的，您能接受的价位是多少呢？")
        dic_talk["message"]= "好的，您能接受的价位是多少呢？"
    if dic_talk['city'] != '' and ((dic_talk['price'] or dic_talk['belowPrice'] or dic_talk['abovePrice']) != []) and dic_talk[
        'address'] != '' and dic_talk['require'] == '':
        #print("您还有什么要求吗？（如指定连锁酒店名称，修改价格、地点等）")
        dic_talk["message"] = "您还有什么要求吗？（如指定连锁酒店名称，修改价格、地点等）"
        # 最小槽填充
    if dic_talk['city'] != '' and ((dic_talk['price'] or dic_talk['belowPrice'] or dic_talk['abovePrice']) != []) and dic_talk[
        'require'] != '' and dic_talk['address'] != '':
        # 进行查询并结束会话
        # print("好的，查询结果如下：")
        print(search(dic_talk))
        dic_talk["message"] = "http://127.0.0.1:8000"
        dic_talk["result"] = search(dic_talk)
    return dic_talk


