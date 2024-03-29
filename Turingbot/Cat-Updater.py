#!/usr/bin/python

# released under MIT License
# This code is executed by user:Turingbot which belongs
# to the user:Mojtabakd on fawiki. It updates categories
# in a list of pages given by a file or randmoly chosen...

import pywikibot
import re
from pywikibot import pagegenerators

remover = True

# update_list = open('update_list.txt', 'r')
# upd_lines = update_list.readlines()
# update_list.close()

exclude_list = open('exclude_list.txt', 'r')
exc_lines = exclude_list.readlines()
exclude_list.close()

pgen = []

site_fa = pywikibot.Site('fa', 'wikipedia')
site_en = pywikibot.Site('en', 'wikipedia')

# for line in upd_lines:
    # pgen.append(pywikibot.Page(site_fa, line.strip()))

pgen = site_fa.randompages(total=200, namespaces=0, redirects=False)

# pgen = []
# pgen.append(pywikibot.Page(site_fa, 'کاربر:Mojtabakd/صفحه تمرین'))

edit_limit = 100
edit_counter = 0

counter = 0

out = open("out.txt", "a")


# pywikibot's categories() isn't helpful here, becuase
# it returns extra unneeded categories. So we define:
def GetCats(src, lang):
    if lang == "en":
        cat = "category"
    elif lang == "fa":
        cat = "رده"

    pattern = r'\[\[[^:\[\]]*?' + cat + r'[^:\[\]]*?:[^:\[\]]*?\]\]'
    cats = re.findall(pattern, src, flags=re.I)

    stripped = []

    for x in cats:
        tmp = re.sub(r"\[\[", "", x)
        tmp = re.sub(r"\]\]", "", tmp)

        cat_groups = re.search(r"([^\|]*)\|?(.*)", tmp)
        cat_g1 = cat_groups.group(1).strip()
        cat_g2 = cat_groups.group(2).strip()
        splitter[cat_g1] = cat_g2

        stripped.append(cat_g1)

    stripped.sort()

    return stripped


for curr_page in pgen:
    eng_cats = []
    loc_cats = []
    eng_cats_trans = []
    orig_fa_cats = []
    splitter = {}

    if curr_page.exists():
        counter += 1
        print("="*10 + curr_page.title() + "="*10 + str(counter))

        page_is_conn = False

        try:
            curr_page_item = pywikibot.ItemPage.fromPage(curr_page)
            engtitle = curr_page_item.getSitelink('enwiki')
            page_is_conn = True
        except Exception:
            page_is_conn = False
            print('Page is not connected.')

        if page_is_conn:
            # So the page is connected we can continue the task
            engpage = pywikibot.Page(site_en, engtitle)
            for cat_title in GetCats(engpage.text, 'en'):
                cat = pywikibot.Category(site_en, cat_title)
                if cat.exists():
                    eng_cats.append(cat.title())
                else:
                    print("#"*10 + cat.title() + "#"*10)
                    print('Eng cat doesn\'t exists')

            # Now fetch the corresponding fawiki titles
            # of the english categories of the page if ...
            for x in eng_cats:
                try:
                    x_page = pywikibot.Page(site_en, x)
                    x_item = pywikibot.ItemPage.fromPage(x_page)
                    fatitle = x_item.getSitelink('fawiki')
                    eng_cats_trans.append(fatitle)
                except Exception:
                    print("The \"" + x + "\" is not created in fawiki.")

            # now we determine which categories of fawiki page
            # are local to make an exception for them while updating
            for cat_title in GetCats(curr_page.text, 'fa'):
                orig_fa_cats.append(cat_title)
                cat = pywikibot.Category(site_fa, cat_title)
                if cat.exists():
                    try:
                        curr_cat_item = pywikibot.ItemPage.fromPage(cat)
                        engcat = curr_cat_item.getSitelink('enwiki')
                        # now we can be sure that it has a corresponding
                        # category on english wikipedia which is connected
                        # to it, but we don't need to keep track of them here
                    except Exception:
                        # But we need to keep local cats to exclude them from
                        # update of fawiki page categories, since we don't know
                        # right now if those are in the correct page or not
                        loc_cats.append(cat.title())
                else:
                    print("#"*10 + cat.title() + "#"*10)
                    print('Fa cat doesn\'t exists')

    else:
        print("*"*10+curr_page.title()+"*"*10)
        print('Page doesn\'t exists')

    fa_cats_final = []

    # Adding those eng cats except locals and
    # if it is a cat remover, check if it was
    # in the page before updating
    if remover:
        for x in eng_cats_trans:
            if x not in loc_cats:
                if x in orig_fa_cats:
                    fa_cats_final.append(x)
    else:
        for x in eng_cats_trans:
            if x not in loc_cats:
                fa_cats_final.append(x)

    # Taking care of exceptions
    for x in exc_lines:
        if x in orig_fa_cats:
            fa_cats_final.append(x)

    cats_list = []

    for x in fa_cats_final:
        cats_list.append(x)

    # Taking care of locals
    for x in loc_cats:
        cats_list.append(x)
        print("loc_cats=" + x)

    cats_list.sort()
    cats_text = ""

    for x in cats_list:
        if (x in splitter):
            if len(splitter[x]) > 0:
                cats_text += "[[" + x + "|" + splitter[x] + "]]\n"
            else:
                cats_text += "[[" + x + "]]\n"
        else:
            cats_text += "[[" + x + "]]\n"

    old_page_txt = curr_page.text
    new_page_text = re.sub(r"\[\[[^\[\]:]*?رده:[^\[\]]*?\]\]",
                           "", old_page_txt)
    new_page_text = re.sub(r"\n\s*\n$", "", new_page_text, flags=re.M)
    if len(new_page_text) != 0:
        new_page_text += '\n\n' + cats_text
    elif len(new_page_text) == 0:
        new_page_text += cats_text

    # out = open("out.txt", "a")
    # out.write(new_page_text)
    # out.close()

    # Detailed check to see if we really need an edition:
    old_cats = GetCats(curr_page.text, "fa")
    new_cats = GetCats(new_page_text, "fa")

    if edit_counter < edit_limit:
        if set(old_cats) != set(new_cats):
            if len(new_cats) > 0:
                edit_counter += 1
                print("edit number=" + str(edit_counter))
                curr_page.put(new_page_text, "حذف آزمایشی رده‌های اضافه")
