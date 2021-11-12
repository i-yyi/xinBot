
import msg_analyzer.data.data_manager as data_manager
from msg_analyzer.data.talker import fixed_answers
import time
import json
import requests
from random import choice, randint
help_msg = '''你要和我说什么吖~
1.  命令以.开头
    .help/.menu : 查看帮助
    .add msg+reply : 学习对话啦
    .del msg+reply : 删除学习对话
    .cat : 猫猫图！我最喜欢猫猫啦~！
    .rp : 获取今日RP~
    .prprpr : 舔狗语录~, x1n也想拥有一个~！
    .comment : 有想要一点网易云评论嘛？

2.  对话不要以.开头, 如果我听得懂就会回答啦~
'''
ban_list = {}
rp_list = {}
times = {}
rp_list['date'] = 0 # 初始化, 否则rp处会读不到key
my_qq = int(json.load(open("./config.json", encoding="utf-8"))['admin_qq'])
class Detecter() :
    def __init__(self, msg, sender, func_list) :
        self.msg = msg
        self.sender = sender
        self.dataManager = data_manager.Data_Manager()
        self.custom_data = self.dataManager.getData() # return a dict
        self.func_list = func_list
        if self.msg[0] == '.' :
            self.msg = self.msg[1:]
    def help_menu(self) :
        if self.msg[:4] == "help" or self.msg[:4] == "menu":
            return [True, help_msg]
        return [False]
    def add_custom(self) :
        if time.localtime().tm_mday != rp_list['date'] :
            times.clear()
        if self.msg[:4] != "add " :
            return [False]
        msgtemp = self.msg[4:]
        if "/" in msgtemp or "|" in msgtemp :
            return [True,"不能含有/或|呀~"]
        if msgtemp.count('+') != 1 or msgtemp.split("+")[1] == "":
            return [False]
        msgtemp = msgtemp.split("+")
        if len(msgtemp[0]) < 4 and self.sender["user_id"] != my_qq:
            return [True, "长度要大于3鸭~"]
        if self.sender['user_id'] in times :
            times[self.sender['user_id']] += 1
            if times[self.sender['user_id']] > 4 and self.sender["user_id"] != my_qq :
                return [True, "一天只能教xin3句话啦~太多了记不下了呜~~"]
        else :
            if 'fix_custom' not in self.custom_data :
                self.custom_data['fix_custom'] = {}
            times[self.sender['user_id']] = 1
        if msgtemp[0] in self.custom_data['fix_custom'] :
            if msgtemp[1] in self.custom_data['fix_custom'][msgtemp[0]] :
                return [True, choice(fixed_answers['custom_learned'])]
            self.custom_data['fix_custom'][msgtemp[0]].append(msgtemp[1])
        else :
            self.custom_data['fix_custom'][msgtemp[0]] = [msgtemp[1]]
        self.dataManager.saveData(self.custom_data)
        return [True, choice(fixed_answers['custom_learn'])]

    def add_in_custom(self) : 
        if self.msg[:5] != "add1 " : 
            return [False]
        tempStr = str(self.sender['user_id'])
        tempStr1 = str(my_qq)
        if tempStr != tempStr1 :
            return [False]
        if 'fuzz_custom' not in self.custom_data :
            self.custom_data['fuzz_custom'] = {}
        msgtemp = self.msg[5:].split("+", 1)
        if msgtemp[0] in self.custom_data['fuzz_custom'] :
            if msgtemp[1] in self.custom_data['fuzz_custom'][msgtemp[0]] :
                return [True, choice(fixed_answers['custom_learned'])]
            self.custom_data['fuzz_custom'][msgtemp[0]].append(msgtemp[1])
        else :
            self.custom_data['fuzz_custom'][msgtemp[0]] = [msgtemp[1]]
        self.dataManager.saveData(self.custom_data)
        return [True, choice(fixed_answers['custom_learn'])]

    def del_custom(self) :
        if self.msg[:4] != "del " :
            return [False]
        msgtemp = self.msg[4:].split("+", 1)
        if len(msgtemp[0]) < 4 and self.sender["user_id"] != my_qq:
            return [True, "长度要大于3鸭~"]
        if msgtemp[0] in self.custom_data['fix_custom'] :
            for i in range(len(self.custom_data['fix_custom'][msgtemp[0]])) :
                if self.custom_data['fix_custom'][msgtemp[0]][i] == msgtemp[1] :
                    self.custom_data['fix_custom'][msgtemp[0]].pop(i)
                    if(len(self.custom_data['fix_custom'][msgtemp[0]]) == 0) :
                        del self.custom_data['fix_custom'][msgtemp[0]]
                    self.dataManager.saveData(self.custom_data)
                    return [True, choice(fixed_answers['custom_removed'])]
        return [True, choice(fixed_answers['custom_removerr'])]

    def get_setu(self) :
        if self.sender["user_id"] != my_qq :
            return [False]
        if self.msg in ["setu"] :
            try :
                req_url = "https://api.lolicon.app/setu/"
                params = {'size' : 'regular'}
                setu = requests.get(req_url, params=params).json()['data'][0]
                local_img_url = "Title : " + setu['title'] + "\n[CQ:image,file=" + setu['url'] + "]\n画师 : " + setu['author']
                return [True, local_img_url]
            except Exception as e:
                print(e)
                return [True, "呜呜, 找不到图片啦！"]
        return [False]

    def get_cat(self) :
        if self.msg in ["猫猫！", "来张猫猫图", "喵喵~", "猫猫图", "猫", "cat"] :
            try : 
                req_url = "https://api.thecatapi.com/v1/images/search"
                cat = requests.get(req_url).json()[0]['url']
                local_img_url = "[CQ:image,file=" + cat + "]"
                return [True, local_img_url]
            except Exception :
                return [True, "咦~? 怎么找不见猫猫了~"] 
        return [False]

    def get_furry(self) :
        if self.msg in ["furry!", "福瑞图", "来点furry", "furry"] :
            return [True, "Yirannn 太懒啦，没加furry图呢~"]
        return [False]
    
    def get_r18(self) :
        if self.msg in ["r18"] and self.sender['user_id'] == my_qq:
            try :
                req_url = "https://api.lolicon.app/setu/"
                params = {'r18' : '1'}
                setu = requests.get(req_url, params=params).json()['data'][0]
                local_img_url = "Title : " + setu['title'] + "\n[CQ:image,file=" + setu['url'] + "]\n画师 : " + setu['author']
                return [True, local_img_url]
            except Exception as e:
                print(e)
                return [True, "呜呜, 找不到图片啦！"]
        return [False]
    
    def rp_message(self, rp) :
        base_str = "你今天的RP是 ~ ：" + str(rp) + "\n"
        if rp == 100 :
            base_str += choice( ["哇~金色传说！"],
                                ["!!运气这么强的嘛"])
        elif rp > 90 :
            base_str += choice(["有没有试试买彩票呢？~"])
        elif rp > 80 :
            base_str += choice(["nya~ 好强！"])
        elif rp < 10 :
            base_str += choice(["有霉B, 但我不说是谁"])
        elif rp < 30 :
            base_str += choice( ["要小心了.."],
                                ["今天还要出门嘛? ..."])
        elif rp < 40 :
            base_str += choice(["呜~苦鲁西..."])
        elif rp < 50 :
            base_str += choice(["有点低了哦..."])        
        return base_str
    
    def detect_ban(self) :
        for i in fixed_answers['bad_words'] :
            if i in self.msg :
                return [True, choice(fixed_answers['anti-bad_words'])]
        return [False]

    def get_lickingdog(self) :
        if self.msg in ["舔狗", "prprpr"] :
            try :
                req_url = "https://api.oick.cn/dog/api.php"
                dog = requests.get(req_url).text[1:-1]
                return [True, dog]
            except Exception as e :
                print(e)
                return [True, "呜呜~，舔狗下线啦"]
        return [False]

    def get_rp(self) :
        if self.msg in ["rp"] :
            if time.localtime().tm_mday != rp_list['date'] :
                rp_list.clear()
                rp_list['date'] = time.localtime().tm_mday

            if self.sender['user_id'] not in rp_list.keys() :
                rp_list[self.sender['user_id']] = randint(0, 100)
            return [True, self.rp_message(rp_list[self.sender['user_id']])]
        return [False]

    def change_rp(self) :
        if self.sender['user_id'] != my_qq :
            return [False]
        try :
            msgtemp = self.msg.split("+")
            rp_list[int(msgtemp[0])] = int(msgtemp[1])
            return [True, "收到啦！"]
        except :
            return [False]

    def ban_qq(self) :
        if self.msg[:4] != "ban " or self.sender['user_id'] != my_qq :
            return [False]
        try :
            msgtemp = int(self.msg[4:])
            if msgtemp in ban_list :
                ban_list[msgtemp] ^= 1
            else :
                ban_list[msgtemp] = 1
            return [True, "操作成功~"]
        except :
            pass
        if self.sender["user_id"] in ban_list :
            if ban_list[self.sender["user_id"]]:
                return [True, "呜...Yirannn把你Ban掉了"]
        else :
            return [False]
    def get_comment(self) :
        print("DEBUG :: " + self.msg[:7])
        if self.msg[:7] != "comment" :
            return [False]
        try :
            req_url = "http://api.lo-li.icu/wyy/"
            comment = requests.get(req_url).text
            return [True, comment]
        except Exception as e :
            print(e)
            return [True, "呜呜~，不要抑啦~有Xin陪你啊"]
    def want_to_eat() :
        pass
    def not_want_eat() :
        pass
    def what_to_eat() :
        pass
    def custom(self) :
        print("DEBUG :: GETTING CUSTOM MESSAGE")
        print(self.custom_data['fuzz_custom'])
        temp = self.detect_ban()
        if temp[0] :
            return temp
        if self.msg in self.custom_data['fix_custom'] :
            return [True, choice(self.custom_data['fix_custom'][self.msg])]
        for key in self.custom_data['fuzz_custom'] :
            print("DEBUG :: FUZZING")
            print(key)
            if key in self.msg :
                return [True, choice(self.custom_data['fuzz_custom'][key])]
        return [False, choice(fixed_answers['no_answer'])]
        
    def command(self) :
        res = ""
        jud = lambda x, y : x[1] if x[0] else y
        for i in self.func_list :
            exec_func = "self." + i + "()"
            print("DEBUG :: GETTING COMMAND " + exec_func)
            temp = eval(exec_func)
            res = jud(temp, res)
            if res != "" :
                return res
        else :
            return self.help_menu()[1]
