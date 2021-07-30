import scrapy
from env import xggl


class XgglSpider(scrapy.Spider):
    name = 'xggl'
    allowed_domains = ['hnie.edu.cn']

    custom_settings = {'LOG_LEVEL': 'WARNING', 'LOG_FILE': 'xggl.log'}

    def start_requests(self):
        yield scrapy.FormRequest('http://xggl.hnie.edu.cn/website/login',
                                 self.parse_login,
                                 formdata={
                                     'username': xggl['user'],
                                     'password': xggl['passwd_key']
                                 })

    def parse_login(self, _):
        yield scrapy.FormRequest(
            'http://xggl.hnie.edu.cn/content/student/temp/zzdk',
            formdata=xggl['formdata'])

    def parse(self, response):
        self.logger.warning(response.json())
