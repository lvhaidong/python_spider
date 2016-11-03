# _*_ coding:utf-8 _*_

import urllib2
from bs4 import BeautifulSoup
import random
import time

# 获取网页内容的函数 
# hostURL代表是哪个服务器网址
def getHtmlContent(url):
	'''抓取网页内容'''

	# 伪造浏览器信息
	my_headers = \
	[
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
		'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
	  	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; InfoPath.1',
	  	'Mozilla/4.0 (compatible; GoogleToolbar 5.0.2124.2070; Windows 6.0; MSIE 8.0.6001.18241)',
	  	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
	  	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; Sleipnir/2.9.8)'
  	]
  	# 随机选择一个浏览器
  	rand_head = random.choice(my_headers)
  	# 添加浏览器请求头
	send_headers = \
	{
	    'Host':"book.douban.com",
	    'User-Agent':rand_head,
	    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	    'Connection':'keep-alive'
	}

	# 带着请求头部的信息去加载url
	req = urllib2.Request(url,headers = send_headers)
	# 获取了网页内容,格式为.html
	content = urllib2.urlopen(req).read()
	# 返回
	return content

# 获取豆瓣网中书名,评分,评论人数,以及价格信息
def getInfo(info):
	bookList = []
	authorList = []
	gradeNum = []
	numList = []
	priceList = []

	# 获取soup对象
	soup = BeautifulSoup(info,"html.parser")

	# 获取顶层div,然后根据div去查找a标签,拿出title,然后进行转码
	divList = soup.select('div[class="pl2"]')
	for aList in divList:
		aTagList = aList.select('a')
		for titleList in aTagList:
			bookName = titleList['title'].encode("utf-8")
			if len(bookList) <= 100:
				bookList.append(bookName)

	# 获取p标签,是一个长字符串,然后通过'/'切割成列表,第一个就是作者,最后一个就是价格
	pList = soup.select('p[class="pl"]')
	for stringList in pList:
		list1 =stringList.string.encode("utf-8").split('/')
		author = list1[0].strip()
		price = list1[len(list1) - 1].strip()
		if len(authorList) <= 100:
			authorList.append(author)
			priceList.append(price)


	# 评分
	starList = soup.select('span[class="rating_nums"]')
	for star in starList:
		grade = star.string.encode("utf-8")
		if len(gradeNum) <= 100:
			gradeNum.append(grade)

	# 评分人数
	gradeList = soup.select('span[class="pl"]')
	for people in gradeList:
		num = people.string.encode("utf-8")
		num = num.replace("(","").strip()
		num = num.replace(")","").strip()
		if len(numList) <= 100:
			numList.append(num)
	# print("%d %d %d %d"%(len(authorList),len(gradeList), len(numList), len(priceList)))
	try:
		book = open('/Users/lvhaidong/Desktop/basicProject/text/book.txt','w')
		for x in range( len(bookList)):
			# if x <= len(bookList):
				# print("书名:%s 作者:%s 评分:%s 评分人数:%s 价格:%s"%(bookList[x], authorList[x],gradeNum[x], numList[x], priceList[x]))
			book.write("%d. 图书名称:%s"%(x + 1, bookList[x]))
			book.write("\t\t作者:%s"%authorList[x])
			book.write("\t\t评分:%s"%gradeNum[x])
			book.write("\t评价人数:%s"%numList[x])
			book.write("\t\t价格:%s"%priceList[x])
			book.write("\n--------------------------------------------------------------------------\n")
	except Exception as e:
		print(e)
	finally:
		book.close()
		print("\033[0;31;1m抓取图书完毕\033[0m")


if __name__ == "__main__":
	urlStr = "https://book.douban.com/top250?"
	num = 25
	i = 0
	sum = 0
	for i in xrange(1):
		print("正在爬取%d页内容"% ( i + 1))
		if i == 0:
			url = urlStr+"start=%d"%i
		else:
			sum += num
			url = urlStr+"start=%d"%(sum)
		content = getHtmlContent(url)
		getInfo(content)
		time.sleep(1)

