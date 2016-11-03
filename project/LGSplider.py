# _*_ coding:utf-8 _*_

import urllib2
from bs4 import BeautifulSoup
import random
import time

# 存放职责列表
dutyList = []

# 爬取每页的网页内容
def requestContent(url,num):
	# 生成[python]30页的内容
	if url.endswith('html'):
		#print("正在爬取\033[0;31;1m %d\033[0m个职位详情"%num)
		pass
	else:
		print("正在爬取第"+ str(num) + "个页面")
		print("正在获取公司的信息中,请稍等......")


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
	    'Host':"www.lagou.com",
	    'User-Agent':rand_head,
	    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	    'Connection':'keep-alive'
	}

	# 带着请求头部的信息去加载url
	req = urllib2.Request(url, headers = send_headers)
	# 获取了网页内容,格式为.html
	content = urllib2.urlopen(req)
	html = content.read()
	# 返回
	return html

# 获取拉钩网的招聘职责信息
def getDetailInfo(content):
	workList = []
	# 调用bs4来爬取内容
	# 职责
	soup  = BeautifulSoup(content,"html.parser")
	ddList = soup.select('dd[class="job_bt"]')
	for list1 in ddList:
		# 获取P标签所有的内容
		dutyList.append(list1.get_text())


	# 爬取工作地址
	ddList1 = soup.select('dd > h4')
	addr = ddList1[1].string
	# print(addr)
	#工作地址详情
	divList = soup.select('div[class="work_addr"]')[0]
	aList = divList.select('a')
	work = ""
	for workAddr in aList:
		if workAddr.string != None:
			work += workAddr.string
	# 具体地址
	inputList = soup.select('input')

	# 拼接成具体的公司地址
	workAddress = "%s:%s-%s"%(addr, work, inputList[3]['value'])
	# workList.append(workAddress)
	return workAddress

# 获取拉钩网下的薪资,公司以及招聘职责url
def getInfo(content):
	salaryList = []
	companyList = []
	workList = []
	# 调用bs4来爬取内容
	soup  = BeautifulSoup(content,"html.parser")
	# liList = soup.select(' .con_list_item')
	liList = soup.select('li[class="con_list_item"]')
	# 循环列表,拿到每一个li标签,然后进行属性的查找
	for list1 in liList:
		company = list1['data-company'].encode("utf-8")
		salary = list1['data-salary'].encode("utf-8")
		companyList.append(company)
		salaryList.append(salary)

	# 获取详情,通过a标签下的class="position_link获取了,然后进行转码,
	# 将开始的//替换为http://,再次通过urllib去读取
	aList = soup.select('a[class="position_link"]')
	i = 1
	for list2 in aList:
		link = list2['href'].encode("utf-8")
		link = link.replace("//","http://")
		content = requestContent(link, i)
		i += 1
		workAddr = getDetailInfo(content)
		workList.append(workAddr.encode("utf-8"))

	# 将保存公司名称,地址,以及薪资的列表传入到一个函数中,防止使用全局变量有修改,通过局部变量来修改
	printDetailInfo(companyList, salaryList, workList,dutyList)
	#print("dutyList:%s"%dutyList[0])

# 将信息写入company.txt文档中
def printDetailInfo(list1, list2, list3,list4):
	# print("正在获取公司的信息中,请稍等......")
	try:
		companyInfo = open("/Users/lvhaidong/Desktop/basicProject/project/text/company.txt",'w')

		for x in range(len(list1)):
			#print("%d. \033[0;31;1m公司名称:\033[0m%s \033[0;31;1m薪资:\033[0m%s \033[0;31;1m地址:\033[0m%s" %(x + 1 , list1[x], list2[x], list3[x]))
			if x <= 100:
				companyInfo.write("%d."%(x + 1))
				companyInfo.write("公司名称:%s"%list1[x])
				companyInfo.write("\t薪资:%s"%list2[x])
				companyInfo.write("\t%s"%list3[x])
				companyInfo.write("\t%s"%dutyList[x].encode("utf-8"))
				companyInfo.write("\n--------------------------------------------------------------------------\n")
	except Exception as e:
		print(e)
	finally:
		companyInfo.close()
		print("写入文件完毕!!")

if __name__ == "__main__":
	# 一共是30页,爬取30次
	for x in range(1, 2):
		url = "http://www.lagou.com/zhaopin/Python/%d/?filterOption=3"%x
		# 传入页数
		content = requestContent(url,x)
		getInfo(content)
		# 防止程序不断的循环,设置一个等待时间
		time.sleep(1)
