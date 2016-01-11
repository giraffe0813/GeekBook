# -*- coding: utf-8 -*-
import traceback
import urllib2
import re
from bs4 import BeautifulSoup
import MySQLdb
import time
import base64
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from GeekBook.conf import conf_host, conf_user, conf_passwd

conn = MySQLdb.connect(host=conf_host, user=conf_user, passwd=conf_passwd, db="geekbookadmin", charset="utf8")

cur = conn.cursor()

category_url = "https://www.geekbooks.me/category"
pdf_list = []
ISOTIMEFORMAT = '%Y-%m-%d %X'
detail_info_list = []


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
    #
    img_src = soup.find("table", class_="book-info").find("td", class_="cover").find("img").attrs['src']
    img_base64 = base64.b64encode(urllib2.urlopen('https://www.geekbooks.me' + img_src).read())
    book_desc = soup.find("p", class_="desc").text
    pdf_file_name = soup.find("div", class_="download").find("a").attrs['href'].split('/')[-1]
    authors = ""
    author_more_str = 'more »'.decode('utf-8')
    author_less_str = '« less'.decode('utf-8')
    if soup.find("p", class_="author").findAll("a") is not None:
        for author in soup.find("p", class_="author").findAll("a"):
            if author_less_str not in author.string and author_more_str not in author.string:
                authors += author.string + ","
    # tag
    tags = ""
    # soup.findAll("a", class_="tag")
    if soup.findAll("a", class_="tag") is not None:
        for tag in soup.findAll("a", class_="tag"):
            tags += tag.string + ","
    #
    categorys = ""
    if soup.find("ul", class_="breadcrumbs").findAll("li")[2:-1] is not None:
        for category in soup.find("ul", class_="breadcrumbs").findAll("li")[2:-1]:
            categorys += category.string + ","
    #
    info_html = soup.find("td", class_="info")
    title = info_html.h1.string
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

    print "title: " + title
    print "Publisher: " + info_map["Publisher"]
    print "ISBN: " + info_map["ISBN"]
    print "Pages: " + info_map["Pages"]
    print "Year: " + info_map["Year"]
    print "tags: " + tags
    print "authors: " + authors
    print "categorys: " + categorys
    print "pdf_file_name: " + pdf_file_name
    # print "desc: " + str(book_desc)
    book_desc = book_desc.encode(encoding='UTF-8', errors='replace')
    print "======================="
    cur.execute(
        "insert into books_book (title,authors, isbn,pages,publisher,publish_year, tags,come_from,cover,pdf_file_name,description,categorys,qiniu_key,created_at) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (title, authors, info_map["ISBN"], info_map["Pages"], info_map["Publisher"], info_map["Year"], tags, 0,
         img_base64, pdf_file_name, book_desc.decode('utf-8'), categorys, "", time.strftime(ISOTIMEFORMAT, time.localtime())))
    conn.commit()


if __name__ == "__main__":
    f = open("../data/errorurl.data", "r")

    books = []
    destDir = ""
    tmp = ""
    for line in f:
        try:
            if line.startswith("/"):
                get_book_detail("https://www.geekbooks.me" + line)
        except Exception, e:
            error_f = open("../data/errorurl.data", "ab")
            error_f.write(line)
            error_f.close()
            exstr = traceback.format_exc()
            print exstr
            continue
    f.close()
