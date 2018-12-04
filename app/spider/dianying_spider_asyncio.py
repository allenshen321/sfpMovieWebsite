# 最大资源网电影资源
import re
import asyncio
import aiohttp
from datetime import datetime

from fake_useragent import UserAgent
from lxml import etree
from app.models import Movie, Tag, db


class HtmlDownloader(object):

    def __init__(self):
        self.ua = UserAgent()
        self.url_list = None
        self.movie = {}
        self.count = 0  # 记录成功保存电影数目
        self.err_count = 0  # 记录出错数
        self.req_count = 0  # 请求数

    async def start_request(self, url, session):
        self.req_count += 1
        print('第{}次请求'.format(self.req_count))
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
        try:
            r = await session.get(url, headers=headers)
            if r.status == 200:
                r.encoding = 'utf-8'
                return await r.text()
        except asyncio.TimeoutError as e:
            self.err_count += 1
            print(e)
            print('请求出错数{}'.format(self.err_count))
            return None
        return None

    async def download(self, url, session):
        """
        接受url， 进行请求，返回请求结果
        :param url:
        :param session aiohttp.ClientSession对象
        :return:
        """
        self.req_count += 1
        print('第{}次请求'.format(self.req_count))
        user_agent = self.ua.random
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        try:
            r = await session.get(url, headers=headers)
            if r.status == 200:
                r.encoding = 'utf-8'
                return await r.text()
        except asyncio.TimeoutError as e:
            self.err_count += 1
            print(e)
            print('请求出错数{}'.format(self.err_count))
            return
        return None

    def parse_url(self, response):
        """
        解析相应中的url地址
        :param response: 请求返回的结果
        :return: 返回url列表
        """
        if not response:
            return None
        html = etree.HTML(response)
        self.url_list = html.xpath(r'//div[@class="wrap"]/div[@class="box clear"]/table/tbody/tr/td[@class="l"]/a/@href')
        # print(url_list)
        # return url_list

    async def parse_movie_url(self, response, session):
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
            is_exist = await self.check_is_exist_movie(movie_name, session)
            if is_exist:
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
        from app import creat_app, db
        from app.models import Movie, Tag

        app = creat_app('default')
        with app.app_context():
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
                # print(self.movie['tags'])
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
                except Exception as e:
                    print(e)
                    db.session.rollback()
                else:
                    self.count += 1
                    print('已成功插入: {0}, 这是第{1}部电影'.format(movie.name, self.count))

    async def check_is_exist_movie(self, name, session):
        """
        验证数据库是否存在该电影, 如果存在检测url是否为.m3u8类型,如果不是,尝试转换
        :return:
        """
        movie = Movie.query.filter(Movie.name == name).first()
        if movie and not movie.url.endswith('.m3u8'):
            r = await self.download(movie.url, session)
            html = etree.HTML(r)
            try:
                pattern = re.compile(r'redirecturl = "(http://.*?.com)"')
                base_url = pattern.search(r).group(1)
                pattern2 = re.compile(r'main = "(/.*?\.m3u8)\?.*?"')
                secend_url = pattern2.search(r).group(1)
                movie.url = base_url+secend_url
                db.session.add(movie)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
        return movie

    async def download_one(self, url, base_url, session):
        """
        下载单个电影
        :param url: 单个电影的url
        :return:
        """
        resp = await self.download(base_url + url, session)
        # 电影播放地址和电影信息
        info = await self.parse_movie_url(resp, session)
        if not info:
            return
        else:
            loop = asyncio.get_event_loop()
            loop.run_in_executor(None, self.insert_movie_to_mysql)
            # self.insert_movie_to_mysql()

    async def download_one_page(self, page, base_url, session):
        """
        下载一个页面的电影
        :param url:
        :return:
        """
        # print('正在保存{}页'.format(str(page)))
        url = "http://www.jingpinzy.net/?m=vod-index-pg-{}.html".format(str(page))
        r = await self.start_request(url, session)
        # 电影详情页url
        self.parse_url(r)
        # 电影详情页下载页面
        if self.url_list:
            to_do = [self.download_one(url, base_url, session) for url in self.url_list]
            await asyncio.wait(to_do)


async def add_movie_coro():
    """爬虫下载协程管理逻辑"""
    scrapy = HtmlDownloader()
    base_url = 'http://www.jingpinzy.net'
    async with aiohttp.ClientSession() as session:
        to_do = [scrapy.download_one_page(page, base_url, session) for page in range(1, 447)]
        await asyncio.wait(to_do)
    print('共新增电影: {} 部电影'.format(scrapy.count))


def add_movie():
    """
    控制爬虫主程序
    :return:
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(add_movie_coro())
    loop.close()
    print('下载完成')


if __name__ == '__main__':
    add_movie()
