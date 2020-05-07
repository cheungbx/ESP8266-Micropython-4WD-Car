# Author: cheungbx  2020/04/30
# ESP8266 Micropython WIFI remote control and Autodrive car
#
# Pin layout and connections
# ----------------------------------
# PCA9685 16xPWM  module to Wemos D1 Mini (ESP8266)
# -----------------------------------1
# GND -> GND
# VCC -> +5V
# SCL -> D1
# SDA -> D2
# VCC+ -> +5V
# -----------------------------------
# Motor to Dual L298N  4 motor module to PCA9685
# -----------------------------------1
# Front Left motor +ve   -> IN1 -> PWM0
# Front Left motor -ve   -> IN2 -> PWM1
# Back Left motor +ve    -> IN3 -> PWM2
# Back Left motor -ve    -> IN4 -> PWM3
# Front Rightt motor +ve -> IN5 -> PWM4
# Front Right motor -ve  -> IN6 -> PWM5
# Back Right motor +ve   -> IN7 -> PWM6
# Back Right motor -ve   -> IN8 -> PWM7
# ENA -> +5V (use on board jumper)
# ENB -> +5V (use on board jumper)
# ENC -> +5V (use on board jumper)
# END -> +5V (use on board jumper)
# VCC -> +7.4V (two 3.7V rechargable LIPO battery in series)
# GND -> GND of Wemos D1 Mini
# 5V  -> +5V of Wemons D1 Mini
# -----------------------------------
# servo Motor to PCA9685
# -----------------------------------
# (brown) GND  -> GND
# (red)   VCC  -> VCC
# (orange)Sig  -> PWM8
# -----------------------------------
# Ultrasound Sensor hcsr04 to Wemos D1 Mini
# -----------------------------------
# GND  -> GND
# Echo -> D8->GPIO-15
# Trig -> D7->GPIO-13
# VCC  -> +5V

import socket
import machine
import time
from machine import Pin, PWM, ADC, time_pulse_us, I2C
from time import sleep, sleep_us, sleep_ms
import ssd1306
import hcsr04
from hcsr04 import HCSR04
i2c = I2C(-1, Pin(5), Pin(4))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.fill(0)
display.text("uPython Car v1.0",0,28)
display.show()
import pca9685
pca = pca9685.PCA9685(i2c)
pca.freq(50)
pca.duty(8,1000)
import servo
servos = servo.Servos(i2c)

wifissid = 'yourwifissid'
wifipass = 'yourwifipassword'

sensor = HCSR04(trigger_pin=13, echo_pin=15)

servo_right = 20
servo_centre = 90
servo_left = 160
servo_delay = 250
pwm_servo = 8

servos.position(pwm_servo, degrees=servo_centre)

pwm_FL = 0
pwm_BL = 2
pwm_FR = 4
pwm_FL = 6

minspeed = 1500
midspeed = 2500
maxspeed = 4095
speed = midspeed
action = 0

auto=False

def forward_distance () :
  servos.position(pwm_servo, degrees=servo_centre)
  return sensor.distance_cm()

def right_distance () :
  servos.position(pwm_servo, degrees=servo_right)
  sleep_ms(servo_delay)
  return sensor.distance_cm()

def left_distance () :
  servos.position(pwm_servo, degrees=servo_left)
  sleep_ms(servo_delay)
  return sensor.distance_cm()


#HTML to send to browsers
html = """<!DOCTYPE html>
<html>
<head>
<title>Car</title>
<style>
body {background-color: black}
h1 {color:red}
button {
        color: white;
        height: 200px;
        width: 200px;
        background:black;
        border: 3px solid #4CAF50; /* Green */
        border-radius: 50%;
        font-size: 250%;
        position: center;
}
</style>
</head>
<body>
<center>
<form>
<div><button name="CMD" value="l" type="submit">L</button>
<button name="CMD" value="forward" type="submit">Forward</button>
<button name="CMD" value="r" type="submit">R</button></div>
<div><button name="CMD" value="left" type="submit">Ls</button>
<button name="CMD" value="stop" type="submit">Stop</button>
<button name="CMD" value="right" type="submit">Rs</button></div>
<div><button name="CMD" value="back" type="submit">Back</button></div>
<div><button name="CMD" value="slow" type="submit">Slow</button>
<button name="CMD" value="mid" type="submit">Mid</button>
<button name="CMD" value="fast" type="submit">Fast</button>
<button name="CMD" value="auto" type="submit">Auto</button></div>
</form>
</center>
</body>
</html>
"""

def show(text) :
  display.fill(0)
  display.text("uPython Car v1.0",0,0)
  text = "Auto " + text if auto else text
  display.text(text,0,32)
  display.show()

