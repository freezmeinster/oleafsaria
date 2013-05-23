from settings import ARIA_RPC_URL

def test_xmlrpc(request):
    if ARIA_RPC_URL != "" :
        return { 'xmlrpc' : True }
    else :
        return { 'xmlrpc' : False }
