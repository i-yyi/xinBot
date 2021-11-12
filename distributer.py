import json
import msg_analyzer.replyer as replyer
bot_qq = json.load(open("./config.json", encoding="utf-8"))['bot_qq']
'''
request 结构：
{
    post_type : 事件类型
    message_type : 消息类型
    sender : 发送人 {
        sex
        user_id
    }
    sub_type : 次类型
    message/raw_message : 消息
    group_id : 群号
}


reqmeta 结构 ：
{
    type : 事件类型
}
reqdata 结构 :
{
    type : 暂时指消息类型 Private/Group
    msgmeta : 消息元数据 {
        msgtype 消息类型
        msgsender 消息发送者 (Sender)
        subtype
    }
    msgdata : 消息数据 {
        msg/raw_msg
    }
}
'''
class Distributer() :
    reqdata, reqmeta = {}, {}
    def __init__(self, requset) :
        if requset['post_type'] == "message" :
            self.reqmeta['type'] = "message"
            self.reqdata['type'] = requset["message_type"]

            if self.reqdata['type'] == "private" :
                self.reqdata['msgmeta'] = {
                    "msgtype" : "private", 
                    "msgsender" : requset['sender'], 
                    "subtype" : requset['sub_type']
                }
                self.reqdata['msgdata'] = {
                    "raw_msg" : requset['raw_message'], 
                    "msg" : requset['message']
                }
            elif self.reqdata['type'] == "group" :
                self.reqdata['msgmeta'] = {
                    "msgtype" : "group",
                    "msgsender" : requset['sender'],
                    "group_id" : requset['group_id']
                }
                self.reqdata['msgdata'] = {
                    "raw_msg" : requset['raw_message'], 
                    "msg" : requset['message']
                }


        elif requset["post_type"] == "notice" :
            self.reqmeta['type'] = "notice"
            self.reqdata['type'] = requset["notice_type"]


        elif requset['post_type'] == "request" :
            self.reqmeta['type'] = "request"
            self.reqdata['type'] = requset['request_type']

        else :
            raise Exception
    
    def Distribute(self) :
        replydata, replymeta = {}, {}
        logstr = ''' DEBUG DATA ::::
        User : {}
        Message : {}
        Type : {}
        '''
        print("DEBUG :: Distributing")
        # try :
        #     print(logstr.format(reqdata['msgmeta']['msgsender'], reqdata['msgdata']['msg'], reqdata['msgmeta']['msgtype']))
        # except Exception(e) :
        #     print(e)
        if self.reqdata['msgmeta']['msgtype'] == "private" :
            if self.reqdata['msgmeta']['subtype'] != "friend" :
                replydata['msg'] = replyer.talk_to_unknown(self.reqdata['msgmeta']['msgsender'])
            else :
                replydata['msg'] = replyer.talk_to_friend(
                    self.reqdata['msgdata']['msg'], 
                    self.reqdata['msgmeta']['msgsender'],
                    "friend"
                )
            replymeta['type'] = self.reqdata['type']
            replymeta['sender'] = self.reqdata['msgmeta']['msgsender']


        elif self.reqdata['msgmeta']['msgtype'] == 'group' :
            if "[CQ:at,qq={}]".format(bot_qq) in self.reqdata['msgdata']['raw_msg'] :
                try : 
                    self.reqdata['msgdata']['msg'] = self.reqdata['msgdata']['msg'].split(" ", 1)[1]
                    replydata['msg'] = replyer.talk_to_friend(
                        self.reqdata['msgdata']['msg'], 
                        self.reqdata['msgmeta']['msgsender'],
                        "friend"
                    )
                except :
                    replydata['msg'] = "要和我说话嘛？先@我然后就可以说了哦~"
            else :
                replydata['msg'] = replyer.talk_to_friend(
                    self.reqdata['msgdata']['msg'], 
                    self.reqdata['msgmeta']['msgsender'],
                    "group"
                )
            replymeta['type'] = self.reqdata['type']
            replymeta['group_id'] = self.reqdata['msgmeta']['group_id']

        if replydata['msg'] != None :
            return replydata, replymeta
        else :
            return None