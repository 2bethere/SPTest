import datetime
from urlparse import urlparse
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from models import Site, Event, Job
from forms import JobForm
from django.db.models import Count
from celery.result import AsyncResult
import tasks

# Create your views here.
class SiteListView(ListView):
    queryset = Event.objects.values('site__domain','site__last_update').annotate(hits=Count('url', distinct=True))
    template_name = 'search/site_list.html'
    def get_context_data(self, **kwargs):
        context = super(SiteListView, self).get_context_data(**kwargs)
        return context

class JobListView(ListView):
    model = Job
    template_name = 'search/job_lits.html'
    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        for o in context['object_list']:
            o.state = AsyncResult(o.queueid).state
        return context

class JobFormView(CreateView):
    model = Job
    form_class = JobForm
    template_name = 'search/job_form.html'
    success_url = reverse_lazy('joblist')
    def get_context_data(self, **kwargs):
        context = super(JobFormView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        parsedurl = urlparse(form.instance.start_url)
        site, created = Site.objects.get_or_create(domain=parsedurl.netloc, defaults={'last_update': datetime.date.today()})
        form.instance.site = site
        #Create Celery event to crawl
        task_obj = tasks.run_spider.delay(name=parsedurl.netloc, allowed_domains=[parsedurl.netloc,], start_urls=[form.instance.start_url],pagelimit=form.instance.pagelimit)
        #run_spider(name="boston", allowed_domains={}, start_urls={}):
        form.instance.queueid = str(task_obj.id)
        form.instance.state = str(task_obj.state)
        return super(JobFormView, self).form_valid(form)

class EventListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        if 'domainname' in self.kwargs:
            return Event.objects.filter(site__domain=self.kwargs['domainname']).values('request').distinct().all()
        else:
            return Event.objects.values('request').distinct().all()

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        return context