def stop(t=0):
  show ("Stop")
  for i in range(0, 8):
    servos.position(i, duty=0)
  if t > 0 :
    sleep_ms(t)

def forward(t=0):
  show("forward")
  for i in range(0, 8):
    servos.position(i, duty=speed  if i % 2 == 0 else 0)
  if t > 0 :
    sleep_ms(t)

def back(t=0):
  show("back")
  for i in range(0, 8):
    servos.position(i, duty=speed  if i % 2 != 0 else 0)
  if t > 0 :
    sleep_ms(t)

def left (t=0):
  show("left")
  for i in range(0, 8):
    if i > 3 :
      servos.position(i, duty=speed  if i % 2 == 0 else 0)
    else :
      servos.position(i, duty=speed  if i % 2 != 0 else 0)
  if t > 0 :
    sleep_ms(t)


def right (t=0):
  show("right")
  for i in range(0, 8):
   if i > 3 :
     servos.position(i, duty=speed  if i % 2 != 0 else 0)
   else :
     servos.position(i, duty=speed  if i % 2 == 0 else 0)
  if t > 0 :
    sleep_ms(t)


def left_cruise (t=0):
  show("left cruise")
  for i in range(0, 8):
    if i > 3 :
      servos.position(i, duty=speed  if i % 2 == 0 else minspeed)
    else :
      servos.position(i, duty=speed  if i % 2 != 0 else minspeed)
  if t > 0 :
    sleep_ms(t)

def right_cruise (t=0):
  show("right cruise")
  for i in range(0, 8):
   if i > 3 :
     servos.position(i, duty=speed  if i % 2 != 0 else minspeed)
   else :
     servos.position(i, duty=speed  if i % 2 == 0 else minspeed)
  if t > 0 :
    sleep_ms(t)

def autoDrive () :
  # check distance from obstacles in cm.
  fd = forward_distance()
  print('forward ', fd)
  # then take actions in milli seconds
  if fd < 10 :
     stop(100)
     back(200)
     print ("+Auto Stop back")
  elif fd < 25 :
      stop(100)
      ld=left_distance ()
      rd=right_distance ()
      print('L ',ld, ' R ', rd)

      if ld < 15 and rd < 15 :
        # backward
        back(800)
        left(300)
        print ("+Auto back left")

      elif ld > rd :
        # left
        back(100)
        left(300)
        print ("+Auto left")

      else : # ld <= rd
        # right
        back(100)
        right(300)
        print ("+Auto right")
  else  : # >= 25
    # forward
    forward (100)
    print ("+Auto forward")

def remoteControl () :
    global auto, s, action, speed
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print("Content = %s" % str(request))
    request = str(request)

    if request.find('/?CMD=forward') == 6:
        print('+forward')
        action = 1
    elif request.find('/?CMD=back') == 6:
        print('+back')
        action = 2
    elif request.find('/?CMD=left') == 6:
        print('+left')
        action = 3
    elif request.find('/?CMD=right') == 6:
        print('+right')
        action = 4
    elif request.find('/?CMD=l') == 6:
        print('+L')
        action = 5
    elif request.find('/?CMD=r') == 6:
        print('+R')
        action = 6
    elif request.find('/?CMD=stop') == 6:
        print('+stop')
        action = 0
    elif request.find('/?CMD=fast') == 6:
        print('+fast=')
        speed = maxspeed
        print (speed)
    elif request.find('/?CMD=slow') == 6:
        print('+slow=')
        speed = minspeed
        print (speed)
    elif request.find('/?CMD=mid') == 6:
        print('+mid=')
        speed = midspeed
        print (speed)
    elif request.find('/?CMD=man') == 6:
        auto=False
        action = 0
        print('+manual=')
    elif request.find('/?CMD=auto') == 6:
        auto=True
        action = 0
        print('+autoDrive')

    if action == 0:
        stop ()
    elif action == 1:
        forward()
    elif action == 2:
        back()
    elif action == 3:
        left()
    elif action == 4:
        right()
    elif action == 5:
        left_cruise()
    elif action == 6:
        right_cruise()

    response = html
    conn.send(response)
    conn.close()

# main program starts here
print (forward_distance())

stop()

import network

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifissid,wifipass)
count = 7
while not wifi.isconnected() and count > 0 :
    count -= 1
    print ('.')
    time.sleep(1)

if wifi.isconnected() :
    print('network config:', wifi.ifconfig())

    #Setup Socket WebServer
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = socket.socket()


    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(('', 80))
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:80/")
else  :
    print('No Wifi. Auto Mode')
    auto = True


while True:
    if auto :
        autoDrive()
    elif wifi.isconnected()  :
        remoteControl()
