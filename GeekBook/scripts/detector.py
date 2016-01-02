from pyPdf import PdfFileReader
import glob

if __name__ == "__main__":
    f = open("./damaged.data", "a+")
    for book in glob.glob("./books/*/*.pdf"):
        try:
            PdfFileReader(file(book, 'rb'))
        except:
            print 'invalid pdf >', book
            f.write(book + '\n')
    f.close()