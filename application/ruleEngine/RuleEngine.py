from .Controller import Controller
from .RelaisController import RelaisController

class StatusChange:
    def __init__(self):
        self.OFF = -1
        self.ON = 1
        self.NONE = 0
statusChange = StatusChange()

ports = [21, 20, 16, 12, 26, 19, 13, 6]
relaisController = RelaisController(ports)

class RuleEngine:
    def __init__(self, temperatureSensor):
        self.temperatureSensor = temperatureSensor
        self.rules = []
        self.addRule(Controller("hydrate", hydrateValidation, controlHydratingHeater, 0))
        self.addRule(Controller("dehydrate", dehydrateValidation, controlDehydrator, 1))
        self.addRule(Controller("heating", heatingValidation, controlLampHeater, 2))
        self.addRule(Controller("cooling", coolingValidation, controlFridge, 3))


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
    
    def evaluateRules(self):
        print("Evaluating Rules")
        value = self.temperatureSensor.read()
        for rule in self.rules:
            rule.evaluate(value[0].value, value[1].value, self.targetTemperature, self.targetHumidity, self.temperatureThreshold, self.humidityThreshold)

def controlHydratingHeater(validation, port):
    relaisController.switch(port, validation)
    if(validation == statusChange.ON) :
        print("Turning on Waterheater")
    elif(validation == statusChange.OFF):
        print("Turning off Waterheater") 
        turnOff(port)
    else:
        print("No action needed for Waterheater")
def controlDehydrator(validation, port):
    relaisController.switch(port, validation)
    if(validation == statusChange.ON) :
        print("Turning on Dehydrator")
    elif(validation == statusChange.OFF):
        print("Turning off Dehydrator")
    else:
        print("No action needed for Dehydrator")
def controlLampHeater(validation, port):
    relaisController.switch(port, validation)
    if(validation == statusChange.ON) :
        print("Turning on Lamp heater")
    elif(validation == statusChange.OFF):
        print("Turning off Lamp heater")
    else:
        print("No action needed for Lamp heater")    
def controlFridge(validation, port):
    relaisController.switch(port, validation)
    if(validation == statusChange.ON):
        print("Turning on Fridge")
    elif(validation == statusChange.OFF):
        print("Turning off Fridge")
    else:
        print("No action needed for Fridge")

def hydrateValidation(temperature, humidity, targetTemperature, targetHumidity, temperatureThreshold, humidityThreshold):
    if humidity < targetHumidity - humidityThreshold:
        return statusChange.ON
    elif humidity > targetHumidity:
        return statusChange.OFF
    return statusChange.NONE

def dehydrateValidation(temperature, humidity, targetTemperature, targetHumidity, temperatureThreshold, humidityThreshold):
    if humidity > targetHumidity + humidityThreshold:
        return statusChange.ON
    elif humidity < targetHumidity:
        return statusChange.OFF
    return statusChange.NONE

def heatingValidation(temperature, humidity, targetTemperature, targetHumidity, temperatureThreshold, humidityThreshold):
    if temperature < targetTemperature - temperatureThreshold:
        return statusChange.ON
    elif temperature > targetTemperature:
        return statusChange.OFF
    return statusChange.NONE

def coolingValidation(temperature, humidity, targetTemperature, targetHumidity, temperatureThreshold, humidityThreshold):    
    if temperature > targetTemperature + temperatureThreshold:
        return statusChange.ON
    elif temperature < targetTemperature:
        return statusChange.OFF
    return statusChange.NONE
    


