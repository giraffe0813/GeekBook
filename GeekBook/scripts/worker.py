#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import re
import cookielib
import os
import threadpool
from pyPdf import PdfFileReader
from GeekBook.util.log_util import logger
from GeekBook.conf import *


class Book():
    def __init__(self, dir, url):
        self.dir = dir
        self.url = url

    def download(self):
        download_pdf(self.url, self.dir)


# get page from url
def get_html(url):
    page = urllib2.urlopen(url)
    html = page.read()
    return html


def list_pdf_url_by_book_detail_url(book_detail_url):
    html = get_html(book_detail_url)
    reg = r'href="(.+?\.pdf)"'
    imgre = re.compile(reg)
    return re.findall(imgre, html)


def detect_book(dir):
    try:
        PdfFileReader(file(dir, 'rb'))
        return True
    except:
        print 'damage>', dir
        return False


# get url which end of 'pdf' and download
def download_pdf(url, category):
    # add domain
    url = "https://www.geekbooks.me" + url
    # if category directory is not exist, create
    if os.path.isdir(conf_books_dir + category):
        pass
    else:
        os.makedirs(conf_books_dir + category)
    # create instance of MozillaCookieJar
    cookie = cookielib.MozillaCookieJar()
    # get cookie from file
    cookie.load('../data/cookie4geek.data', ignore_discard=True, ignore_expires=True)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    # add header
    opener.addheaders = [('User-agent', 'Mozilla/5.0'), ("Referer", url)]
    for url in list_pdf_url_by_book_detail_url(url):
        logger.info("PageDetailPage> {url}".format(url=("https://www.geekbooks.me" + url)))
        file_name = url.split('/')[-1]
        u = opener.open("https://www.geekbooks.me" + url)
        print "Preparing to download..."
        # f with directory
        if os.path.exists(conf_books_dir + category + "/" + file_name) and detect_book(
                (conf_books_dir + category + "/" + file_name)):
            continue
        f = open(conf_books_dir + category + "/" + file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1)
            print status,
        f.close()


def download_work():
    f = open("../data/detailurl.txt", "r")
    books = []
    destDir = ""
    tmp = ""
    for line in f:
        if not (line.strip()).startswith("/"):
            tmp += "/" + line.strip()
            destDir = tmp
        else:
            # desDir
            book = Book(destDir, line.strip())
            books.append(book)
            tmp = ""
    pool = threadpool.ThreadPool(conf_thread_count)
    reqs = threadpool.makeRequests(lambda book: book.download(), books)
    [pool.putRequest(req) for req in reqs]
    pool.wait()


if __name__ == "__main__":
    download_work()



