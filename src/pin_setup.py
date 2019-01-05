import RPi.GPIO as GPIO

class PinSetup:
  def __init__(self):
    self.furnacePin = 17 # pin 11 WARNING: CREATES 'PIN IN USE' WARNING
    self.tempPin = 27 # pin 13
    self.ioTestPin = 26 # pin 37
    self.runTestPin = 16 # pin 36

  def initializePins(self):
    # set mode for board pin numbering
    GPIO.setmode(GPIO.BCM)

    # Initialize pins
    GPIO.setup(self.furnacePin, GPIO.OUT)
    GPIO.setup(self.tempPin, GPIO.IN)
    GPIO.setup(self.ioTestPin, GPIO.IN)
    GPIO.setup(self.runTestPin, GPIO.IN)
