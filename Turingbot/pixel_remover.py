#!/usr/bin/python

# released under MIT License
# This code is executed by user:Turingbot which belongs
# to the user:Mojtabakd on fawiki
# removing wrong pixel parameters in infobox of some pages

import pywikibot
from pywikibot import pagegenerators
import wikitextparser as wtp
import re

cat = pywikibot.Category(pywikibot.Site("fa"),
                         "رده:صفحه‌هایی که از جعبه اطلاعات شاعر"
                         + " و نویسنده با پارامترهای نامعلوم استفاده می‌کنند")
gen = pagegenerators.CategorizedPageGenerator(cat)
pgen = pagegenerators.PreloadingGenerator(gen)

site = pywikibot.Site('fa', 'wikipedia')

# pgen = []
# pgen.append(pywikibot.Page(site, 'کاربر:Mojtabakd/صفحه تمرین'))

edit_limit = 10
edit_counter = 0

try:
    for curr_page in pgen:
        parsed = wtp.parse(curr_page.text)
        print(str(curr_page.title()))

        modified_text = ""

        for line in curr_page.text.splitlines():
            x = re.search(r"(.*?)(\|[\d]+?px)(.*?)", line)
            if x and not re.search(r"[\[]", x.group(1)):
                print(x.group(2))
                modified_line = x.group(1)+x.group(3)
                modified_text += modified_line + "\r\n"
            else:
                modified_text = modified_text + line + "\r\n"

        if (modified_text != curr_page.text):
            try:
                edit_counter += 1
                curr_page.put(modified_text, "اصلاح پارامتر پیکسل اشتباه"
                                             + " در تصویر جعبه اطلاعات")
                # print(modified_text)
            except pywikibot.exceptions.LockedPageError:
                print(curr_page.title()+" is locked!")

        if (edit_counter >= edit_limit):
            break
except Exception as e:
    print("Error: {0}".format(e))
