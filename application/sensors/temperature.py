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