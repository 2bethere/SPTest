# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from search.models import Event
from scrapy.contrib.djangoitem import DjangoItem


class SspiderItem(DjangoItem):
    django_model = Event
