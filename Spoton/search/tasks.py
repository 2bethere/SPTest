import datetime

from celery import shared_task

from scrapy.crawler import Crawler
from spiders.cspider import CSpider
from scrapy import log, project, signals
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings
from models import Site
from django.db.utils import InterfaceError
from django import db


class UrlCrawlerScript(Process):
        def __init__(self, spider):
            Process.__init__(self)
            settings = get_project_settings()
            self.crawler = Crawler(settings)

            if not hasattr(project, 'crawler'):
                self.crawler.install()
                self.crawler.configure()
                self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
            self.spider = spider

        def run(self):
            self.crawler.crawl(self.spider)
            self.crawler.start()
            reactor.run()

@shared_task
def run_spider(name="boston", allowed_domains={}, start_urls={}, pagelimit=100):
    spider = CSpider(name=name, allowed_domains=allowed_domains, start_urls=start_urls, pagelimit=pagelimit)
    crawler = UrlCrawlerScript(spider)
    siteobj = Site.objects.filter(domain=allowed_domains[0])[0]
    siteobj.last_update = datetime.datetime.utcnow()
    try:
        siteobj.save()
    except InterfaceError:
        db.connection.close()
        siteobj.save()
    crawler.start()
    crawler.join()
