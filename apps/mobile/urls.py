from django.conf.urls import patterns, include, url

urlpatterns = patterns('mobile.views',
    url(r'^$', 'index', name='mobile_index'),
    url(r'^tentang$', 'tentang', name='mobile_tentang'),
    url(r'^tambah$', 'tambah', name='mobile_tambah'),
    url(r'^hapus/(?P<id>\w+)/$', 'hapus', name='mobile_hapus'),
)
