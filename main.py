
import json
import time

import sender
while True :
    time.sleep(1)
    try :
        import receiver
        break
    except OSError :
        print("Connect Failed")
        continue
    except KeyboardInterrupt :
        break
import threading
import distributer

sem = threading.Semaphore(5)
config = json.load(open("./config.json", encoding="utf-8"))
#data : raw_msg, msg
#meta : sender/target, type
class disThread(threading.Thread):
    def __init__(self, req) :
        threading.Thread.__init__(self)
        self.msgrequest = req
    def run(self) :
        with sem :
            manager = distributer.Distributer(self.msgrequest)
            try :
                replydata, replymeta = manager.Distribute()
            except :
                return None
            # DEBUG
            print("replydata : ", end = "")
            print(replydata)
            # print("replymeta : ", end = "")
            # print(replymeta)
            # DEBUG
            
            talker = sender.Talker((config["IP"], config["send_port"]))
            talker.Distribute(replydata, replymeta)

print("Starting...")
while(True) :
    time.sleep(0.1)
    print("Heartbeat")
    req = ""
    try :
        req = receiver.Receive() # request (dict)
        if req == None :
            print("NONE")
            continue
    except KeyboardInterrupt :
        print("\nQuitting...")
        break
    except Exception :
        print(Exception)
        continue
    thisThread = disThread(req)
    thisThread.start()

