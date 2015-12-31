# sort the pdf download url  format : "sn##category##pdf_url"

import geekbook

f = open("detailurl.txt","r");
pdf_url_file = open('pdf_url_file.txt','w+')

domain = "https://www.geekbooks.me"
category = ""
serial_number = 0
for line in f:
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




