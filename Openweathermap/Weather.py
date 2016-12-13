import json, requests

key = '03e9627de83adeb223a4bbdd8bd15b94'

unites = 'imperial'
cityid = '4747845'
url = requests.get('http://api.openweathermap.org/data/2.5/weather?id='+cityid+'&units='+unites+'&APPID='+key)
weather = json.loads(url.text)

print "City: "+weather['name']
print "Temperature: "+str(weather['main']['temp'])+" F"
print "Conditions: "+weather['weather'][0]['description']
print "Wind: "+str(weather['wind']['speed'])+" mph"
