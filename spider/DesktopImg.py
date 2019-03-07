class DesktopImg:

	def __init__(self, name, download_url, path="E:/img"):
		self.name = name
		self.path = path
		self.download_url = download_url

	def set_name(self, name):
		self.name = name

	def set_path(self, path):
		self.path = path

	def set_download_url(self, download_url):
		self.download_url = download_url

	def get_full_name(self):
		return self.path + "/" + self.name

