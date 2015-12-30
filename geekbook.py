import urllib2
import urllib
import re
import cookielib


# deprecated
def readSaveCookie(url):
	filename = 'cookie4geek.txt'
	cookie = cookielib.MozillaCookieJar(filename)
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	response = opener.open(url)
	cookie.save(ignore_discard=True, ignore_expires=True)


# get page from url
def getHtml(url):
	page = urllib2.urlopen(url)
	html = page.read()
	return html

# get url which end of 'pdf' and download
def getPdf(html):
	reg = r'href="(.+?\.pdf)"'
	imgre = re.compile(reg)
	imglist = re.findall(imgre, html)
	#create instance of MozillaCookieJar
	cookie = cookielib.MozillaCookieJar()
	#get cookie from file
	cookie.load('cookie4geek.txt', ignore_discard=True, ignore_expires=True)
	for item in cookie:
		print item.name
		print item.value
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	# add header
	opener.addheaders = [('User-agent', 'Mozilla/5.0'),("Referer","https://www.geekbooks.me/book/view/angularjs-directives-cookbook")]
	
	for url in imglist:
		print("https://www.geekbooks.me" + url)
		file_name = url.split('/')[-1]
    	u = opener.open("https://www.geekbooks.me" + url)
    	print("preparing......")
    	f = open(file_name, 'wb')
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
        	status = status + chr(8)*(len(status)+1)
        	print status,

    	f.close()

#get page from specific url
html = getHtml("https://www.geekbooks.me/book/view/angularjs-directives-cookbook")

getPdf(html)






