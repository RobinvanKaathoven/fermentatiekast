class Controller():
    def __init__(self, name, validationFunction, controlFunction):
        self.name = name
        self.validationFunction = validationFunction
        self.controlFunction = controlFunction
        self.state = False
    def evaluate(self, temperature, humidity, targetTemperature, targetHumidity, temperatureThreshold, humidityThreshold):
        self.controlFunction(self.validationFunction(temperature, humidity, targetTemperature, targetHumidity, temperatureThreshold, humidityThreshold))
    