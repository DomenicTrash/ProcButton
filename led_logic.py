import RPi.GPIO as GPIO


# GPIO.setmode(GPIO.BCM)
# GPIO.setup(7, GPIO.OUT)
#
# print("LED on")
# GPIO.output(7, True)
# time.sleep(3)
# print("LED off")
# GPIO.output(7, False)
# GPIO.cleanup()
# print(1)


def led1():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(7, GPIO.OUT)

    if GPIO.input(7) == False:
        GPIO.output(7, True)
    else:
        GPIO.output(7, False)
    print("LED changed")


if __name__ == "__main__":
    led1()
    GPIO.cleanup()
