# sort the pdf download url  format : "sn##category##pdf_url"

import geekbook
import sys


f = open("txt/detailurl.txt","r");
pdf_url_file = open('txt/pdf_url_file.txt','r')
merge_pdf_url_file = open('txt/merge_pdf_url_file.txt','w+')

book_list = []
for line in f:
    if line.find("/book/view/") != -1:
        book_list.append(line)

print book_list.__len__()

pdf_url_list = pdf_url_file.readlines()
print pdf_url_list.__len__()

merge_list = []
if book_list.__len__() == pdf_url_list.__len__():
    i = 0;
    for line in book_list:
        temp = str(line)
        print temp
        merge = pdf_url_list[i].strip() + "##" + temp.strip() + "\n"
        print merge
        merge_list.append(merge)
        i += 1
else:
    print book_list.__len__() + " " + pdf_url_list.__len__()

merge_pdf_url_file.writelines(merge_list)

f.close()
pdf_url_file.close()
merge_pdf_url_file.close()





