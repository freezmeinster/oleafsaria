from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.admin.models import User

def akun_profile(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST" :
        data = request.POST.copy()
        user.first_name = data.get("name")
        user.last_name = ""
        user.email = data.get("email")
        user.save()
    return render_to_response("akun_profile.html",{
        'user' : user
        },RequestContext(request))

def akun_bekukan(request,id):
    if id != 1 :
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
    return redirect("akun_list")

def akun_cairkan(request,id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect("akun_list")

def akun_hapus(request,id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("akun_list")

def akun_list(request):
    user = User.objects.all()
    return render_to_response("akun_list.html",{
        'user' : user
        },RequestContext(request))
