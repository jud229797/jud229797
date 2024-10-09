import datetime
import cloud
import paho.mqtt.client as mqtt
import json  # 确保导入了json模块
import time


# 假设有一组环境数据
windrint_data = 5
air_hum_data = 30
air_temp_data = 22
lux_data = 1000
soild_temp_data = 18
soild_hum_data = 45
ph_data = 5.8
EC_data = 1.2
N_data = 0.5
P_data = 0.3
K_data = 1.0
winddirection_data = 'N'


        
class EnvironmentalData :
    def __init__(self, region, windrint_data, air_hum_data, air_temp_data, lux_data,  soild_temp_data, soild_hum_data, ph_data, EC_data ,N_data, P_data, K_data,winddirection_data):
        self.region = region   #区域 ##1为左上角，2为右上角，3为左下角，4为右下角
        self.windrint_data = windrint_data #风速
        self.air_hum_data = air_hum_data    # 湿度
        self.air_temp_data = air_temp_data  # 温度
        self.lux_data = lux_data # 光照强度
        self.soild_temp_data = soild_temp_data  # 土壤温度
        self.soild_hum_data = soild_hum_data  # 土壤湿度
        self.ph_data = ph_data     # pH值
        self.N_data = N_data   # 氮含量（假设）
        self.P_data = P_data   # 磷含量（假设）
        self.K_data = K_data # 钾含量（假设）
        self.EC_data = EC_data # 电导率（假设）
        self.winddirection_data = winddirection_data #风向
    @staticmethod
    def uart(s):
        numbers = list(map(float, s.split(',')))
        if len(numbers) < 13:  # 检查是否有足够的数据
            raise ValueError("Received data does not contain enough values")
        return EnvironmentalData(*numbers)

    


data=[['11日（今天）', '晴朗', '16', '21'], ['12日（明天）', '晴朗', '16', '20'], ['13日（后天）', '雷阵雨转阵雨', '34', '28']]
#判断季节
def get_season():
    today = datetime.date.today()
    month = today.month

    if (month == 3 or month == 4 or month == 5):
        return "spring"
    elif (month == 6 or month == 7 or month == 8):
        return "summer"
    elif (month == 9 or month == 10 or month == 11):
        return "fall"
    else:
        return "winter"


# 定义函数来提取指定日期的天气信息
def extract_weather_info(date_str):
    for item in data:
        if date_str in item[0]:
            weather_info = item[1]
            # weather_low_temp = item[2]
            # weather_hight_temp = item[3]
            return weather_info
    return None

def  extract_weather_ltemp(date_str):
    for item in data:
        if date_str in item[0]:
            # weather_info = item[1]
            weather_low_temp = item[2]
            # weather_hight_temp = item[3]
            return int(weather_low_temp)
    return None


def  extract_weather_htemp(date_str):
    for item in data:
        if date_str in item[0]:
            # weather_info = item[1]
            # weather_low_temp = item[2]
            weather_hight_temp = item[3]
            return int(weather_hight_temp)
    return None


env_data_topleft = EnvironmentalData(1, 5, 30, 22, 1000, 18, 45, 6, 1.2, 0.5, 0.3, 1.0, 'N')
env_data_topright = EnvironmentalData(2, 5, 30, 22, 1000, 18, 45, 6, 1.2, 0.5, 0.3, 1.0, 'N')
env_data_bottomright = EnvironmentalData(3, 5, 30, 22, 1000, 18, 45, 6, 1.2, 0.5, 0.3, 1.0, 'N')
env_data_bottomleft = EnvironmentalData(4, 5, 30, 22, 1000, 18, 45, 6, 1.2, 0.5, 0.3, 1.0, 'N')

circle_data_topleft = "nothing"
circle_data_topright = "nothing"
circle_data_bottomright = "flower"
circle_data_bottomleft = "white_f"

suggestions = [[] for _ in range(4)]# 创建一个包含四个空列表的列表，用于存储每块土地的建议

