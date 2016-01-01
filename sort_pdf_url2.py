# sort the pdf download url  format : "sn##category##pdf_url"

import geekbook
import sys


f = open("detailurl.txt","r");
pdf_url_file = open('pdf_url_file.txt','a+')

domain = "https://www.geekbooks.me"
category = ""
file_line_num = int(sys.argv[1]) - 1
serial_number = int(sys.argv[2])

i = 0
for line in f:
    i += 1
    print "origin line %s : %s " % (i,line)
    if i <= file_line_num:
        if line.find("/book/view/") == -1:
            category = line.strip()
        continue

    file_line_num += 1
    if line.find("/book/view/") != -1:
        pdf_url_list = geekbook.list_pdf_url_by_book_detail_url(domain + line)
        for pdf_url in pdf_url_list:
            serial_number += 1
            sorted_pdf_url = str(serial_number) + "##" + category + "##" + domain + pdf_url
            print sorted_pdf_url
            pdf_url_file.write(sorted_pdf_url+'\n')
    else:
        category = line.strip()

f.close()
pdf_url_file.close()




