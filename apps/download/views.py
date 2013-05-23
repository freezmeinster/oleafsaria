import re
import xmlrpclib
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.conf import settings
from download.models import Unduhan
from django.template import RequestContext
from download.forms import FormDownload
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    unduhan  = Unduhan.objects.filter(user=request.user)
    list_id = []
    for data in unduhan:
        list_id.append(data.unduh_id)
    
    if settings.ARIA_RPC_URL :
        reg_b = re.compile(r"android|avantgo|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino", re.I|re.M)
        reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|e\\-|e\\/|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\\-|2|g)|yas\\-|your|zeto|zte\\-", re.I|re.M)
        if request.META.has_key('HTTP_USER_AGENT'):
                user_agent = request.META['HTTP_USER_AGENT']
                b = reg_b.search(user_agent)
                v = reg_v.search(user_agent[0:4])
                if b or v:
                    return redirect("mobile_index")
        files = []
        server = xmlrpclib.ServerProxy(settings.ARIA_RPC_URL)
        active = server.aria2.tellActive()
        for file in active :
            fl = server.aria2.getFiles(file.get("gid"))
            
            try:
                nama_file = fl[0].get("path").split(settings.ARIA_REPO_PATH)[1]
            except :
                nama_file = "Inisiasi unduhan....."
            if file.get("gid") in list_id :    
                files.append(
                    {
                        "namafile" : nama_file,
                        "gid" : file.get("gid"),
                        "totalunduh" : file.get("totalLength"),
                        "process" : float(file.get("completedLength")) / float(file.get("totalLength")) * 100,
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
            if data.get("gid") in list_id :
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
            if data.get("gid") in list_id :
                file_pause.append({
                    "namafile" : nama_files ,
                    "gid" : data.get("gid"),
                    "berhasilunduh" : data.get("completedLength"),
                    "totalunduh" : fl[0].get("length"),
                    "url" : url_path
                })
                
        return render_to_response("index.html",{
            "files" : files,
            "stops" : file_stop,
            "pauses" : file_pause
        },context_instance=RequestContext(request))
    else :
         return render_to_response("index.html",{
        },context_instance=RequestContext(request))

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
                id = server.aria2.addUri([url],{'split': split})
                u = Unduhan(
                    user = request.user,
                    url = url,
                    unduh_id = id
                )
                u.save()
            except:
                messages.add_message(request, messages.INFO, 'Url yang anda masukan tidak valid')
                return redirect("tambah")
            
            return redirect(settings.ARIA_URL_PATH)
    return render_to_response("tambah.html",{
        "form" : form
        },context_instance=RequestContext(request))

def tentang(request):
    server = xmlrpclib.ServerProxy(settings.ARIA_RPC_URL)
    return render_to_response("tentang.html",{
        'stats' : server.aria2.getGlobalStat()
    })

def aksi(request,aksi,id):
    server = xmlrpclib.ServerProxy(settings.ARIA_RPC_URL)
    if aksi == "henti" :
        server.aria2.pause(id)
    elif aksi == "mulai" :
        server.aria2.unpause(id)
    elif aksi == "batal" :
        server.aria2.remove(id)
    else :
        return redirect(settings.ARIA_URL_PATH)
    return redirect(settings.ARIA_URL_PATH)


def hapus(requets,id):
    server = xmlrpclib.ServerProxy(settings.ARIA_RPC_URL)
    server.aria2.removeDownloadResult(id)
    return redirect(settings.ARIA_URL_PATH)

def daftar(request):
    if request.method =="POST" :
        data = request.POST.copy()
        try:
            user = User.objects.create_user(
                username = data.get('username'),
                email = data.get("email")
            )
            user.save()
            user.set_password(data.get('password'))
            user.first_name = data.get('name')
            user.save()
            messages.success(request,"Pengguna %s berhasil didaftarkan" % data.get('name'))
        except ValueError :
            messages.error(request,"Lengkapi form yang ada !")
        except :
            messages.warning(request,"Pengguna %s sudah pernah mendaftar" % data.get('name'))
            
    return  render_to_response('register.html',{
    },context_instance=RequestContext(request))


def login_page(request):
    if request.method == 'POST':
        data = request.POST.copy()
        username = data.get("username")
        password = data.get("password")
        print data
        user = authenticate(username=username,password=password)
        print user
        if user != None :
            if user.is_active :
                login(request,user)
                return redirect("/")
            else :
                messages.error(request, "Nama pengguna tidak aktif")
    
        else :
            messages.error(request, "Nama pengguna yang anda masukan tidak terdaftar atau password anda salah")
        
    return render_to_response("login.html",{
        },context_instance=RequestContext(request))

def logout_page(request):
    logout(request)
    return redirect("/")
