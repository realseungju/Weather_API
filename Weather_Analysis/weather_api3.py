import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_hours():
  current_date = datetime.now()
  cal_hour = current_date
  cal_hour = cal_hour.hour

  if cal_hour < 5 and cal_hour > 2:
     cal_hour = 2
  elif cal_hour < 8 and cal_hour > 5:
     cal_hour = 5
  elif cal_hour < 11 and cal_hour > 8:
     cal_hour = 8
  elif cal_hour < 14 and cal_hour > 11:
     cal_hour = 11
  elif cal_hour < 17 and cal_hour > 14:
     cal_hour = 14
  elif cal_hour < 20 and cal_hour > 17:
     cal_hour = 17
  elif cal_hour < 23 and cal_hour > 20:
     cal_hour = 20
  elif cal_hour < 2 and cal_hour > 23:
     cal_hour = 23

  if cal_hour < 10:
    cal_hour = '0' + str(cal_hour)
  cal_hour = str(cal_hour) + '00'

  return cal_hour

def cal_sky(sky):
  sky = int(sky)
  if sky == 1:
     sky = '맑음'
  elif sky == 3:
     sky = '구름 많음'
  elif sky == 4:
     sky = '흐림'
  return sky

def cal_wsd(wsd):
  if wsd > 0 and wsd <= 0.3:
    char = '고요바람'
  elif wsd > 0.3 and wsd <= 1.5:
     char = '실바람'
  elif wsd > 1.5 and wsd <= 3.3:
     char = '남실바람'
  elif wsd > 3.3 and wsd <= 5.4:
     char = '산들바람'
  elif wsd > 5.4 and wsd <= 7.9:
     char = '건들바람'
  elif wsd > 7.9 and wsd <= 10.7:
     char = '흔들바람'
  elif wsd > 10.7 and wsd <= 13.8:
     char = '된바람'
  elif wsd > 13.8 and wsd <= 17.1:
     char = '센바람'
  elif wsd > 17.1:
     char = '바람이 매우 강합니다.'
  return char

def get_weather(time):
   for i in range(len(weather_data['time'])):
      if weather_data['time'][i] == str(time):
         char_str = (weather_data['time'][i] + " 시, ")
         char_str += ("온도: " + str(weather_data['tmp'][weather_data['time'][i]]) + ", ")
         char_str += ("강수 확률: " + str(weather_data['pop'][weather_data['time'][i]]) + "%, ")
         char_str += ("풍속: " + cal_wsd(weather_data['wsd'][weather_data['time'][i]]) + "  " + str(weather_data['wsd'][weather_data['time'][i]]) + "m/s, ")
         char_str += ("강수량: " + str(weather_data['pcp'][weather_data['time'][i]]) + ", ")
         char_str += ("기상: " + cal_sky(weather_data['sky'][weather_data['time'][i]]) + ", ")
         char_str += ("습도: " + str(weather_data['reh'][weather_data['time'][i]]) + "% ")
         return char_str
   return ("이전 시간 혹은 잘못된 시간을 입력하셨습니다. 가까운 API 배포 시간 " + weather_data['time'][0] + "시 부터 입력 가능합니다.")

def current_time():
   str = "현재 불러온 시간은 " + weather_data['time'][0] + "시 부터 " + weather_data['time'][-1] + "시 까지 입니다."
   return str

def weather_analysis():
   max_tmp = max(weather_data['tmp'].values())
   min_tmp = min(weather_data['tmp'].values())
   max_wsd = max(weather_data['wsd'].values())
   max_pop = max(weather_data['pop'].values())

   if max_tmp - min_tmp > 10:
      str = "일교차는 10도 이상으로 외투를 챙기는 것이 좋아보이며, "
   else:
      str = "일교차는 10도 이하, "
   
   if max_wsd > 5:
      str += "바람이 조금 불며 "
   if max_wsd > 10:
      str += "바람이 많이 불며 "
   if max_wsd > 15:
      str += "바람이 매우 많이 불며 "
   else:
      str += "바람은 선선하며 "

   if max_pop > 60:
      str += "강수 확률이 60프로 이상으로 우산을 챙기는 것이 좋습니다."
   else:
      str += "강수 확률은 적습니다."
   
   return str
   

cal_hour = get_hours()
# API가 배포되는 시간을 계산

current_date = datetime.now().strftime("%Y%m%d")

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
key = 'Your_API_Key'
params ={'serviceKey' : key , 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'JSON', 'base_date' : current_date, 'base_time' : cal_hour, 'nx' : '60', 'ny' : '127' }

response = requests.get(url, params=params)

res_json = json.loads(response.content)

items = res_json['response']['body']['items']['item']

weather_data = {'time': [], 'tmp': {}, 'pop': {}, 'wsd': {}, 'pcp': {}, 'sky': {}, 'reh': {}}
# 시간, 온도, 강수확률, 풍속, 강수량, 기상, 습도 

for i in items:
    if i['fcstDate'] == current_date and i['category'] == 'TMP':
        weather_data['tmp'][str(i['fcstTime'][:2])] = int(i['fcstValue'])
        weather_data['time'].append(str(i['fcstTime'][:2]))
    if i['fcstDate'] == current_date and i['category'] == 'POP':
        weather_data['pop'][str(i['fcstTime'][:2])] = int(i['fcstValue'])
    if i['fcstDate'] == current_date and i['category'] == 'WSD':
        weather_data['wsd'][str(i['fcstTime'][:2])] = float(i['fcstValue'])
    if i['fcstDate'] == current_date and i['category'] == 'PCP':
        weather_data['pcp'][str(i['fcstTime'][:2])] = str(i['fcstValue'])
    if i['fcstDate'] == current_date and i['category'] == 'SKY':
        weather_data['sky'][str(i['fcstTime'][:2])] = str(i['fcstValue'])
    if i['fcstDate'] == current_date and i['category'] == 'REH':
        weather_data['reh'][str(i['fcstTime'][:2])] = int(i['fcstValue'])
