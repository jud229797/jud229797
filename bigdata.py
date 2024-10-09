import decide__3

def send_bigdata():
    global env_data_topleft, env_data_topright, env_data_bottomright, env_data_bottomleft
    env_data_list = [env_data_topleft, env_data_topright, env_data_bottomright, env_data_bottomleft]
    global ill_data_topleft, ill_data_topright, ill_data_bottomright, ill_data_bottomleft
    ill_data_list = [ill_data_topleft, ill_data_topright, ill_data_bottomright, ill_data_bottomleft]
    tweather = decide__3.extract_weather_info("明天")

    send_data_storage = [[] for _ in range(4)]
    while True:
        for i, (env_data, sick_data) in enumerate(zip(env_data_list, ill_data_list)):
            # 检查病虫害数据是否存在
            sick_status = "无病虫害" if sick_data.ill_data =="nothing" else f"有{sick_data.ill_data}"
            send_info = f"土地{i+1} 温度：{env_data.air_temp_data}；湿度：{env_data.air_hum_data}；" \
                        f"土壤湿度：{env_data.soild_hum_data}；土壤pH：{env_data.ph_data}；" \
                        f"土壤N、P、K：{env_data.N_data}、{env_data.P_data}、{env_data.K_data}，" \
                        f"植株{sick_status}，明天天气：{tweather}"
            send_data_storage[i].append(send_info)
        combined_info = "\n".join("\n".join(info) for info in send_data_storage)
        for i in range(4):
            send_data_storage[i].clear()
        print(combined_info)
        return combined_info
        time.sleep(10)

    

send_bigdata()