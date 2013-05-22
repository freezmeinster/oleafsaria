from django.contrib.auth.models import User
from django.db import models

class Unduhan(models.Model):
    user = models.ForeignKey(User)
    url = models.URLField()
    mulai_unduh = models.DateTimeField(auto_now_add=True)
    unduh_id = models.CharField(max_length=255)
    ukuran = models.IntegerField(blank=True,null=True)
    selesai_unduh = models.DateTimeField(blank=True,null=True)
    nama_file = models.TextField(blank=True,null=True)
    lokasi_file = models.TextField(blank=True,null=True)
    
    def __unicode__(self):
        return self.url
    
