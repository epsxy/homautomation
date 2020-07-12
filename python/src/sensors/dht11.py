import Adafruit_DHT
from datetime import datetime
from rethinkdb import r
from dotenv import load_dotenv
from model.redb import ReDB
import time
import os


def read_temp_sensor(sensor, pin: int):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is None or temperature is None:
        pattern = 'Sensor got faulty values: ({},{}) as (*C, %)'
        print(pattern.format(temperature, humidity))
        read_temp_sensor()
    else:
        return temperature, humidity


def post_db_result(db: ReDB, temperature: int, humidity: int):
    r.db('dashboard').table('temperatures').insert({
        'timestamp': r.expr(datetime.now(r.make_timezone('+02:00'))),
        'location': 'SANDBOX',
        'value': temperature
    }).run(db.get_conn())
    r.db('dashboard').table('humidity').insert({
        'timestamp': r.expr(datetime.now(r.make_timezone('+02:00'))),
        'location': 'SANDBOX',
        'value': humidity
    }).run(db.get_conn())


def run(db_host: str, db_port: int, is_logger_enabled: bool,
        is_db_enabled: bool):
    sensor = Adafruit_DHT.DHT11
    pin = 2
    database = ReDB(db_host, db_port)
    if(is_db_enabled):
        print('DB {}:{} enabled'.format(database.host, database.port))
        database.connect()
    while True:
        temp, humidity = read_temp_sensor(sensor, pin)
        if(is_logger_enabled or True):
            print('{}*C, {}%'.format(temp, humidity))
        if(is_db_enabled):
            post_db_result(database, temp, humidity)
        time.sleep(3600)


if __name__ == '__main__':
    load_dotenv(verbose=True)

    mail = os.getenv('SMTP_MAIL')
    pwd = os.getenv('SMTP_PWD')
    port = 465
    is_mail_enabled = os.getenv('NOTIFICATION_ENABLED') == 'True'
    is_logger_enabled = os.getenv('LOG_ENABLED') == 'True'
    is_db_enabled = os.getenv('DB_ENABLED') == 'True'
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')

    run(db_host, db_port, is_logger_enabled,
        is_db_enabled)
