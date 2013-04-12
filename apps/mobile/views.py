import re
import xmlrpclib
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.template import RequestContext
from download.forms import FormDownload
from django.contrib import messages
from django.http import HttpResponse

def index(request):
    files = []
    server = xmlrpclib.ServerProxy(settings.ARIA_RPC_URL)
    active = server.aria2.tellActive()
    for file in active :
        fl = server.aria2.getFiles(file.get("gid"))
        
        try:
            nama_file = fl[0].get("path").split(settings.ARIA_REPO_PATH)[1]
        except :
            nama_file = "Inisiasi unduhan....."
            
        files.append(
            {
                "namafile" : nama_file,
                "gid" : file.get("gid"),
                "totalunduh" : file.get("totalLength"),
                "berhasilunduh" : file.get("completedLength"),
                "kecepatanunduh" : file.get("downloadSpeed"),
            }
        )
    stop = server.aria2.tellStopped(0,10000)
    file_stop = []
    for data in stop :
        fl = server.aria2.getFiles(data.get("gid")) 
        if len(fl[0].get("path").split(settings.ARIA_REPO_PATH)) == 1 :
            nama_files = "Gagal Download"
            url_path =  "#"
        else :
            nama_files = fl[0].get("path").split(settings.ARIA_REPO_PATH)[1]
            url_path = settings.ARIA_REPO_URL + fl[0].get("path").split(settings.ARIA_REPO_PATH)[1]
        file_stop.append({
            "namafile" : nama_files ,
            "gid" : data.get("gid"),
            "totalunduh" : fl[0].get("length"),
            "url" : url_path
        })
    
    pause = server.aria2.tellWaiting(0,10000)
    file_pause = []
    for data in pause :
        fl = server.aria2.getFiles(data.get("gid")) 
        if len(fl[0].get("path").split(settings.ARIA_REPO_PATH)) == 1 :
            nama_files = "Gagal Download"
            url_path =  "#"
        else :
            nama_files = fl[0].get("path").split(settings.ARIA_REPO_PATH)[1]
            url_path = settings.ARIA_REPO_URL + fl[0].get("path").split(settings.ARIA_REPO_PATH)[1]
        file_pause.append({
            "namafile" : nama_files ,
            "gid" : data.get("gid"),
            "berhasilunduh" : data.get("completedLength"),
            "totalunduh" : fl[0].get("length"),
            "url" : url_path
        })
    
    return render_to_response("mobile/index.html",{
        "files" : files,
        "stops" : file_stop,
        "pauses" : file_pause
    })

def hapus(requets,id):
    server = xmlrpclib.ServerProxy(settings.ARIA_RPC_URL)
    server.aria2.removeDownloadResult(id)
    return HttpResponse("ok")

def tentang(request):
    server = xmlrpclib.ServerProxy(settings.ARIA_RPC_URL)
    return render_to_response("mobile/tentang.html",{
        'stats' : server.aria2.getGlobalStat()
    })

def tambah(request):
    form = FormDownload()
    if request.method == "POST":
        data = request.POST.copy()
        form = FormDownload(data)
        if form.is_valid :
            url = data.get("url")
            split = data.get("split")
            server = xmlrpclib.ServerProxy(settings.ARIA_RPC_URL)
            try:
                server.aria2.addUri([url],{'split': split})
            except:
                messages.add_message(request, messages.INFO, 'Url yang anda masukan tidak valid')
                return redirect("mobile_tambah")
            
            return redirect("mobile_index")
    return render_to_response("mobile/tambah.html",{
        },context_instance=RequestContext(request))
