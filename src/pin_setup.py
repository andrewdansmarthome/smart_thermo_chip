import RPi.GPIO as GPIO

class PinSetup:
  def __init__(self):
    self.furnacePin = 17 # pin 11 CREATES 'PIN IN USE' WARNING
    self.tempPin = 27 # pin 13
    self.ioTestPin = 26 # pin 37
    self.runTestPin = 16 # pin 36
    self.clk = 21
    self.cs = 8
    self.miso = 19
    self.mosi = 20
    self.initializePins()

  def initializePins(self):
    # set mode for board pin numbering
    GPIO.setmode(GPIO.BCM)

    # Initialize pins
    GPIO.setup(self.furnacePin, GPIO.OUT)
    GPIO.setup(self.tempPin, GPIO.IN)
    GPIO.setup(self.ioTestPin, GPIO.IN)
    GPIO.setup(self.runTestPin, GPIO.IN)
