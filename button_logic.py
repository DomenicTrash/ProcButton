import RPi.GPIO as GPIO

import db_logic
import display_controller

button1 = 23


def main_button():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button1, GPIO.IN)
    GPIO.add_event_detect(button1, GPIO.RISING, callback = on_click, bouncetime = 500)


def on_click(channel):
    print("Updated databank and display.")
    db_logic.add_incremented_row()
    display_controller.create_and_display_image()


def on_click_test(channel):
    print("clicked " + channel)
