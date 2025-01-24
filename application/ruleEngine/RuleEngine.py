from ruleEngine.Rule import Rule
class RuleEngine:
    def __init__(self, temperatureSensor):
        self.temperatureSensor = temperatureSensor
        self.rules = []
        self.addRule(Rule("hydrate", hydrateValidation, controlHydratingHeater))
        self.addRule(Rule("dehydrate", dehydrateValidation, controlDehydrator))
        self.addRule(Rule("heating", heatingValidation, controlLampHeater))
        self.addRule(Rule("cooling", coolingValidation, controlFridge))

    def addRule(self, rule):
        self.rules.append(rule)
    
    def evaluateRules(self):
        print("Evaluating Rules")
        value = self.temperatureSensor.read()
        for rule in self.rules:
            rule.evaluate(value[0].value, value[1].value)

def controlHydratingHeater(validation):
    if(validation) :
        print("Turning on Waterheater")
    else:
        print("Turning off Waterheater") 
def controlDehydrator(validation):
    if(validation) :
        print("Turning on Dehydrator")
    else:   
        print("Turning off Dehydrator")
def controlLampHeater(validation):
    if(validation) :
        print("Turning on Lamp heater")
    else:
        print("Turning off Lamp heater")
def controlFridge(validation):
    if(validation) :
        print("Turning on Fridge")
    else:
        print("Turning off Fridge")

def hydrateValidation(temperature, humidity):
    if humidity < 40:
        return True
    return False

def dehydrateValidation(temperature, humidity):
    if humidity > 60:
        return True
    return False

def heatingValidation(temperature, humidity):
    if temperature < 15:
        return True
    return False

def coolingValidation(temperature, humidity):
    if temperature > 25:
        return True
    return False


