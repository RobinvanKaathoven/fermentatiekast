import time

try:
        adafruit_dht = __import__("adafruit_dht")
        board = __import__("board")
        print("AdaFruit DHT found")
except:
        random = __import__("random")
        print("No AdaFruit DHT found")

class Metric:
    def __init__(self, name, value, labels={}):
        self.name = name
        self.labels = labels
        self.value = value
        
    
    def to_prometheus(self):
        labels = ', '.join([f"{key}=\"{val}\"" for key, val in self.labels.items()])
        return f"{self.name}{{{labels}}} {self.value}"
  
class TemperatureSensor:
    def __init__(self, data_pin):
        try:
            self.dht_device = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        except NameError as error:
            self.temperature = 20
            self.humidity = 50
            self.dht_device = None
            
    def read(self, retries=5):
        if self.dht_device is not None:
            try:
                self.temperature = self.dht_device.temperature
                self.humidity = self.dht_device.humidity
            except RuntimeError as error:
                #Happens. Screw DHTs
                1+1
            return [
                Metric("pihome_temperature", self.temperature),
                Metric("pihome_humidity", self.humidity)
            ]
        else:
            return [
                Metric("pihome_temperature", self.temperature),
                Metric("pihome_humidity", self.humidity)
            ]
        
    def readJson(self):
        if self.dht_device is not None:
            self.temperature = self.dht_device.temperature
            self.humidity = self.dht_device.humidity
        return {
            "temperature": self.temperature,
            "humidity": self.humidity
        }
    
    def set(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity
        
            
