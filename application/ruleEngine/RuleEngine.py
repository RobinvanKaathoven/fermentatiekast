from .Rule import Rule
from .RelaisController import relaisController

class StatusChange:
    def __init__(self):
        self.OFF = -1
        self.ON = 1
        self.NONE = 0
statusChange = StatusChange()

ports = [21, 20, 16, 12, 26, 19, 13, 6]
relaisController.setPorts(ports)

class RuleEngine:
    def __init__(self):
        self.rules = []
        # self.addRule(Rule("hydrate", "humidity", "low", 5, 0))
        # self.addRule(Rule("dehydrate", "humidity", "high", 5, 1))
        # self.addRule(Rule("heat", "temperature", "low", 2, 2))
        # self.addRule(Rule("cool", "temperature", "high", 2, 3))

    temperatureThreshold = 3
    targetTemperature = 15
    humidityThreshold = 10
    targetHumidity = 50

    def testOn(self, number):
        relaisController.turnOn(number)
    def testOff(self, number):
        relaisController.turnOff(number)

    def setTargetTemperature(self, temperature):
        print(f"Setting target temperature to {temperature}")
        self.targetTemperature = temperature
    def setTemperatureThreshold(self, threshold):
        print(f"Setting temperature threshold to {threshold}")
        self.temperatureThreshold = threshold

    def setTargetHumidity(self, humidity):
        print(f"Setting target humidity to {humidity}")
        self.targetHumidity = humidity

    def setHumidityThreshold(self, threshold):
        print(f"Setting humidity threshold to {threshold}")
        self.humidityThreshold = threshold

    def getTargetTemperature(self):
        return self.targetTemperature
    def getTemperatureThreshold(self):
        return self.temperatureThreshold
    def getTargetHumidity(self):
        return self.targetHumidity
    def getHumidityThreshold(self):
        return self.humidityThreshold

    def addRule(self, rule):
        self.rules.append(rule)
    def removeRule(self, rule):
        self.rules.remove(rule)
    
    def validateRule(self, rule, temperature, humidity):
        if rule.type == "humidity" :
            if rule.variant == "Too Low":
                return hydrateValidation(temperature, humidity, self.targetTemperature, self.targetHumidity, rule.threshold)
            elif rule.variant == "Too High":
                return dehydrateValidation(temperature, humidity, self.targetTemperature, self.targetHumidity, rule.threshold)
        elif rule.type == "temperature":
            return heatingValidation(temperature, humidity, self.targetTemperature, self.targetHumidity, rule.threshold)
        elif rule.type == "cooling":
            return coolingValidation(temperature, humidity, self.targetTemperature, self.targetHumidity, rule.threshold)
        else:
            return statusChange.NONE

    def evaluateRules(self, temperature, humidity):
        print("Evaluating Rules")
        for rule in self.rules:
            relaisController.switch(rule.relay, self.validateRule(rule, temperature, humidity))    
            #relaisController.switch(rule.port, rule.validationFunction(temperature, humidity, self.targetTemperature, self.targetHumidity, self.temperatureThreshold, self.humidityThreshold))

def controlHydratingHeater(validation, port):
    relaisController.switch(port, validation)
    
def controlDehydrator(validation, port):
    relaisController.switch(port, validation)
    
def controlLampHeater(validation, port):
    relaisController.switch(port, validation)
    
def controlFridge(validation, port):
    relaisController.switch(port, validation)
    


def hydrateValidation(temperature, humidity, targetTemperature, targetHumidity, threshold):
    if humidity < targetHumidity - threshold:
        return statusChange.ON
    elif humidity > targetHumidity:
        return statusChange.OFF
    return statusChange.NONE

def dehydrateValidation(temperature, humidity, targetTemperature, targetHumidity, threshold):
    if humidity > targetHumidity + threshold:
        return statusChange.ON
    elif humidity < targetHumidity:
        return statusChange.OFF
    return statusChange.NONE

def heatingValidation(temperature, humidity, targetTemperature, targetHumidity, threshold):
    if temperature < targetTemperature - threshold:
        return statusChange.ON
    elif temperature > targetTemperature:
        return statusChange.OFF
    return statusChange.NONE

def coolingValidation(temperature, humidity, targetTemperature, targetHumidity, threshold):    
    if temperature > targetTemperature + threshold:
        return statusChange.ON
    elif temperature < targetTemperature:
        return statusChange.OFF
    return statusChange.NONE
    
ruleEngine = RuleEngine()

