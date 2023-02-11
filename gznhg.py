import random
import time
import datetime
import requests
from pypushdeer import PushDeer
import fake_useragent

GET_RATE_URL = "http://yunhq.sse.com.cn:32041/v1/shb1/snap/"  # 获取国债逆回购收益率的接口
EXPECTED_RATE = 2.9  # 预期年化收益率
START_WHETHER_SEND = 0  # 国债逆回购开始时是否发送过消息
END_WHETHER_SEND = 0  # 国债逆回购即将结束时是否发送过消息
PUSH_DEER_SERVER = ""
# PushDeer的自架API endpoint，默认是 https://api2.pushdeer.com/message/push
PUSH_KEY = ""
# PushDeer的Key，具体操作见https://github.com/easychen/pushdeer

CODE_LIST = ["204001", "204002", "204003", "204004",
             "204007", "204014", "204028", "204091", "204182"]  # 国债逆回购代码列表

CODE_WETHER_SEND_DICT = {"204001": False, "204002": False, "204003": False,
                         "204004": False, "204007": False, "204014": False,
                         "204028": False, "204091": False, "204182": False}  # 国债逆回购代码是否发送过消息，状态记录，以避免重复发送消息


def is_in_time(start_time_str, end_time_str):
    """
    判断当前时间是否处于输入的时间范围，仅支持当前日内时间
    :param start_time_str: '9:30'
    :param end_time_str: '15:26'
    :return: TRUE/FALSE
    """
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + start_time_str, '%Y-%m-%d%H:%M')
    # 开始时间
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + end_time_str, '%Y-%m-%d%H:%M')
    # 结束时间
    now_time = datetime.datetime.now()
    # 当前时间
    if start_time < now_time < end_time:
        print("是在%s - %s这个时间区间内" % (start_time_str, end_time_str))
        return True


def get_rate(code):
    """
    国债逆回购代码
    :param code: "204001"
    :return: 当前年化收益率
    """
    ua = fake_useragent.UserAgent()
    random_ua = ua.random
    rheader = {"User-Agent": random_ua}  # 配置随机User-Agent
    rate_resp = requests.get(url=GET_RATE_URL + code, headers=rheader)
    return rate_resp.json()["snap"][5]


def send_mgs(msg):
    """
    使用pushdeer把消息发送到设备
    :param msg: "要发送的字符串"
    :return:
    """
    pushdeer = PushDeer(server=PUSH_DEER_SERVER, pushkey=PUSH_KEY)
    pushdeer.send_text(msg)
    print(msg)


def judge(code):
    """
    根据年化收益率-预期收益率的比较和是否发送过消息共同判断是否发送消息到设备
    :param code: "204001"
    :return:
    """
    rate = get_rate(code)
    if rate < EXPECTED_RATE and CODE_WETHER_SEND_DICT[code] is True:
        CODE_WETHER_SEND_DICT[code] = False
    if rate > EXPECTED_RATE and CODE_WETHER_SEND_DICT[code] is False:
        send_mgs("!!大于%s&&&当前国债逆回购%s天期年化收益率为%s" % (EXPECTED_RATE, code[3:6], rate) + "%")
        CODE_WETHER_SEND_DICT[code] = True
    print(CODE_WETHER_SEND_DICT)


if __name__ == '__main__':
    while True:
        time.sleep(random.uniform(0.1, 0.2))
        if is_in_time("9:30", "15:26"):
            """如果时间处于国债逆回购交易时间，则轮询收益率"""
            a = random.uniform(1.1, 4.4)
            time.sleep(a)
            for i in CODE_LIST:
                time.sleep(random.uniform(0.1, 0.4))  # 随机延时模拟真实请求
                judge(i)
        if is_in_time("9:30", "10:48") and START_WHETHER_SEND == 0:
            """如果刚开始国债逆回购交易，查一下204001发送给设备"""
            send_mgs(get_rate("204001"))
            START_WHETHER_SEND = 1
            time.sleep(random.uniform(1.1, 1.3))
        if is_in_time("15:25", "15:26") and END_WHETHER_SEND == 0:
            """如果即将结束国债逆回购交易，查一下204001发送给设备"""
            send_mgs(get_rate("204001"))
            END_WHETHER_SEND = 1
            time.sleep(random.uniform(1.1, 1.3))
        if is_in_time("9:30", "10:48") is not True and is_in_time("15:25", "15:26") is not True:
            START_WHETHER_SEND = 0
            END_WHETHER_SEND = 0
            print("reseted!!")
