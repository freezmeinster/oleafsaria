import xmlrpclib

server = xmlrpclib.ServerProxy("http://bram:pass4bram@103.23.244.131:6800/rpc")
stop = server.aria2.tellStopped(0,1000)
wait = server.aria2.tellWaiting(0,1000)
active = server.aria2.tellActive()
