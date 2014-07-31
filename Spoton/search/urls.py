try:
    from django.conf.urls import (patterns, include, url,
                                  handler500, handler404)
except ImportError:
    from django.conf.urls.defaults import (patterns, include, url, # noqa
                                  handler500, handler404)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from views import SiteListView, JobListView, EventListView, JobFormView

urlpatterns = patterns(
    '',
    url(r'^$', SiteListView.as_view(),name='sitelist'),
    url(r'^jobs/$', JobListView.as_view(),name='joblist'),
    url(r'^jobs/new$', JobFormView.as_view(),name='jobform'),
    url(r'^events/$', EventListView.as_view(),name='eventlist'),
    url(r'^events/(?P<domainname>.*)/$', EventListView.as_view(),name='eventsearch'),

)