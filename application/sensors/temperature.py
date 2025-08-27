import time
from util.metric import Metric

try:
        adafruit_dht = __import__("adafruit_dht")
        board = __import__("board")
        print("AdaFruit DHT found")
except:
        random = __import__("random")
        print("No AdaFruit DHT found")

class TemperatureSensor:
    def __init__(self, data_pin):
        try:
            self.dht_device = adafruit_dht.DHT22(board.D4, use_pulseio=False)
            self.temperature = 0
            self.humidity = 0
        except NameError as error:
            self.temperature = 20
            self.humidity = 50
            self.dht_device = None
    def update(self):
        if self.dht_device is not None:
            try:              
                _temperature, _humidity = self.dht_device.read_retry()
                if _temperature != 0 or _humidity != 0:
                    self.temperature = _temperature
                    self.humidity = _humidity

            except RuntimeError as error:
                #Happens. Screw DHTs
                1+1
            return {
                "temperature": self.temperature,
                "humidity": self.humidity
            }
        else:
            self.temperature = random.uniform(15.0, 25.0)
            self.humidity = random.uniform(30.0, 70.0)
            return {
                "temperature": self.temperature,
                "humidity": self.humidity
            }   
             
    def read(self):
        return {
            "temperature": self.temperature,
            "humidity": self.humidity
        }  
          
    def readJson(self):
        return {
            "temperature": self.temperature,
            "humidity": self.humidity
        }
    
    def set(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity
        
            
