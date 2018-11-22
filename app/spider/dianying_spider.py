import requests, json, jsonpath, pymysql, re, time
from fake_useragent import UserAgent
from lxml import etree
from datetime import datetime
from app.models import Movie, Tag, db


class HtmlDownloader(object):

    def __init__(self):
        self.ua = UserAgent()
        self.url_list = None
        self.movie = {}

    def start_request(self, url):
        if not url:
            return None
        user_agent = self.ua.random
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None

    def download(self, url):
        """
        接受url， 进行请求，返回请求结果
        :param url:
        :return:
        """
        user_agent = self.ua.random
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None

    def parse_url(self, response):
        """
        解析相应中的url地址
        :param response:
        :return: 返回url列表
        """
        if not response:
            return None
        html = etree.HTML(response)
        self.url_list = html.xpath(r'//div[@class="wrap"]/div[@class="box clear"]/table/tbody/tr/td[@class="l"]/a/@href')#.extract()
        # print(url_list)
        # return url_list

    def parse_movie_url(self, response):
        """
        解析电影播放url
        :param response: 电影详情的响应
        :return:
        """
        if not response:
            return None
        html = etree.HTML(response)
        try:
            movie_name = html.xpath(r'//div[@class="contentMain"]/div["videoDetail"]/li[1]/text()[2]')[0]#.extract_first()
            if self.check_is_exist_movie(movie_name):
                return None
            self.movie['name'] = movie_name  # 电影名字
        except Exception as e:
            return None
        # 电影url
        try:
            url = html.xpath(r'//div[@class="contentURL"]/div[@class="movievod"]/ul/li[2]/text()')[0]#.extract_first()
            if not url.endswith('.m3u8'):
                url = html.xpath(r'//div[@class="contentURL"]/div[@class="movievod"]/ul/li[4]/text()')[0]#.extract_first()
            self.movie['url'] = url
        except Exception as e:
            print(e)
            self.movie = {}
            return None
        # 电影封面
        self.movie['cover'] = html.xpath(
            r'//div[@class="videoPic"]/img/@src'
        )[0]#.extract_first()
        # 电影主演
        try:
            self.movie['actors'] = html.xpath(r'//div[@class="contentMain"]/div["videoDetail"]/li[4]/text()[2]')[0]#.extract_first()
        except Exception as e:
            print(e)
            self.movie['actors'] = ''
        # 导演
        try:
            self.movie['director'] = html.xpath(r'//div[@class="contentMain"]/div["videoDetail"]/li[5]/text()[2]')[0]#.extract_first()
        except Exception as e:
            self.movie['director'] = ''
        # tags
        try:
            self.movie['tags'] = html.xpath(r'//div[@class="contentMain"]/div["videoDetail"]/li[6]/div[@class="left"]/text()[2]')[0]#.extract_first()
        except Exception as e:
            print(e)
            self.movie['tags'] = ''
        # 地区
        try:
            self.movie['area'] = html.xpath(r'//div[@class="contentMain"]/div["videoDetail"]/li[7]/div[@class="right"]/text()[2]')[0]#.extract_first()
        except Exception as e:
            print(e)
            self.movie['area'] = ''
        # 上映时间
        try:
            self.movie['release_time'] = html.xpath(r'//div[@class="contentMain"]/div["videoDetail"]/li[8]/div[@class="right"]/text()[2]')[0]#.extract_first()
        except Exception as e:
            print(e)
            self.movie['release_time'] = ''
        # 豆瓣评分
        try:
            self.movie['rating'] = html.xpath(r'//div[@class="contentMain"]/div["videoDetail"]/li[9]/div[@class="right"]/text()[2]')[0]#.extract_first()
        except Exception as e:
            self.movie['rating'] = ''
        # 剧情介绍
        try:
            info = html.xpath(r'//div[@class="contentNR"]/div[@class="movievod"]/p/text()')#.extract()
            self.movie['info'] = '/n'.join(info)
        except Exception as e:
            self.movie['info'] = ''

        return True

    def insert_movie_to_mysql(self):
        """
        将电影信息插入mysql中
        :param tag_type_dict:
        :return:
        """
        if self.movie != {}:
            movie = Movie(
                name=self.movie['name'],
                url=self.movie['url'],
                release_time=self.movie['release_time'],
                area=self.movie['area'],
                introduction=self.movie['info'],
                actors=self.movie['actors'],
                director=self.movie['director'],
                rating=self.movie['rating'],
                cover=self.movie['cover'],
                addtime=datetime.now(),
            )
            print(self.movie['tags'])
            if self.movie['tags']:
                tag = Tag.query.filter_by(name=self.movie['tags'][:2]).first()
                if tag:
                    movie.tags.append(tag)
                else:
                    new_tag = Tag(name=self.movie['tags'][:2], addtime=datetime.now())
                    db.session.add(new_tag)
                    db.session.commit()
                    movie.tags.append(new_tag)

            try:
                db.session.add(movie)
                db.session.commit()
                print('已成功插入: {}'.format(movie.name))
            except Exception as e:
                print(e)
                db.session.rollback()

    def check_is_exist_movie(self, name):
        """
        验证数据库是否存在该电影, 如果存在检测url是否为.m3u8类型,如果不是,尝试转换
        :return:
        """
        movie = Movie.query.filter(Movie.name == name).first()
        if movie and not movie.url.endswith('.m3u8'):
            r = self.download(movie.url)
            html = etree.HTML(r)
            try:
                pattern = re.compile(r'redirecturl = "(http://.*?.com)"')
                base_url = pattern.search(r).group(1)
                pattern2 = re.compile(r'main = "(/.*?\.m3u8)\?.*?"')
                secend_url = pattern2.search(r).group(1)
                movie.url = base_url+secend_url
                db.session.add(movie.url)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
        return movie


def add_movie():
    """
    控制爬虫主程序
    :return:
    """
    scrapy = HtmlDownloader()
    base_url = 'http://www.jingpinzy.net'
    # page = 0
    for page in range(1, 447):
        url = "http://www.jingpinzy.net/?m=vod-index-pg-{}.html".format(str(page))
        r = scrapy.start_request(url)
        # time.sleep(2)
        # 电影详情页url
        scrapy.parse_url(r)
        print(scrapy.url_list)
        # http://www.jingpinzy.net/?m=vod-detail-id-25501.html
        # 电影详情页下载页面
        for url in scrapy.url_list:
            r = scrapy.download(base_url + url)
            # 电影播放地址和电影信息
            info = scrapy.parse_movie_url(r)
            if not info:
                break
            # time.sleep(2)
            scrapy.insert_movie_to_mysql()


if __name__ == '__main__':
    add_movie()
    # scrapy = HtmlDownloader()
    # url = 'http://vip.yingshidaqian.com/share/QvRDvqY0vm7Q2fwr'
    # r = scrapy.download(url)
    # pattern = re.compile(r'redirecturl = "(http://.*?.com)"')
    # base_url = pattern.search(r).group(1)
    # pattern2 = re.compile(r'main = "(/.*?\.m3u8)\?.*?"')
    # secend_url = pattern2.search(r).group(1)
    # movie.url = base_url + secend_url

