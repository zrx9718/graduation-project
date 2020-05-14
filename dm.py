import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def call_crf(m):
    # 将输入的句子转换成模型测试的格式
    b = ("\n".join(m))
    # print(b)
    with open('chat/CRF/test.txt', 'w') as f:
        f.write(b)
        f.close()

    # 执行训练好的模型生成测试结果
    # os.system(r'bt.bat')
    # print(1,os.stat("test.txt"))
    # print(2,os.stat("result.txt"))

    print(BASE_DIR)
    crf_test_path = os.path.join(BASE_DIR,"crf_test")
    test_text_path = os.path.join(BASE_DIR,"test.txt")
    result_txt_path = os.path.join(BASE_DIR,"result.txt")
    model_path = os.path.join(BASE_DIR,"model")

    a= os.system(f'{crf_test_path} -m {model_path} {test_text_path} >{result_txt_path}')
    print(a)
    # print(3,os.stat("test.txt"))
    # print(4,os.stat("result.txt"))

    # 读取测试的结果，提取实体
    f1 = open('chat/CRF/result.txt', 'r')
    city_list = []
    address_list = []
    hotel_list = []

    for line in f1.readlines():
        if 'B-city' in line:
            city_list.append(line[0])
        if 'I-city' in line:
            city_list.append(line[0])
        if 'B-address' in line:
            address_list.append(line[0])
        if 'I-address' in line:
            address_list.append(line[0])
        if 'B-hotel' in line:
            hotel_list.append(line[0])
        if 'I-hotel' in line:
            hotel_list.append(line[0])
    f1.close()
    # 把list转换成字符串
    city = ''.join(city_list)
    address = ''.join(address_list)
    hotel = ''.join(hotel_list)

    return city, address, hotel
