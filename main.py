#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import threading
import time
import sys
# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.

ev3 = EV3Brick()
motor = Motor(Port.A)
# right_motor = motorB
# robot = DriveBase(left_motor, right_motor, wheel_diameter=55, axle_track=152)
# robot.settings(straight_speed=200, straight_acceleration=150, turn_rate=0)

try:
    obstacle_sensor = UltrasonicSensor(Port.S1)
except:
    ev3.speaker.beep(frequency=500, duration = 100)
    ev3.screen.print("UltrasonicSensor is not connected. Please check again")
    sys.exit()
motor.run(speed=600)    
while True:
        a = round(obstacle_sensor.distance())
        if a < 200:
            #Calculate Speed
            #Beeping Alert(1 score)
            ev3.speaker.beep(frequency=500, duration = 1000)
            #Alert light on
            ev3.light.on(Color.RED) 
            #Print screen activate ( 1 score)
            #Slow down smoothly (1 point)
            speed_decrease = motor.speed() - round((a - 3) * motor.speed()/a) 
            while motor.speed() > 0:
                b = round(obstacle_sensor.distance())
                if b  < 50:
                    motor.run(speed = 0)
                    break 
                if motor.speed() - speed_decrease < 0:
                    motor.run(speed = motor.speed() - motor.speed())
                    break
                else:
                    motor.run(speed = motor.speed() - speed_decrease)
                    time.sleep(0.01)
            c = round(obstacle_sensor.distance())   
            ev3.light.off()
            ev3.screen.print(c)
            ev3.screen.print("MEB activate")

        elif a > 200:
            motor.run(speed = 600)
