import time
import urllib.request as request

from bs4 import BeautifulSoup

from spider.DesktopImg import DesktopImg


def download_img(img):
	data = request.urlopen(img.download_url)
	img_data = data.read()
	try:
		with open(img.get_full_name(), "wb") as code:
			code.write(img_data)
			code.close()
			print("下载完毕", img.name, img.download_url)
	except OSError:
		print("文件存储错误，文件名为：", img.get_full_name(), "下载地址：", img.download_url)
		pass
	time.sleep(1)


def mkdir(path):
	# 引入模块
	import os

	# 去除首位空格
	path = path.strip()
	# 去除尾部 \ 符号
	path = path.rstrip("\\")

	# 判断路径是否存在
	# 存在     True
	# 不存在   False
	isExists = os.path.exists(path)

	# 判断结果
	if not isExists:
		# 如果不存在则创建目录
		# 创建目录操作函数
		os.makedirs(path)

		print(path + ' 创建成功')
		return True
	else:
		# 如果目录存在则不创建，并提示目录已存在
		print(path + ' 目录已存在')
		return False


class SimpleDeskTopSpider:

	def __init__(self, save_path):
		self.save_path = save_path
		self.website_url = "http://simpledesktops.com"

	def run(self, next_page_url="/browse/1/"):
		mkdir(self.save_path)
		rq = request.Request(self.website_url + next_page_url)
		images_page = request.urlopen(rq)
		page_soup = BeautifulSoup(images_page, "lxml")
		img_div_list = page_soup.find_all(name="div", attrs={"class": "desktop"})
		self.get_img_page(img_div_list)
		next_page = page_soup.find_all(name="a", attrs={"class": "back"})
		if len(next_page) > 0:
			next_page_url = next_page[0]["href"]
			self.run(next_page_url)

	def get_img_page(self, img_div_list):
		for img_div in img_div_list:
			tag_a = img_div.a
			img_url = self.website_url + tag_a["href"]
			img_page = request.urlopen(img_url)
			img_soup = BeautifulSoup(img_page, "lxml")
			tag_a = img_soup.find_all(name="div", attrs={"class": "desktop"})[0].a
			download_url = self.website_url + tag_a["href"]
			suffix = str(tag_a.img["src"])[-4:]
			img_name = str(tag_a.img["title"]).replace("/", "-") + suffix
			download_img(DesktopImg(img_name, download_url, self.save_path))
