# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from models import Event

class DuplicatesPipeline(object):

    def process_item(self, item, spider):
        if Event.objects.filter(url=item['url']).count():
            raise DropItem("Duplicate item found: %s" % item)
        else:
            return item

