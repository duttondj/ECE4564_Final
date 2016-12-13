import json, requests

key = '03e9627de83adeb223a4bbdd8bd15b94'

unites = 'imperial'
cityid = '4747845'
url = requests.get('http://api.openweathermap.org/data/2.5/weather?id='+cityid+'&units='+unites+'&APPID='+key)
weather = json.loads(url.text)

print weather['main']['temp'],"F"
print weather['weather'][0]['description']