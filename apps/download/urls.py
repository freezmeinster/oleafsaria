from django.conf.urls import patterns, include, url

urlpatterns = patterns('download.views',
    url(r'^tentang$', 'tentang', name='tentang'),
    url(r'^tambah$', 'tambah', name='tambah'),
    url(r'^aksi/(?P<aksi>\w+)/(?P<id>\w+)/$', 'aksi', name='aksi'),
    url(r'^hapus/(?P<id>\w+)/$', 'hapus', name='hapus'),
    url(r'^login$', 'login_page', name='login'),
    url(r'^daftar$', 'daftar', name='daftar'),
    url(r'^logout$', 'logout_page', name='logout'),
)
