
from django.conf.urls import patterns, include, url

urlpatterns = patterns('akun.views',
    url(r'^list$', 'akun_list', name='akun_list'),
    url(r'^profile$', 'akun_profile', name='akun_profile'),
    url(r'^ganti-password$', 'akun_profile', name='akun_ganti_password'),
    url(r'^bekukan/(?P<id>\d+)/$', 'akun_bekukan', name='akun_bekukan'),
    url(r'^cairkan/(?P<id>\d+)/$', 'akun_cairkan', name='akun_cairkan'),
    url(r'^hapus/(?P<id>\d+)/$', 'akun_hapus', name='akun_hapus'),
)