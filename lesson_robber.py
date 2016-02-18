#!/usr/env python3
'''
a small part of the unfinished code.
These usages have been implemented:
    1. load the entry page ,get the image check code and show it to the user
    2. get the username, password and check code from the user and log into the mis system
    3. save the final response page into a file called login.html
'''

from urllib import request, parse
from http import cookiejar
import re
from PIL import Image # used to show random picture
import pyquery

header = {
    "Host": "mis.teach.ustc.edu.cn",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}

url = "http://mis.teach.ustc.edu.cn"

def get_opener(head):
    # deal with the Cookies
    cj = cookiejar.CookieJar()
    pro = request.HTTPCookieProcessor(cj)
    opener = request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

def get_random_image(opener):
    '''
    this function will grap the check code image
    and save it to /tmp/ramdom_image
    '''
    postdata = parse.urlencode({'userbz':'s'}).encode()
    entry_res = opener.open(url+"/userinit.do", postdata)

    entry_page = entry_res.read().decode('gb2312')

    regex = re.compile("randomImage.do\?date='\d*'")

    image_url = regex.search(entry_page)

    if image_url is None:
        print("Something went wrong!\n")
        return 1
    else:
        image_res = opener.open("%s/%s"%(url,image_url.group()))
        image_data = image_res.read()
        image_file = open("/tmp/random_image", "wb")
        image_file.raw.write(image_data)
        image_file.close()

def data_input():
    data = {
        'passWord': '',
        'userCode': '',
        'check' : '',
    }

    data['userCode'] = input("用户名:")
    data['passWord'] = input("密码:")

    image_file = open("/tmp/random_image", "rb")
    image = Image.open(image_file)
    image.show()

    data['check'] = input("验证码:")

    return data

def login(opener):
    postdata = data_input()
    postdata['userbz'] = 's'
    postdata['hldjym'] = ''
    postdata = parse.urlencode(postdata).encode()

    login_res = opener.open(url+"/login.do", postdata)
    #login_page = login_res.read().decode("gb2312")

    #res_file = open("login.html", "w")
    #res_file.write(login_page)
    #res_file.close()

def query_lesson(opener):
    lesson_type = int(input("课程类型 (1-8, 输0了解编号含义 ):"))

    if lesson_type == 0:
        print("1: 计划内课程")
        print("2: 自由选修")
        print("4: 公选课")
        print("5: 体育选项")
        print("6: 英语选课")
        print("8: 重修重考")

    else:
        while lesson_type not in [1, 2, 4, 5, 6, 8]:
            lesson_type = input("错误的课程类型～\n课程类型 (1-8, 输0了解编号含义 ):")

    lesson_number = input("课堂号:")

    get_data = {
        'xnxq': 20152,
        'seldwdm': 'null',
        'selkkdw': '',
        'seyxn': 2015,
        'seyxq': 2,
        'queryType': lesson_type,
        'rkjs': '',
        'kkdw': '',
        'kcmc': '',
        }
    
    get_data = parse.urlencode(get_data, encoding = 'gb2312')

    query = opener.open("http://mis.teach.ustc.edu.cn/init_st_xk_dx.do?"+get_data)

    query_page = query.read()
    query_page = pyquery.PyQuery(query_page)

    table = query_page.find('table#dxkctable1')
    tr_list = table.find('tr')[1:]
    parameter = {} # some data to grap from query result

    for tr in tr_list:
        if lesson_number == tr.findall('td')[1].text.strip():
            para_text = tr.findall('td')[-1].find('input').values()[-1]
            para_list = para_text.split('(')[1].split(')')[0].split(',')

            parameter['xnxq'] = 20152
            parameter['kcbjbh'] = lesson_number
            parameter['kcid'] = para_list[3][1:-1] # drop "'"
            parameter['kclb'] = para_list[5][1:-1]
            parameter['kcsx'] = para_list[6][1:-1]
            parameter['cxck'] = para_list[9][1:-1]
            parameter['zylx'] = para_list[10][1:-1]
            parameter['gxkfl'] = para_list[11][1:-1]
            parameter['xlh'] = para_list[12][1:-1]
            parameter['sjpdm'] = para_list[7][1:-1]
            parameter['kssjdm'] = para_list[8][1:-1]
            
            break

    try:
        parameter['xnxq']
    except KeyError: # lesson not found
        print('没找到。。。')
        return None
    else:
        return parse.urlencode(parameter, encoding='gb2312')
    
def rob_lesson(opener, para):
    insert_page = opener.open("http://mis.teach.ustc.edu.cn/xkgcinsert.do?"+para)
    print(insert_page.read())

def main():
    opener = get_opener(header)
    get_random_image(opener)
    login(opener)

    try:
        while True:
            para = query_lesson(opener)
            if para != None:
                break

        while rob_lesson(opener, para):
            pass
    except KeyboardInterrupt:
        print('Bye~~')
        return 1

if __name__ == '__main__':
    main()
