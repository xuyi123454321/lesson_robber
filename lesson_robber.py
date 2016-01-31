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
from PIL import Image

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

    data['userCode'] = input("user code:")
    data['passWord'] = input("password:")

    image_file = open("/tmp/random_image", "rb")
    image = Image.open(image_file)
    image.show()

    data['check'] = input("And the check code:")

    return data

def login(opener):
    postdata = data_input()
    postdata['userbz'] = 's'
    postdata['hldjym'] = ''
    postdata = parse.urlencode(postdata).encode()

    login_res = opener.open(url+"/login.do", postdata)
    login_page = login_res.read().decode("gb2312")

    res_file = open("login.html", "w")
    res_file.write(login_page)
    res_file.close()

def main():
    opener = get_opener(header)
    get_random_image(opener)
    login(opener)

if __name__ == '__main__':
    main()
