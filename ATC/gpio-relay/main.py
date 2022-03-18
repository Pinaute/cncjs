import RPi.GPIO as GPIO
import time
import sys

# RELAY
RELAY_1 = 4
RELAY_2 = 17

class RelayControl():
  class RelayStates():
    ON  = 1
    OFF = 0

  def __init__(self, gpio_pin):
    self.__current_state = self.RelayStates.OFF
    self.__current_Relay_state = False
    self.gpio_pin = gpio_pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio_pin, GPIO.OUT)
    self.__set_off()

  def __set_on(self):
    self.__current_Relay_state = True
    GPIO.output(self.gpio_pin, True)

  def __set_off(self):
    self.__current_Relay_state = False
    GPIO.output(self.gpio_pin, False)

  def set_on(self):
    self.__current_state = self.RelayStates.ON
    self.__set_on()

  def set_off(self):
    self.__current_state = self.RelayStates.OFF
    self.__set_off()

if __name__ == "__main__":
  try:

    if "R1" == sys.argv[1]:
      relay = RelayControl(RELAY_1)
      relay.set_on()
      time.sleep(5)
    elif "R2" == sys.argv[1]:
      relay = RelayControl(RELAY_2)
      relay.set_on()
      time.sleep(5)

  except:
    print("Unexpected error - ", sys.exc_info()[0], sys.exc_info()[1])
    raise

  finally:
    relay.set_off()
    GPIO.cleanup()
