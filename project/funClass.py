# _*_ coding:utf-8 _*_

import urllib
import urllib2
from bs4 import BeautifulSoup
import random
import time

# 获取网页内容
class webPage(object):
	"""抓取网页内容"""

	# hostURL 指的是主机的地址
	def __init__(self,  hostURL = "www.3jy.com"):
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
		self.head = \
		{
		    'Host':hostURL,
		    'User-Agent':rand_head,
		    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		    'Connection':'keep-alive'
		}

	# 通过urllib2来拿到网页内容
	def getHtmlContent(self, url):
		# 带着请求头部的信息去加载url
		req = urllib2.Request(url, headers = self.head)
		# 获取了网页内容,格式为.html
		content = urllib2.urlopen(req)
		html = content.read()
		# 返回
		return html

# 通过标签来拿到相应的内容
class tagContent(object):
	"""通过标签来获取对应的内容"""
	def __init__(self, content):
		self.soup = BeautifulSoup(content, "html.parser")

	# 通过标签来进行查找属性
	def searchTag(self):
		# 1.先获取顶层的div
		divList = self.soup.select('div[class="xh clearfix"]')
		# 定义一个空的列表,保存img,当大于50时,就不在进行保存
		imagesList = []
		titlelist = []

		# 2.遍历顶层的div列表
		for list1 in divList:
			# 2.1 从list1对象中再次查找下一个div,然后类属性为listpic
			divList2 = list1.select('div[class="listpic"]')

			# 2.2因为没有图片的div,再次从divList2中转换对象时就会报错(列表越界)
			if len(divList2) != 0:
				divList2 = divList2[0]
				# 2.3查找divList2对象下的img属性
				imgList = divList2.select('img')

				# 2.4遍历imglist列表,保存的是每一个的对象
				for img in imgList:
					# 2.5保存50张图片
					if len(imagesList) <= 50:
						# 2.6将unicode码转换为utf-8
						title = img['title'].encode("utf-8")
						# 2.7去掉标题中左边的_
						title = title.replace("_","")

						# 将unicode编码成utf-8
						image = img['src'].encode("utf-8")
						imagesList.append(image)
						print("-" * 90)
						print("\033[0;31;1m%d. 下载的图片链接为\033[0m :\n%s,\n\033[0;31;1m标题为\033[0m:%s"%(len(imagesList), image, title))
						print("-" * 90)

				# 2.8查找list1对象下查找p标签
				divList3 = list1.select('p[class="textp"]')
				# 2.9遍历p列表对象,最后将字符串拿出来转换成utf-8
				for pTitle in divList3:
					if len(titlelist) <= 50:
						pTitle = pTitle.string.strip().encode("utf-8")
						titlelist.append(pTitle)
				# 3.保存到本地项目文件夹下
				# urllib.urlretrieve(image, filename='/Users/lvhaidong/Desktop/basicProject/images/%s%s.jpg'%(title,pTitle))
		return(imagesList, titlelist)


if __name__ == '__main__':
	for x in range(1,2):
		url = "http://www.3jy.com/index/%d.html"%x
		# if x == 1:
		# 	url = "http://www.3jy.com/egao/"
		# else:
		# 	url = "http://www.3jy.com/egao/%d.html"%x
		print("*" * 90)
		print("正在爬取第%d页,对应的url:%s"%(x, url))
		print("*" * 90)

		# 抓取网页内容的类
		content = webPage()
		info = content.getHtmlContent(url)

		# 通过属性来进行遍历的类
		tag = tagContent(info)
		tag.searchTag()

		time.sleep(1)