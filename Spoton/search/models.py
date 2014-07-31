from django.db import models

# Create your models here.
class Site(models.Model):
    domain = models.CharField(max_length=100)
    last_update = models.DateTimeField()

class Event(models.Model):
    site = models.ForeignKey(Site, verbose_name="patent site")
    url = models.CharField(max_length=2000)
    request = models.CharField(max_length=2000)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField(default=None, blank=True, null=True)
    end_time = models.DateTimeField(default=None, blank=True, null=True)

class Job(models.Model):
    site = models.ForeignKey(Site, verbose_name="patent site")
    start_url = models.CharField(max_length=2000)
    pagelimit = models.IntegerField(default=30)
    queueid = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
