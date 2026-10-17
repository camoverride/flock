from gpiozero import LED  # type: ignore
from time import sleep



led = LED(17)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
