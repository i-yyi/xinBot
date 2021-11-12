import msg_analyzer.word_detecter as word_detecter
from msg_analyzer.data.talker import fixed_answers
from random import choice
def talk_to_unknown(sender) :
    if sender['sex'] == 'female' :
        return choice(fixed_answers["unknown_girls"])
    return choice(fixed_answers["unknown_answer"])
# 增加功能在list里面写好函数名, 然后去detecter里加函数
func_list_friend = [
    "detect_ban",
    "add_custom",
    "add_in_custom",
    "del_custom",
    "get_furry",
    "get_setu",
    "get_cat",
    "get_r18",
    "get_rp",
    "get_lickingdog",
    "ban_qq",
    "change_rp",
    "get_comment"
]
func_list_group = [
    "detect_ban",
    "add_custom",
    "del_custom",
    "get_furry",
    "get_setu",
    "get_cat",
    "get_rp",
    "get_lickingdog",
    "ban_qq",
    "get_comment"
]
def talk_to_friend(msg, sender, type) : 
    # input : msg (String), sender (Dict)
    # result : msg (String)
    func_list = eval("func_list_"+type)
    detecter = word_detecter.Detecter(msg, sender, func_list)
    if msg[0] == '.' :
        tempMsg = detecter.command()
        if tempMsg != None :
            return tempMsg
    else :
        tempCustom = detecter.custom()
        if type == "group" and tempCustom[0] == False:
            return None
        else :
            return tempCustom[1]