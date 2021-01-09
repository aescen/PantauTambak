#!/usr/bin/env/python2
import os, sys, time, pymysql
import RPi.GPIO as GPIO

# Database setup..
## Create connection to MySQL server
print("Connecting ...")
try:
    connection = pymysql.connect(host='localhost',
                                 user='pi',
                                 password='raspberry',
                                 db='pi',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
except pymysql.err.Error as msg:
    print("Connection error: ", msg)
    exit()
## Create cursor
cc = connection.cursor()
#----------------------------------------------------------------------------------------->
 
SENSOR_PIN1 = 21
SENSOR_PIN2 = 20
RELAY_PIN1 = 16
RELAY_PIN2 = 26
pir1 = 0
pir2 = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN1, GPIO.IN)
GPIO.setup(SENSOR_PIN2, GPIO.IN)
GPIO.setup(RELAY_PIN1, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RELAY_PIN2, GPIO.OUT, initial=GPIO.HIGH)
 
try:
    while True:
        time.sleep(0.1)
        pir1 = GPIO.input(SENSOR_PIN1)
        pir2 = GPIO.input(SENSOR_PIN2)
        if pir1 == 1:
            print("Movement on sensor 1!")
            GPIO.output(RELAY_PIN1, GPIO.LOW)
        if pir2 == 1:
            print("Movement on sensor 2!")
            GPIO.output(RELAY_PIN2, GPIO.LOW)
        if pir1 == 0:
            print("No movement on sensor 1!")
            GPIO.output(RELAY_PIN1, GPIO.HIGH)
        if pir2 == 0:
            print("No movement on sensor 2!")
            GPIO.output(RELAY_PIN2, GPIO.HIGH)
        try:
            result1 = "UPDATE `motion` SET `deteksi`='%s' WHERE `motion`.`sensor` = 'pir1';" % (pir1)
            cc.execute(result1)
            connection.commit()
            result2 = "UPDATE `motion` SET `deteksi`='%s' WHERE `motion`.`sensor` = 'pir2';" % (pir2)
            cc.execute(result2)
            connection.commit()
        except pymysql.err.InternalError as msg:
                    print("Command skipped: ", msg)
        time.sleep(1)
except KeyboardInterrupt:
    print("Finish...")
GPIO.cleanup()