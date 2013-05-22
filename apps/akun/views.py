from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.admin.models import User

def akun_profile(request):
    return render_to_response("akun_list.html",{
        },RequestContext(request))

def akun_list(request):
    user = User.objects.all()
    return render_to_response("akun_list.html",{
        'user' : user
        },RequestContext(request))
