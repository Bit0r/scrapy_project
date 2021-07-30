from hashlib import md5

import scrapy
from env import xggl


class XgglSpider(scrapy.Spider):
    name = 'xggl'
    allowed_domains = ['hnie.edu.cn']

    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        'LOG_FILE': 'xggl.log',
    }

    def start_requests(self):
        passwd_hash = md5(xggl['passwd'].encode()).hexdigest()
        if len(passwd_hash) > 5:
            passwd_hash = passwd_hash[:5] + 'a' + passwd_hash[5:]
        if len(passwd_hash) > 10:
            passwd_hash = passwd_hash[:10] + 'b' + passwd_hash[10:]
        passwd_hash = passwd_hash[:-2]

        yield scrapy.FormRequest('http://xggl.hnie.edu.cn/website/login',
                                 self.parse_login,
                                 formdata={
                                     'username': xggl['user'],
                                     'password': passwd_hash
                                 })

    def parse_login(self, _):
        return scrapy.FormRequest(
            'http://xggl.hnie.edu.cn/content/student/temp/zzdk',
            formdata=xggl['formdata'])

    def parse(self, response):
        self.logger.warning(response.json())
