try:
        adafruit_dht = __import__("RPi.GPIO")
except:
        random = __import__("random")
# import RPi.GPIO as GPIO

class RelaisController:
    def __init__(self, ports):
        self.ports = ports
        try:
            RPi.GPIO.setmode(GPIO.BCM)
            for i in self.ports.length:
                RPi.GPIO.setup(self.ports[i], RPi.GPIO.OUT)
                RPi.GPIO.output(self.ports[i], False)                  
        except NameError as error:
            print("RPi.GPIO not found, using mock GPIO")
                    
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
