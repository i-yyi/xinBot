
# 暂时使用一个文件IO级别的自定义协议，可以扩展成 SQL
import json
file = "./msg_analyzer/data/custom_data.json"
class Data_Manager() :
    def __init__(self) :
        self.data = json.load(open(file))
    def getData(self) :
        return self.data
    def saveData(self, data) :
        fp = open(file, "w")
        json.dump(data, fp)
        fp.close()