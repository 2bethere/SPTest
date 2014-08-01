import scrapy, pickle, urlparse, parsedatetime, re, datetime
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import SspiderItem
from ..models import Site, Event
from celery.utils.log import get_task_logger
from scrapy.linkextractor import IGNORED_EXTENSIONS
from django.db.utils import InterfaceError
from django import db



class CSpider(scrapy.Spider):
    def __init__(self, name="boston", allowed_domains={}, start_urls={}, pagelimit=100):
        self.name = name
        self.allowed_domains = allowed_domains
        self.start_urls = start_urls
        self.count = pagelimit
    """
    name = "boston"
    allowed_domains = ["events.stanford.edu"]
    start_urls = [
        "http://events.stanford.edu/events/353/35309/",
    ]
    """
    rules = (Rule(SgmlLinkExtractor(deny_extensions=IGNORED_EXTENSIONS), follow=True),)
    # Pre compile to speed things up a bit
    prog1 = re.compile("([0-9][0-9][\/|\s][0-9][0-9][\/|\s][0-9][0-9])")
    prog2 = re.compile("[^(on)]\b[^(in)]\b(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s?([0-9]{2})([\s|,|.]{0,5})([0-9]{2,4})?", re.I)
    proglist = {prog1,prog2}




    def parse(self, response):
        logger = get_task_logger(__name__)
        sel = Selector(response)

        """
        *Magic*, try parse through all the text fields, looking for the following patterns
        1. dd/dd/dd (d=digit) (date)
        2. Jan.... Feb .... (date)
        3. January... (date)
        4. dd:dd:?dd (time)
        5. x to y, x - y (duration)
        If such pattern exists, insert into the database by using django items

        Also, ignore numbers with 3 or more continuous numbers unless number is 4 digit
        and starts with 19 or 20. Unfortunately I don't have enough time here as 1990 or 2014
        are valid addresses. One way to get rid of those is to use Google map geocoding API
        to check if the string is an address or not.
        """
        for text in sel.xpath('//*[text()]/text()[string-length()>4]').extract():
            found = False
            for prog in self.proglist:
                if(prog.search(text)!=None):
                    found = True
                    break
            if(found):
                item = SspiderItem()
                item['request'] = response.url
                parsedurl = urlparse.urlparse(response.url)
                item['url'] = parsedurl.path
                site, created = Site.objects.get_or_create(domain=parsedurl.netloc, defaults={'last_update': datetime.date.today()})
                item['site'] = site
                item['title'] = sel.xpath('/html/head/title/text()').extract()[0].encode('UTF-8', 'ignore').strip()[:199]
                print("Length")
                print(len(item['title']))
                try:
                    item.save()
                except InterfaceError:
                    db.connection.close()
                    item.save()

                self.count -= 1

                print(self.count)
                yield item
        if(self.count > 0):
            for url in sel.xpath('//a/@href').extract():
                if(url[-3:].lower() in IGNORED_EXTENSIONS) or Event.objects.filter(url=url).count():
                    pass
                else:
                    yield Request(urlparse.urljoin(response.url, url), callback=self.parse)
