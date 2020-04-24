dict = {'city': '',
        'price': [],
        'abovePrice': [],
        'belowPrice': [],
        'address': '',
        'hotel': '',
        'require': ''}


def search(dict1):
    # 传入字典
    city = dict1['city']
    price = dict1['price']
    abovePrice = dict1['abovePrice']
    belowPrice = dict1['belowPrice']
    address = dict1['address']
    hotel = dict1['hotel']
    require = dict1['require']

    # 文件地址
    filename = "data/" + city + ".txt"
    data = []
    data1 = []
    data2 = []
    with open(filename, encoding="utf-8") as f:
        for line in f:
            arr = line.split(", ")
            cit = arr[0]
            name = arr[1]
            pri = int(arr[2])
            addr = arr[3].split("\n")[0]
            # 查询价格
            if price != []:
                # 价格在某个区间,必须有两个值，否则会报错
                if len(price) >= 2:
                    if price[0] <= pri < price[1]:
                        data.append((name, pri, addr))
                else:
                    # 某个价格上下浮动30元,list只有一个值
                    if price[0] - 30 < pri < price[0] + 30:
                        data.append((name, pri, addr))
            # 低于某个价格
            if belowPrice != []:
                if pri <= belowPrice[0]:
                    data.append((name, pri, addr))
            # 高于某个价格
            if abovePrice != []:
                if pri > abovePrice[0]:
                    data.append((name, pri, addr))

        # 查询地址
        if address != '':
            for i in data:
                # print(i)
                if address in i[2]:
                    data1.append(i)

    # 查询酒店
    if hotel == '':
        if data1 != []:
            return data1
        else:
            return "抱歉，没找到符合的酒店。"
    elif hotel != '':
        for h in data1:
            if hotel in h[0]:
                data2.append(h)
        if data2 != []:
            return data2
        else:
            return "抱歉，没找到符合的酒店。"
