import urllib2
import re
from bs4 import BeautifulSoup
import MySQLdb
import time
from GeekBook.conf import conf_host, conf_user, conf_passwd

conn = MySQLdb.connect(host=conf_host, user=conf_user, passwd=conf_passwd, db="geekbookadmin",charset="utf8")
cur = conn.cursor()


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

    f = open("./data/detailurl.data", "ab")
    f.write(category)
    f.write('\n')

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
        f.write('\n')
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

def get_book_detail(url):
    """
    get book detail,include author,title,and so on
    :param url:
    :return:
    """
    page = urllib2.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html)
    info_html = soup.find("td", class_="info")
    title = info_html.h1.string
    authors_href = info_html.findAll("a")
    authors = ""
    for item in authors_href:
        authors += item.string
    p = info_html.findAll("p")
    p.remove(p[0])
    p.remove(p[4])
    info_map = {}
    for item in p:
        if item.string is None:
            continue
        info = item.string.split(": ")
        if len(info) >= 2:
            info_map[info[0]] = info[1]
    print authors
    print title + info_map["Publisher"] +info_map["ISBN"] + info_map["Pages"] + info_map["Year"]
    cur.execute("insert into books_book (title,authors,isbn,pages,publisher,publish_year, tags,come_from) values (%s,%s,%s,%s,%s,%s,%s,%s)",(title,authors,info_map["ISBN"],info_map["Pages"],info_map["Publisher"],info_map["Year"],"",0))
    conn.commit()

if __name__ == "__main__":
    f = open("../data/detailurl.txt", "r")
    books = []
    destDir = ""
    tmp = ""
    for line in f:
        try:
            if line.startswith("/"):
                get_book_detail("https://www.geekbooks.me" + line)
        except:
            continue






