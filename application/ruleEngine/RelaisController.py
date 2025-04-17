try:
    RPi = __import__("RPi.GPIO")
except:
    random = __import__("random")

class RelaisController:
    def __init__(self, ports):
        self.ports = ports
        try:
            RPi.GPIO.setmode(RPi.GPIO.BCM)
            for i in self.ports:
                print(i)
                RPi.GPIO.setup(i, RPi.GPIO.OUT)
                RPi.GPIO.output(i, False)                  
        except NameError as error:
            print("RPi.GPIO not found, using mock GPIO")
    def addRelais(self, port):
        self.ports.append(port)
        self.setPorts(self.ports)
        return self.ports
    
    def removeRelais(self, port):
        self.ports.remove(port)
        self.setPorts(self.ports)
        return self.ports
    
    def setPorts(self, ports):
        self.ports = ports
        try:
            RPi.GPIO.cleanup()
            RPi.GPIO.setmode(RPi.GPIO.BCM)
            for i in self.ports:
                print(i)
                RPi.GPIO.setup(i, RPi.GPIO.OUT)
                RPi.GPIO.output(i, False)                  
        except NameError as error:
            print("RPi.GPIO not found, SETTING PORTS LIKE A BOOSSSSS")

    def getPortStatus(self, port):
        try:
            return RPi.GPIO.input(port)
        except NameError as error:
            print("RPi.GPIO not found, Beep Boop Port Status!")
            return random.choice([True, False])
    
    def getPorts(self):
        return self.ports

    def switch(self, number, status):
        try:
            if(status == -1) :
                RPi.GPIO.output(self.ports[number], False)
            elif(status == 1):
                RPi.GPIO.output(self.ports[number], True)          
        except NameError as error:
            print("RPi.GPIO not found, Beep Boop Switch!")

    def turnOn(self, number):
        try:
            RPi.GPIO.output(self.ports[number], True)        
        except NameError as error:
            print("RPi.GPIO not found, Beep Boop ON!")
        

    def turnOff(self, number):
        try:
            RPi.GPIO.output(self.ports[number], False)  
        except NameError as error:
            print("RPi.GPIO not found, Beep Boop OFF!")
relaisController = RelaisController([])