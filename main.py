# Execute this file to run program
import threading
import time

import schedule
from RPi import GPIO

import button_logic
import db_logic


def test_schedule():
    print("1 minute passed")


def update_at_night():
    schedule.every(1).minutes.do(test_schedule)
    # schedule.every().day.at("00:01").do(db_logic.check_if_row_was_added)
    while True:
        schedule.run_pending()
        time.sleep(1)


def run():
    nightly_update_thread = threading.Thread(target = update_at_night)
    nightly_update_thread.start()
    try:
        # addd event_detects:
        button_logic.main_button()
        while True:
            time.sleep(100)
    finally:
        print("cleanup")
        GPIO.cleanup()


if __name__ == '__main__':
    db_logic.drop_table_db()
    db_logic.create_db()
    run()
