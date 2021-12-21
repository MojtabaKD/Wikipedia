#!/usr/bin/python
#۱۴٬۳۵۸ members of the "رده:صفحه‌های دارای ارجاع با متغیر تکراری" category now! 21 december 2021 2:20 PM
#released under MIT License (which I don't know it exactly yet!)

import pywikibot
import re
import requests

S = requests.Session()

URL = "https://fa.wikipedia.org/w/api.php"

PARAMS = {
    "action": "query",
    "cmtitle": "رده:صفحه‌های دارای ارجاع با متغیر تکراری",
    "cmlimit": "200",
    "list": "categorymembers",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

PAGES = DATA['query']['categorymembers']

for curr_page in PAGES:
    print(curr_page['title'])
    site = pywikibot.Site('fa', 'wikipedia')
    page = pywikibot.Page(site, curr_page['title'].encode().decode())
    text = page.get()


    citeweb = []

    ind = []

    for match in re.finditer(r'(\{\{یادکرد وب)([^\}\{]*?)(\|\s*archive[-]?url\s*=\s*)([^\s\|\}]*)([^\}\{]*?)(\|\s*تاریخ بایگانی\s*=\s*)([^\|\}]*)([^\}\{]*?)(\|\s*پیوند بایگانی\s*=\s*)([^\s\|\}]*)([^\}\{]*?\}\})', text):
        ind.append((match.start(), match.end(), match.span(6), match.span(7), match.span(9), match.span(10)))
        

    if len(ind)>0:
        tmp = text[0:ind[0][0]]
        i = 0
        
        for x in ind:
            if (i<len(ind)-1):
                tmp += text[x[0]:x[2][0]] + text[x[3][1]:x[4][0]] + text[x[5][1]:x[1]] + text[x[1]:ind[i+1][0]]
            else:
                tmp += text[x[0]:x[2][0]] + text[x[3][1]:x[4][0]] + text[x[5][1]:x[1]] + text[x[1]:]
            i += 1
        # print(tmp)
        page.put(tmp, "حذف پارامتر تکراری در الگوی «یادکرد وب»")

#This is a version of above code for tests in the sandbox:

# site = pywikibot.Site('fa', 'wikipedia')
# page = pywikibot.Page(site, 'کاربر:Mojtabakd/صفحه تمرین')
# text = page.get()

# citeweb = []

# ind = []

# # print("******New Test*******")
# # print("*********************")
# # print("*********************")
# # print("*********************")
# # print("*********************")
# # print("*********************")

# for match in re.finditer(r'(\{\{یادکرد وب)([^\}\{]*?)(\|\s*archive[-]?url\s*=\s*)([^\s\|\}]*)([^\}\{]*?)(\|\s*تاریخ بایگانی\s*=\s*)([^\|\}]*)([^\}\{]*?)(\|\s*پیوند بایگانی\s*=\s*)([^\s\|\}]*)([^\}\{]*?\}\})', text):
    # # print(str(match)+"+++++++")
    
    # # try:
        # # print(str(match.group(1))+"------1-")
    # # except IndexError:
        # # print("1 doesn't exist-------")
    
    # # try:
        # # print(str(match.group(2))+"------2-")
    # # except IndexError:
        # # print("2 doesn't exist-------")
    
    # # try:
        # # print(str(match.group(3))+"------3-")
    # # except IndexError:
        # # print("3 doesn't exist-------")
    
    # # try:
        # # print(str(match.group(4))+"------4-")
    # # except IndexError:
        # # print("4 doesn't exist-------")
    
    # # try:
        # # print(str(match.group(5))+"------5-")
    # # except IndexError:
        # # print("5 doesn't exist-------")
    
    # # try:
        # # print(str(match.group(6))+"------6-")
    # # except IndexError:
        # # print("6 doesn't exist-------")
    
    # # try:
        # # print(str(match.group(7))+"------7-")
    # # except IndexError:
        # # print("7 doesn't exist-------")
    
    # # try:
        # # print(str(match.group(8))+"------8-")
    # # except IndexError:
        # # print("8 doesn't exist-------")
    
    # # try:
        # # print(str(match.group(9))+"------9-")
    # # except IndexError:
        # # print("9 doesn't exist-------")
    
    # # try:
        # # print(str(match.group(10))+"-----10-")
    # # except IndexError:
        # # print("10 doesn't exist-------")
    
    # # try:
        # # print(str(match.group(11))+"-----11-")
    # # except IndexError:
        # # print("11 doesn't exist-------")
    
    # # print("^^^^^^^")
    # # print(len(match.groups()))
    # # print("^^^^^^^")
    
    # ind.append((match.start(), match.end(), match.span(6), match.span(7), match.span(9), match.span(10)))
    

# if len(ind)>0:
    # tmp = text[0:ind[0][0]]
    # i = 0
    
    # for x in ind:
        # if (i<len(ind)-1):
            # tmp += text[x[0]:x[2][0]] + text[x[3][1]:x[4][0]] + text[x[5][1]:x[1]] + text[x[1]:ind[i+1][0]]
        # else:
            # tmp += text[x[0]:x[2][0]] + text[x[3][1]:x[4][0]] + text[x[5][1]:x[1]] + text[x[1]:]
        # i += 1
    # # print(tmp)
    # page.put(tmp, "تست حذف پارامتر تکراری در «یادکرد ویکی»")
