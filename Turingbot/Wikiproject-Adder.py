#!/usr/bin/python

# released under MIT License
# This code is executed by user:Turingbot which belongs
# to the user:Mojtabakd on fawiki
# It adds wikiprojects to talkpages of articles

import pywikibot
import wikitextparser as wtp

list_file = open('Persian List of Articles-Pure-Dups Removed-Talk ns.txt', 'r')
Lines = list_file.readlines()

pgen = []
site = pywikibot.Site('fa', 'wikipedia')

for line in Lines:
    pgen.append(pywikibot.Page(site, line.strip()))

# pgen = []
# pgen.append(pywikibot.Page(site, 'کاربر:Mojtabakd/صفحه تمرین'))

edit_limit = 5
edit_counter = 0

out = open("out.txt", "a")

wikiproject_name = "ویکی‌پروژه اسلام"

for curr_page in pgen:
    if edit_counter < edit_limit:
        parsed = wtp.parse(curr_page.text)

        print("article " + str(edit_counter))
        # out.write("\n" + "#"*10 + "Article "
        # + str(edit_counter+1) + "#"*10 +"\n")

        patoob = False

        for temp in parsed.templates:
            if ('پتوپ' == temp.name.strip()):
                patoob = True
                patoob_args = []
                for arg in temp.arguments:
                    parsed_arg_val = wtp.parse(arg.value.strip())
                    for temp_arg in parsed_arg_val.templates:
                        patoob_args.append(temp_arg.name.strip())
                if ('ویکی‌پروژه اسلام' not in patoob_args):
                    old_page = curr_page.text
                    new_arg_name = str(len(temp.arguments)+1)
                    wikiproject_template = '{{' + wikiproject_name
                    + '|کلاس=|خودکار=|نیازمند تصویر='
                    + '|نیازمند جعبه اطلاعات=|اهمیت=}}'
                    old_temp = str(temp)
                    temp.set_arg(name=new_arg_name,
                                 value=wikiproject_template, positional=True)
                    new_temp = str(temp)
                    new_page = old_page.replace(old_temp, new_temp)
                    # out.write(new_page)
                    edit_counter += 1
                    curr_page.put(new_page, "افزودن مقاله به "
                                  + wikiproject_name)

        if not patoob:
            # if curr_page.exists():
            wikiproject_template = '{{پتوپ|{{' + wikiproject_name
            + '|کلاس=|خودکار=|نیازمند تصویر='
            + '|نیازمند جعبه اطلاعات=|اهمیت=}}}}\n'
            new_page = wikiproject_template + curr_page.text
            # out.write(new_page)
            edit_counter += 1
            curr_page.put(new_page, "افزودن مقاله به " + wikiproject_name)

    else:
        out.close()
        break
