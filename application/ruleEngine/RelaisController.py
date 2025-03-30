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
