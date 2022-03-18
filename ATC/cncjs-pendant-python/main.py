import jwt
import socketio
import json
from pathlib import Path
import RPi.GPIO as GPIO
import time
import sys

sio = socketio.Client()

# CNCJS
SERVER_ADDRESS = 'ws://localhost:8000'
SERIAL_PORT = '/dev/ttyACM0'
SERIAL_BAUDRATE = 115200
CONTROLLER_TYPE = "Grbl"
SECRET = "$2a$10$L4U3VUiFL0v20q9cTmUdQu"
USER_ID = "1aef42b4-c34f-4469-abdd-51d344c9370b"
USER_NAME = "cncjs-pendant"
COMMAND = 'gcode:resume'

# RELAY
RELAY_1 = 4
RELAY_2 = 17

with open(str(Path('/app/ATC/config/cncrc.json'))) as cncrc:
  config = json.load(cncrc)

access_token =  jwt.encode(
                payload={'id': USER_ID, 'name': USER_NAME},
                key=config['secret'],
                algorithm='HS256')


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
      relay.set_off()
      sio.connect(SERVER_ADDRESS + '/socket.io/\?token=' + access_token)
      sio.sleep(2)
      sio.emit('open', (SERIAL_PORT, {'baudrate': SERIAL_BAUDRATE, 'controllerType': CONTROLLER_TYPE}))
      sio.sleep(2)
      sio.emit('command', (SERIAL_PORT, COMMAND))
      sio.sleep(2)
      sio.disconnect()
    elif "R2" == sys.argv[1]:
      relay = RelayControl(RELAY_2)
      relay.set_on()
      time.sleep(5)
      sio.connect(SERVER_ADDRESS + '/socket.io/\?token=' + access_token)
      sio.sleep(2)
      sio.emit('open', (SERIAL_PORT, {'baudrate': SERIAL_BAUDRATE, 'controllerType': CONTROLLER_TYPE}))
      sio.sleep(2)
      sio.emit('command', (SERIAL_PORT, COMMAND))
      sio.sleep(2)
      sio.disconnect()


  except:
    print("Unexpected error - ", sys.exc_info()[0], sys.exc_info()[1])
    raise

  finally:

    GPIO.cleanup()






