# ESP8266_Micropython_Robotic_Car

![car1](https://github.com/cheungbx/esp8266_Micropython_Robotic_Car/blob/master/car1.jpg) 
![car2](https://github.com/cheungbx/esp8266_Micropython_Robotic_Car/blob/master/car2.jpg) 
![car3](https://github.com/cheungbx/esp8266_Micropython_Robotic_Car/blob/master/webpage.jpg) 
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
