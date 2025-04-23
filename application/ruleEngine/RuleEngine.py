from .Rule import Rule
from .RelaisController import relaisController
import time

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
        for i, o in enumerate(self.rules):
            if o.name == rule.name:
                del self.rules[i]
                break
    
    def validateRule(self, rule, temperature, humidity):
        if rule.type == "humidity" :
            if rule.variant == "low":
                return hydrateValidation(temperature, humidity, self.targetTemperature, self.targetHumidity, rule.threshold)
            elif rule.variant == "high":
                return dehydrateValidation(temperature, humidity, self.targetTemperature, self.targetHumidity, rule.threshold)
        elif rule.type == "temperature":
            if rule.variant == "low":
                return heatingValidation(temperature, humidity, self.targetTemperature, self.targetHumidity, rule.threshold)
            elif rule.variant == "high":
                return coolingValidation(temperature, humidity, self.targetTemperature, self.targetHumidity, rule.threshold)
        elif rule.type == "time":
            return timeValidation(rule.duration, rule.interval)
        else:
            return statusChange.NONE

    def evaluateRules(self, temperature, humidity):
        print("Evaluating Rules")
        for rule in self.rules:
            relaisController.switch(rule.relay, self.validateRule(rule, temperature, humidity))        

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

def timeValidation(duration, interval):
    """
    Determines if a relay should be powered based on the current time.

    Args:
        duration (float): Duration in minutes that the relay should be ON.
        interval (float): Total cycle interval in minutes.

    Returns:
        bool: True if the relay should be ON, False otherwise.
    """
    # Convert duration and interval from minutes to seconds
    duration_sec = duration * 60
    interval_sec = interval * 60

    # Get the current time in seconds since epoch
    current_time = time.time()

    # Find time elapsed within the current interval
    time_in_cycle = current_time % interval_sec

    if time_in_cycle < duration_sec:
        return statusChange.ON
    else:
        return statusChange.OFF

ruleEngine = RuleEngine()

