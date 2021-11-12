
import requests

class Talker() :
    base_url = ""
    def __init__(self, target) :
        self.base_url = "http://" + str(target[0]) + ":" + str(target[1]) + "/"
    
    def Distribute(self, data, meta) :
        if meta['type'] == "private" :
            user_id = meta['sender']['user_id']
            message = data['msg']
            body = {
                'user_id' : user_id,
                'message' : message
            }
            url = self.base_url+"send_private_msg"
            res = requests.post(url = url, data = body)

        if meta['type'] == "group" :
            group_id = meta['group_id']
            message = data['msg']
            body = {
                'group_id' : group_id,
                'message' : message
            }
            url = self.base_url+"send_group_msg"
            res = requests.post(url = url, data = body)
        else :
            return False
        
        if res.json()['status'] == 'ok' :
            return True
        return False
