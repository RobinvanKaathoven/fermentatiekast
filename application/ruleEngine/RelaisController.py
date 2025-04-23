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

    def switch(self, port, status):
        try:
            if(status == -1) :
                RPi.GPIO.output(port, False)
            elif(status == 1):
                RPi.GPIO.output(port, True)          
        except NameError as error:
            print(f"RPi.GPIO not found, Beep Boop {port} to {status}!")

    def turnOn(self, port):
        try:
            RPi.GPIO.output(port, True)        
        except NameError as error:
            print("RPi.GPIO not found, Beep Boop ON!")
        

    def turnOff(self, port):
        try:
            RPi.GPIO.output(port, False)  
        except NameError as error:
            print("RPi.GPIO not found, Beep Boop OFF!")
relaisController = RelaisController([])
