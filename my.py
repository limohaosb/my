import datetime
import random
from zhdate import ZhDate as lunar_date
from requests import get, post
import os
import sys
today = datetime.date.today()
 
# print(today.year, today.month, today.day)
# print("大年时间: ", lunar_date(today.year+1, 1, 1).to_datetime().date())
# print("端午时间: ", lunar_date(today.year, 5, 5).to_datetime().date())
# print("中秋时间: ", lunar_date(today.year, 8, 15).to_datetime().date())
# print("元旦时间: ", f"{today.year+1}-01-01")
# print("清明时间: ", f"{today.year+1}-04-05")
# print("劳动时间: ", f"{today.year+1}-05-01")
# print("国庆时间: ", f"{today.year+1}-10-01")
 
distance_big_year = (lunar_date(today.year + 1, 1, 1).to_datetime().date() - today).days
 
distance_5_5 = (lunar_date(today.year, 5, 5).to_datetime().date() - today).days
distance_5_5 = distance_5_5 if distance_5_5 > 0 else (
        lunar_date(today.year + 1, 5, 5).to_datetime().date() - today).days
 
distance_8_15 = (lunar_date(today.year, 8, 15).to_datetime().date() - today).days
distance_8_15 = distance_8_15 if distance_8_15 > 0 else (
        lunar_date(today.year + 1, 8, 15).to_datetime().date() - today).days
 
distance_year = (datetime.datetime.strptime(f"{today.year + 1}-01-01", "%Y-%m-%d").date() - today).days
 
distance_4_5 = (datetime.datetime.strptime(f"{today.year}-04-05", "%Y-%m-%d").date() - today).days
distance_4_5 = distance_4_5 if distance_4_5 > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-04-05", "%Y-%m-%d").date() - today).days
 
distance_5_1 = (datetime.datetime.strptime(f"{today.year}-05-01", "%Y-%m-%d").date() - today).days
distance_5_1 = distance_5_1 if distance_5_1 > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-05-01", "%Y-%m-%d").date() - today).days
 
distance_10_1 = (datetime.datetime.strptime(f"{today.year}-10-01", "%Y-%m-%d").date() - today).days
distance_10_1 = distance_10_1 if distance_10_1 > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-10-01", "%Y-%m-%d").date() - today).days
 
 
def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    print(week_day_dict[day])
    return week_day_dict[day]
 
 
# print("距离大年: ", distance_big_year)
# print("距离端午: ", distance_5_5)
# print("距离中秋: ", distance_8_15)
# print("距离元旦: ", distance_year)
# print("距离清明: ", distance_4_5)
# print("距离劳动: ", distance_5_1)
# print("距离国庆: ", distance_10_1)
# print("距离周末: ", 5 - today.weekday())
 
now_ = f"{today.year}年{today.month}月{today.day}日"
week_day_ = 5 - today.weekday()

def get_access_token():
    # appId 
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause") 
        sys.exit(1)
    # print(access_token)
    return access_token
def get_color():
    # 往list中填喜欢的颜色即可
    color_list = ['#6495ED','#3CB371']
 
    return random.choice(color_list)
def send_message(access_token,to_user,distance_big_year,distance_5_5,distance_8_15,distance_year,distance_4_5,distance_5_1,distance_10_1,week_day_):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "data": {
            "distance_big_year": {
                "value": distance_big_year,
                "color": get_color()
            },
            "distance_5_5": {
                "value": distance_5_5,
               "color": get_color()
            },
            "distance_8_15": {
                "value": distance_8_15,
                "color": get_color() 
            },
            "distance_year": {
                "value": distance_year,
                "color": get_color()
            },
            "distance_4_5": {
                "value": distance_4_5,
                "color": get_color()
            },
            "distance_5_1": {
                "value": distance_5_1,
                "color": get_color()
            },
            "distance_10_1": {
                "value": distance_10_1,
                "color": get_color()
            },
            "week_day_": {
                "value": week_day_,
               "color": get_color()
            }
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)
if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

accessToken = get_access_token()
users = config["user"]
for user in users:
    send_message(accessToken,user,distance_big_year,distance_5_5,distance_8_15,distance_year,distance_4_5,distance_5_1,distance_10_1,week_day_)
    os.system("pause")

   
 