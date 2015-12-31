import urllib2
import re
import os
import cookielib
import geekbook

category_url = "https://www.geekbooks.me/category"
pdf_list = []


# get all category url
def get_all_category_url(url):

    """
    get all category url
    :param url:
    :return:
    """

    category_page = urllib2.urlopen(url)
    category_html = category_page.read()
    reg = r'href="(/category.+?)"'
    category_re = re.compile(reg)
    category_list = re.findall(category_re, category_html)
    for item in category_list:
        print item
        category = item.split('/')[-1]
        get_all_detail_url("https://www.geekbooks.me" + item, category)


def get_all_detail_url(url, category):
    """
    get all detail url with specific category
    :param url:
    :param category:
    :return:
    """
    # if category directory is not exist, create
    # if os.path.isdir("./" + category):
    #     pass
    # else:
    #     os.mkdir("./" + category)

    f = open("detailurl.txt", "wb")
    f.write(category)

    page = urllib2.urlopen(url)
    html = page.read()
    book_reg = r'href="(/book/view/.+?)"'
    book_re = re.compile(book_reg)
    url_list = re.findall(book_re, html)
    pagination_reg = r'href="(.+?p=\d*)"'
    pagination_re = re.compile(pagination_reg)
    pagination_list = re.findall(pagination_re, html)
    # remove duplicate item
    pagination_list = list(set(pagination_list))

    pagination_list = deal_with_pagination(pagination_list)

    for item in pagination_list:
        page = urllib2.urlopen("https://www.geekbooks.me/category/view/" + category + item)
        html = page.read()
        temp_list = re.findall(book_re, html)
        url_list += temp_list

    url_list = list(set(url_list))
    for item in url_list:
        f.write(item)
    f.close()
    print(url_list)


def deal_with_pagination(pagination_list):

    """
    deal with pagination url
    eg: input [?p=7,?p=3,?p=2]
        ouput [?p=7,?p=6,?p=5,?p=4,?p=3,?p=2]
    :param pagination_list:
    :return:

    """
    result = []
    if pagination_list.__len__() <= 1:
        return pagination_list
    prefix = pagination_list[0].split("&")[0]
    num = []
    for item in pagination_list:
        num.append(int(item.split("=")[-1]))
    num.sort()
    # get last page number
    max_page = num[len(num) - 1]
    while max_page >= 2:
        result.append(prefix + "&p=" + str(max_page))
        max_page -= 1

    return result


get_all_category_url(category_url)