#增加字符串函数
def add_suggestions(index, text):
    suggestions[index].append(text)

# 将字符串转化为最终1个字符串上云
# def final(suggestions):
#     final_suggestions = "\n".join(
#         f"土地{i+1}：\n- " + "\n- ".join(region_suggestions)
#         for i, region_suggestions in enumerate(suggestions)
#     )
#     return final_suggestions


def Decide():
    while True:
        # 假设 env_data 和 circle_data 是全局变量，并且会在函数外部更新
        global env_data_topleft, env_data_topright, env_data_bottomright, env_data_bottomleft
        env_data_list = [env_data_topleft, env_data_topright, env_data_bottomright, env_data_bottomleft]
        circle_data_list = [circle_data_topleft, circle_data_topright, circle_data_bottomright, circle_data_bottomleft]

        # 遍历每块土地的数据并生成建议
        for index, (env_data, cycle_data) in enumerate(zip(env_data_list, circle_data_list)):
            if cycle_data == "nothing":
                suggest_disease_prevention("green", index)
            elif cycle_data == "bud":
                suggest_disease_prevention("bud", index)
            elif cycle_data == "flower":
                suggest_disease_prevention("flower", index)
            elif cycle_data == "white_f":
                suggest_disease_prevention("white_f", index)
            else:
                suggest_disease_prevention("red_f", index)

        # 将建议转化为字符串并上云
        client = cloud.activate_devices()
        for i in range(4):
            final_suggestions = "\n".join(suggestions[i])
            attribute = f"land{i+1}"
            print(attribute)
            print(final_suggestions)
            cloud.trans_suggest(client, attribute, final_suggestions)
            suggestions[i].clear()
        # 确保在发送建议后清空建议列表
        time.sleep(10)  # 等待10秒

# 决策播种
def check_weather_and_soil_for_seeding(index, env_data):
    global env_data_topleft,env_data_topright,env_data_bottomright,env_data_bottomleft
    env_data_list = [env_data_topleft, env_data_topright, env_data_bottomright, env_data_bottomleft]

    if get_season()=="summer":
        # 天气判断
        if '晴' in extract_weather_info('今天'):
            if '晴' in extract_weather_info('明天'):
                if extract_weather_ltemp('今天')>=15 and extract_weather_htemp('今天')<=23 and extract_weather_ltemp('明天')>=15 and extract_weather_htemp('明天')<=23:
                    add_suggestions(index, "现在是秋天,天气晴朗,今天和明天适宜播种噢。\n")
                    #水分判断
                    if env_data_list[index].soild_hum_data<80:
                        add_suggestions(index, "土壤水分含量过少,需要浇水啦。\n")
                    else:
                        add_suggestions(index, "土壤水分含量适宜播种。\n")
                    #pH判断
                    if 5.5<=env_data_list[index].ph_data<=6.5:
                        add_suggestions(index, "土壤pH=%.1f适宜,不需要另外施加。\n"% env_data_list[index].ph_data)
                    elif env_data_list[index].ph_data<=5.5:
                        needph = 5.5-ph_data
                        add_suggestions(index, "土壤pH=%.1f,需要另外施加50kg左右的石灰或草木灰等碱性物质。\n" % env_data_list[index].ph_data)#一亩地大概
                    else:
                        needph = ph_data-6.5
                        add_suggestions(index, "土壤pH=%.1f,需要另外施加50kg左右的施用硫酸铵或氯化铵等酸性物质。\n" % env_data_list[index].ph_data)#一亩地大概
                        add_suggestions(index, "记得给土壤松土施肥。\n")
                elif extract_weather_htemp('今天')<=15:
                    add_suggestions(index, "现在是秋天，天气晴朗，但最近气温较低，不宜播种。\n")
                elif extract_weather_ltemp('今天')>=23 and extract_weather_htemp('明天')>=23:
                    add_suggestions(index, "现在是秋天，天气晴朗，但最近气温较高，不宜播种。\n")
                else:
                    add_suggestions(index, "现在是秋天，天气晴朗，但最近气温不宜播种。\n")
            else:
                add_suggestions(index, "明天会下雨，不宜播种。\n")
                
        elif '雨' in extract_weather_info('今天'):
            if '雨' in extract_weather_info('明天'):
                add_suggestions(index, "这两天都在下雨，不宜播种。\n")
        else:
            add_suggestions(index, "今天在下雨，不宜播种。\n")


