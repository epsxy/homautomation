import time
import os
import RPi.GPIO as GPIO
from datetime import datetime
from dotenv import load_dotenv
from rethinkdb import r
from model.notifier import Notifier
from model.door import Door
from model.redb import ReDB


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)


def post_db_result(db: ReDB, is_opened: bool):
    r.db('dashboard').table('doors').insert({
        'timestamp': r.expr(datetime.now(r.make_timezone('+02:00'))),
        'location': 'MAIN',
        'opened': is_opened
    }).run(db.get_conn())


def run(mail: str,
        pwd: str,
        port: int,
        db_host: str,
        db_port: int,
        is_mail_enabled: bool,
        is_logger_enabled: bool,
        is_db_enabled: bool):
    door = Door()
    notifier = Notifier(mail, pwd, port)
    database = ReDB(db_host, db_port)
    if(is_db_enabled):
        print('DB {}:{} enabled'.format(database.host, database.port))
        database.connect()
    try:
        while True:
            sensor_input = GPIO.input(18)
            is_door_open = True if sensor_input == 1 else False
            if(is_door_open):
                if(is_logger_enabled):
                    print('opened')
                is_transition = door.open(is_mail_enabled, notifier)
            else:
                if(is_logger_enabled):
                    print('closed')
                is_transition = door.close(is_mail_enabled, notifier)
            if(is_transition and is_db_enabled):
                post_db_result(database, is_door_open)
            time.sleep(2)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    load_dotenv(verbose=True)

    port = 465
    mail = os.getenv('SMTP_MAIL')
    pwd = os.getenv('SMTP_PWD')
    is_mail_enabled = os.getenv('NOTIFICATION_ENABLED') == 'True'
    is_logger_enabled = os.getenv('LOG_ENABLED') == 'True'
    is_db_enabled = os.getenv('DB_ENABLED') == 'True'
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')

    print('Mail notifications are {}'.format(
        'enabled' if is_mail_enabled else 'disabled')
    )

    print('Logger is {}'.format(
        'enabled' if is_logger_enabled else 'disabled')
    )

    setup_gpio()
    run(mail,
        pwd,
        port,
        db_host,
        db_port,
        is_mail_enabled,
        is_logger_enabled,
        is_db_enabled)
