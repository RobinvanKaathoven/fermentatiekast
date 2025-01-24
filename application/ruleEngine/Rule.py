class Rule():
    def __init__(self, name, validationFunction, controlFunction):
        self.name = name
        self.validationFunction = validationFunction
        self.controlFunction = controlFunction
    def evaluate(self, temperature, humidity):
        self.controlFunction(self.validationFunction(temperature, humidity))