def suggest_disease_prevention(growth_stage,index):
    # 根据生长阶段提供疾病预防建议

    if growth_stage=="green":
        add_suggestions(index, "育苗季，可能发生草莓炭疽病,注意预防。匍匐茎、叶柄、花茎发病症状都表现为近黑色的纺锤形或椭圆形病斑、稍凹陷，溃疡状，湿度高时病部可见肉红色黏质孢子堆。预防药剂：代森联、咪鲜胺、辛菌胺、代森锰锌、二氰蒽醌。\n")
        add_suggestions(index, "青枯病,草莓植株下位叶1～2片凋萎脱落，叶柄变为紫红色，植株发育不良。预防药剂：中生菌素、春雷霉素、络氨铜、噻唑锌、叶枯唑、氢氧化铜、壬菌铜。\n")
        add_suggestions(index, "细菌性叶斑病,片下表面出现水浸状红褐色不规则形病斑。预防药剂：中生菌素、春雷霉素、乙蒜素、络氨铜、噻唑锌、叶枯唑、氢氧化铜、壬菌铜、可杀得三千、康普森细菌立健。\n")
        add_suggestions(index, "黄萎病，叶片边缘水浸状，叶片、叶柄产生黑褐色长条形病斑，然后叶片萎蔫、缺素，无新叶生长。防治药剂：敌克松，恶霉灵或甲霜.恶霉灵，申嗪霉素，乙蒜素。\n")
        add_suggestions(index, "根腐病，有传染性！急性根腐病症状为雨后叶尖突然凋萎，不久呈青枯状，引起全株迅速枯死。防治药剂：甲霜.恶霉灵，霜脲.锰锌，烯酰.福美双，四霉素，康尔根。\n")
        add_suggestions(index, "芽枯病（立枯病），植株基部发病，在近地面部分初生无光泽褐斑，逐渐凹陷，并长出米黄色至淡褐色蜘蛛巢状菌丝体。防治药剂：多抗霉素，百菌清，异菌脲，肟菌酯。\n")
        add_suggestions(index, "幼苗成活后，两片叶已经展开时，这是第一次追肥的时间节点。每亩用施硝硫基复合肥20斤，50~100克磷酸二氢钾，复配喷雾600倍沃丰素+300倍奥菌优。\n")
        return suggestions[index]
    elif growth_stage=="bud":
        add_suggestions(index, "花蕾期，可能出现黄萎病，叶片边缘水浸状，叶片、叶柄产生黑褐色长条形病斑，然后叶片萎蔫、缺素，无新叶生长。防治药剂：敌克松，恶霉灵或甲霜.恶霉灵，申嗪霉素，乙蒜素。\n")
        add_suggestions(index, "芽枯病（立枯病），植株基部发病，在近地面部分初生无光泽褐斑，逐渐凹陷，并长出米黄色至淡褐色蜘蛛巢状菌丝体。防治药剂：多抗霉素，百菌清，异菌脲，肟菌酯。\n")
        add_suggestions(index, "花蕾时期，每亩可施加磷、钾肥7.5～10千克")
        add_suggestions(index, "在花开前一周放养蜜蜂，让蜜蜂适应棚室内环境。花开时，蜜蜂可以辅助授粉，提高坐果率。注意棚内温度应保持在最适温度15-25℃。\n")
        return suggestions[index]
    elif growth_stage=="flower":
        add_suggestions(index, "花期，此时期是病虫害的高发期，应多观察花朵形状、颜色、状态。可能出现花蕾、花染病，花瓣呈粉红色，花蕾不能开放。果实染病，幼果不能正常膨大，干枯，若后期受害，果面覆有一层白粉。防治药剂：醚菌酯，四氟醚唑，露娜森，绿妃，康普森白立健。\n")
        add_suggestions(index, "灰霉病，发病多从花期开始，病菌最初从将开败的花或较衰弱的部位侵染，使花呈浅褐色坏死腐烂，产生灰色霉层。防治药剂：异菌脲、腐霉利、嘧霉胺、嘧菌酯、咯菌腈、嘧菌环胺。\n")
        add_suggestions(index, "枯萎病，主要在开花至收获期发生，心叶变黄绿或黄色卷曲，3个小叶中有1-2片变狭或呈船型，叶片变黄，随后叶缘变褐色。防治：70%甲基硫菌灵可湿性粉剂400倍液淋土及浸苗5分钟再定植。\n")
        add_suggestions(index, "芽枯病（立枯病），植株基部发病，在近地面部分初生无光泽褐斑，逐渐凹陷，并长出米黄色至淡褐色蜘蛛巢状菌丝体。防治药剂：多抗霉素，百菌清，异菌脲，肟菌酯。\n")
        return suggestions[index]
    elif growth_stage=="white_f":
        add_suggestions(index, "白果期，可能出现果腐病，花、果期连续多日低温多雨时，病菌侵袭花、果穗而使田间花、果穗成批急剧变黑枯死，或浆果干腐。防治：在定植前对土壤进行消毒处理，可以使用氯化苦进行土壤薰蒸消毒。\n")
        add_suggestions(index, "灰霉病，发病多从花期开始，病菌最初从将开败的花或较衰弱的部位侵染，使花呈浅褐色坏死腐烂，产生灰色霉层。防治药剂：异菌脲、腐霉利、嘧霉胺、嘧菌酯、咯菌腈、嘧菌环胺。\n") 
        add_suggestions(index, "芽枯病（立枯病），植株基部发病，在近地面部分初生无光泽褐斑，逐渐凹陷，并长出米黄色至淡褐色蜘蛛巢状菌丝体。防治药剂：多抗霉素，百菌清，异菌脲，肟菌酯。\n")  
        add_suggestions(index, "坐果后，至草莓变色，所用肥料为：20-10-30+TE（低度膨果型）13-4-42+TE（高度膨果型）5-10kg/亩，6-7天一次，追施1-2次。\n")
        return suggestions[index]
    else:
        add_suggestions(index, "成熟期，可能出现灰霉病，发病多从花期开始，病菌最初从将开败的花或较衰弱的部位侵染，使花呈浅褐色坏死腐烂，产生灰色霉层。防治药剂：异菌脲、腐霉利、嘧霉胺、嘧菌酯、咯菌腈、嘧菌环胺。\n")
        add_suggestions(index, "白粉病，发病初期在叶片背面长出薄薄的白色菌丝层，叶片向上卷曲呈汤匙状，逐步扩大并叶片背面及果实上产生一层薄霜似的白色粉状物。防治药剂：四氟醚唑，翠贝干悬浮剂。\n")
        add_suggestions(index, "芽枯病（立枯病），植株基部发病，在近地面部分初生无光泽褐斑，逐渐凹陷，并长出米黄色至淡褐色蜘蛛巢状菌丝体。防治药剂：多抗霉素，百菌清，异菌脲，肟菌酯。\n")
         # 采摘提示
        if '晴' in extract_weather_info('今天') or '阴' in extract_weather_info('今天'):
            add_suggestions(index, "草莓已经成熟了，今天天气不错，可以跟游客宣传采摘了！\n")
            add_suggestions(index, "每次摘果后，植株体内养分缺乏，为了尽快恢复植株生长，更快促使发新叶扎新根，要适当增施氮、磷、钾专用肥，每亩施入量尿素10～15千克、磷肥15～20千克、钾肥7.5～10千克。\n")
        return suggestions[index]


# 确保在主函数或脚本的合适位置调用 Decide()
if __name__ == "__main__":
    Decide()