import Adafruit_DHT
from DTH11 import DTH11

d = DTH11(21 ,Adafruit_DHT.DHT11)
temp = d.getTemperature()
hum = d.getHumidity()
print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temp, hum))


