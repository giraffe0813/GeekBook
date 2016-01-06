from pyPdf import PdfFileReader
import os, sys
import subprocess
from GeekBook.conf import *


if __name__ == "__main__":
    f = open("./damaged.txt", "a+")
    p = subprocess.Popen("find " + conf_books_dir + "/" + "  -type f -name '*.pdf'", stdout=subprocess.PIPE,
                         shell=True)
    output, err = p.communicate()
    if len(output) == 0:
        print 'no .pdf files to deal'
        sys.exit()
    # remove the last \n
    output = output[:-1]
    file_list = output.split("\n")
    for book in file_list:
        # print book
        try:
            mypdf = PdfFileReader(file(book, 'rb'))
        except:
            print 'invalid pdf >', book
            os.remove(book)
            # write to file
            f.write(book + '\n')
    f.close()