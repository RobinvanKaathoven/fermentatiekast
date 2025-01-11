from helpers.metric import Metric
    
class TemperatureSensor:
    def __init__(self, data_pin):
        self.temperature = 0
        self.humidity = 0
        #self.sensor = Adafruit_DHT.DHT22

    def read(self, retries=5):
        self.temperature += 0.01
        self.humidity += 0.01
        return [
            Metric("pihome_temperature", self.temperature),
            Metric("pihome_humidity", self.humidity)
        ]