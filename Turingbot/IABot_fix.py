#!/usr/bin/python

# released under MIT License
# This code is executed by user:Turingbot which belongs
# to the user:Mojtabakd on fawiki
# Upgraded according to user:Huji suggestions:
# https://fa.wikipedia.org/w/index.php?title=&oldid=33780764

import pywikibot
from pywikibot import pagegenerators
import wikitextparser as wtp

cat = pywikibot.Category(pywikibot.Site("fa"),
                         "رده:صفحه‌های دارای ارجاع با متغیر تکراری")
# gen = pagegenerators.CategorizedPageGenerator(cat)
# pgen = pagegenerators.PreloadingGenerator(gen)

site = pywikibot.Site('fa', 'wikipedia')

pgen = []
pgen.append(pywikibot.Page(site, 'کاربر:Mojtabakd/صفحه تمرین'))

edit_limit = 1000
edit_counter = 0

accessdate = {'access-date', 'accessdate', 'بازدید',
              'بازیابی', 'بازبینی', 'تاریخ بازدید',
              'تاریخ بازیابی', 'تاریخ بازبینی', 'تاریخ دسترسی'}

for curr_page in pgen:
    parsed = wtp.parse(curr_page.text)
    print(str(curr_page.title()))

    old_templates = []
    new_templates = []

    for template in parsed.templates:
        if (template.name.strip() == 'یادکرد وب'):
            args_names = []

            for arg in template.arguments:
                args_names.append(arg.name.strip())

            dup_accessdates = list(accessdate.intersection(set(args_names)))

            if ((('archiveurl' in args_names) or
                    ('archive-url' in args_names)) and
                    ('پیوند بایگانی' in args_names) and
                    ('تاریخ بایگانی' in args_names) and
                    (len(dup_accessdates) > 1)):

                old_templates.append(str(template))
                template.del_arg('پیوند بایگانی')
                template.del_arg('تاریخ بایگانی')

                for access in dup_accessdates:
                    if ((('accessdate' in dup_accessdates) or
                        ('access-date' in dup_accessdates)) and not
                       (access in ['access-date', 'accessdate'])):
                        template.del_arg(access)

                new_templates.append(str(template))

            elif ((('archiveurl' in args_names) or
                    ('archive-url' in args_names)) and
                    ('پیوند بایگانی' in args_names) and
                    ('تاریخ بایگانی' in args_names) and
                    len(dup_accessdates) <= 1):

                old_templates.append(str(template))
                template.del_arg('پیوند بایگانی')
                template.del_arg('تاریخ بایگانی')
                new_templates.append(str(template))

            elif (len(dup_accessdates) >= 2):
                # I have added this case for special rare cases
                old_templates.append(str(template))

                for access in dup_accessdates:
                    if ((('accessdate' in dup_accessdates) or
                        ('access-date' in dup_accessdates)) and not
                       (access in ['access-date', 'accessdate'])):
                        template.del_arg(access)

                new_templates.append(str(template))

    tmp = curr_page.text

    for i in range(len(old_templates)):
        tmp = tmp.replace(old_templates[i], new_templates[i])

    if (tmp != curr_page.text):
        try:
            edit_counter += 1
            curr_page.put(tmp, "حذف پارامتر(های) تکراری در الگوی «یادکرد وب»")
        except pywikibot.exceptions.LockedPageError:
            print(curr_page.title()+" is locked!")

    if (edit_counter >= edit_limit):
        break
