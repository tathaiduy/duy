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
# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.

ev3 = EV3Brick()
motor = Motor(Port.A)
# right_motor = motorB
# robot = DriveBase(left_motor, right_motor, wheel_diameter=55, axle_track=152)
# robot.settings(straight_speed=200, straight_acceleration=150, turn_rate=0)
while True:
    boolean = False
    try:
        
        obstacle_sensor = UltrasonicSensor(Port.S2)
        a = round(obstacle_sensor.distance())
        if a < 100:
            #Calculate Speed
            #Beeping Alert(1 score)
            ev3.speaker.beep(frequency=500, duration = 100)
            #Alert light on
            ev3.light.on(Color.RED) 
            #Print screen activate ( 1 score)
            ev3.screen.print("MEB activate") 
            #Slow down smoothly (1 point)
            speed_decrease = 500 - round((a - 3) * motor.speed()/a)
            while motor.speed() < 0:
                if motor.speed() - speed_decrease < 0:
                    motor.run(speed = motor.speed() - motor.speed())
                    break
                else:
                    motor.run(speed = motor.speed() - speed_decrease)
                    print("Motor speed: ",motor.speed())
                    time.sleep(0.01)
                b = round(obstacle_sensor.distance())
                if b < 3:
                    motor.run(speed = 0)
                    break    
            ev3.light.off()
            break   
    except:
        ev3.speaker.beep(frequency=500, duration = 100)
        ev3.screen.print("Ultrasonic Sensor is not connected. Please check again")
        boolean = True
if boolean == False:         
    ev3.screen.print("MEB deactivate")