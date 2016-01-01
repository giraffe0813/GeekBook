#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import urllib2
import re
import cookielib
import os
import threadpool


class Book():
    def __init__(self, dir, url, down_url):
        self.dir = dir
        self.url = url
        self.down_url = down_url

    def download(self):
        download_pdf("https://www.geekbooks.me" + self.url, self.dir,self.down_url)


# deprecated
def read_save_cookie(url):
    filename = 'cookie4geek.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    response = opener.open(url)
    cookie.save(ignore_discard=True, ignore_expires=True)


# get page from url
def get_html(url):
    page = urllib2.urlopen(url)
    html = page.read()
    return html


# get url which end of 'pdf' and download
def download_pdf(url, category,down_url):
    # if category directory is not exist, create

    parent_path = "book/"
    if os.path.isdir(parent_path + category):
        pass
    else:
        os.makedirs(parent_path + category)

    # create instance of MozillaCookieJar
    cookie = cookielib.MozillaCookieJar()
    # get cookie from file
    cookie.load('cookie4geek.txt', ignore_discard=True, ignore_expires=True)
    for item in cookie:
        print item.name
        print item.value
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    # add header
    opener.addheaders = [('User-agent', 'Mozilla/5.0'), ("Referer", url)]

    print(down_url)
    file_name = url.split('/')[-1] + ".pdf"
    u = opener.open(down_url)
    print("preparing......")
    # f with directory
    f = open(parent_path + category + "/" + file_name, 'wb')
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



def downloadTask(book):
    book.download()


if __name__ == "__main__":
    # processing all books
    f = open("../txt/merge_pdf_url_file.txt", "r")
    books = []
    for line in f:
        merge_list = line.split('##')
        # desDir
        book = Book(merge_list[1], merge_list[3].strip(),merge_list[2])
        books.append(book)

    # books > download with full speed
    for book in books:
        print book.dir, "#", book.url , "#" ,book.down_url
        # book.download()
    pool = threadpool.ThreadPool(20)
    reqs = threadpool.makeRequests(downloadTask, books)
    [pool.putRequest(req) for req in reqs]
    pool.wait()



