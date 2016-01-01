import geekbook

f = open("../txt/demo_book.txt","r");

for line in f:
    geekbook.download_pdf("https://www.geekbooks.me"+line,"")






