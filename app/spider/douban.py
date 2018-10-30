import requests, json, jsonpath, pymysql, re, time
from fake_useragent import UserAgent
from lxml import etree
from datetime import datetime
from app.models import Movie, Tag, db


class HtmlDownloader(object):

    def __init__(self):
        self.ua = UserAgent()

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
        解析标签和标签对应的type编号，这个编号在请求各类型的电影时用到
        :param response:
        :return:
        """
        tag_type_dict = {}
        html = etree.HTML(response)
        # tag_list = html.xpath(r"//div[@class='types']/span/a/text()")
        tag_url_list = html.xpath(r'//div[@class="types"]/span/a/@href')
        for url in tag_url_list:
            pattern = re.compile(r'type_name=([\u4e00-\u9fa5]*?)&.*?type=(\d*?)&')
            m = pattern.search(url)
            tag_type_dict[m.group(1)] = m.group(2)
        return tag_type_dict

    def parse_movie_info(self, response):
        """
        response对象是json格式的电影信息
        :param response:
        :return:
        """
        obj_list = json.loads(response)
        for jsonobj in obj_list:
            movie = Movie(name=jsonobj['title'],
                          url=jsonobj['url'],
                          release_time=jsonobj['release_date'],
                          area='/'.join(jsonobj['regions']),
                          actors='/'.join(jsonobj['actors']),
                          cover=jsonobj['cover_url'],
                          rating=jsonobj['score'],
                          play_num=jsonobj['vote_count'])
            try:
                db.session.add(movie)
                db.session.commit()
                print('成功插入电影{}'.format(movie.name))
            except Exception as e:
                db.session.rollback()
                print(e)
            print(jsonobj['types'])
            for movie_tag in jsonobj['types']:
                print(movie_tag)
                tag = Tag.query.filter_by(name=movie_tag).first()
                movie.tags.append(tag)
                try:
                    db.session.add(movie)
                    db.session.commit()
                    print('成功插入关系{0} 和 {1}'.format(movie.name, tag.name))
                except Exception as e:
                    db.session.rollback()
                    print(e)

    def insert_to_mysql_tag(self, tag_type_dict):
        """
        将标签数据写到tag表中
        :param tag_type_dict:
        :return:
        """
        for tag_name in tag_type_dict.keys():
            tag = Tag(name=tag_name)
            try:
                db.session.add(tag)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)


def create_movie_tag_url(tag_type_dict, scrapy):
    for type_num in tag_type_dict.values():
        url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start=20&limit=20'.format(type_num)
        r = scrapy.download(url)
        time.sleep(10)
        scrapy.parse_movie_info(r)


def add_movie():
    scrapy = HtmlDownloader()
    url = "https://movie.douban.com/chart"
    r = scrapy.start_request(url)
    # 返回类型和对应的类型编号
    tag_type_dict = scrapy.parse_url(r)
    # 将标签写到tag表中
    scrapy.insert_to_mysql_tag(tag_type_dict)
    # 构造豆瓣分类url并将数据放入数据库中
    create_movie_tag_url(tag_type_dict, scrapy)


if __name__ == '__main__':
    add_movie()

