from gpiozero import DigitalInputDevice  # type: ignore
from time import sleep



pin = DigitalInputDevice(21, pull_up=False)

while True:
    print(pin.value)
    sleep(1)
