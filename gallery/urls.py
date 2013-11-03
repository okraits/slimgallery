from django.conf.urls import patterns, url

from gallery import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<folder_id>[0-9]+)/$', views.index, name='index'),
    url(r'^(?P<folder_id>[0-9]+)/(?P<image>[a-zA-Z0-9-]+)$', views.browse, name='browse'),
)
