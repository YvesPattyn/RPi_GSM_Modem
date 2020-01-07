import Adafruit_DHT
from time import sleep

class DTH11:
  def __init__(self, pin, sensor):
    self.pin = pin
    self.sensor = sensor
    self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
    
  def getTemperature(self):
    self.refresh()
    return self.temperature

  def getHumidity(self):
    self.refresh()
    return self.humidity

  def refresh(self):
    self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
    while self.humidity is None or self.temperature is None:
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
