import json
import socket
import atexit
Response = '''HTTP/1.1 200 OK
Content-Type:text/html

'<p>Success</p>'
'''
ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind(("localhost", 5701))
ListenSocket.listen(100)
def LoadJson(msg) :
    front, end = 0, len(msg)
    # Find the body from HTTP request
    for i in range(len(msg)) :
        if msg[i] == '{' :
            front = i
            break
    for i in range(len(msg), front, -1) :
        if msg[i-1] == '}' :
            end = i
            break
    # print(msg[front:end])
    if end-front > 0 :
        return json.loads(msg[front:end])
    return None
def Receive() :
    Client, Address = ListenSocket.accept()
    Request = Client.recv(1024).decode(encoding="utf-8")
    Json = LoadJson(Request)
    Client.sendall(Response.encode(encoding="utf-8"))
    Client.close()
    return Json