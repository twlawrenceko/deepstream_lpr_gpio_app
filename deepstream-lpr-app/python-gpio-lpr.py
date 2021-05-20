#!/usr/bin/env python
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
import RPi.GPIO as GPIO
import time
import subprocess


# Pin Definitions
GPIO_TRIGGER = 18  # BCM pin 18, BOARD pin 12
GPIO_ECHO = 24
LED_Control = 22
Light_detect = 23

command = "nvgstcapture --mode=2 --automate --capture-auto --video-res=3 --capture-time=5 --file-name=video"
command2 = "cp video*.mp4 video.mp4"
detection_command = "/home/lawrenceko/deepstream_lpr_app/deepstream-lpr-app/deepstream-lpr-app 1 3 0 video.mp4 output.264"
command3 = "rm video*"
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance

def main():
    prev_value = None
    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # set pin as an OUTPUT pin
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.setup(LED_Control, GPIO.OUT)
    GPIO.setup(Light_detect, GPIO.IN)
    print("Starting MEASURING now! Press CTRL+C to exit")
    try:
        while True:
            light_value = GPIO.input(Light_detect)
            
            dist = distance()
            print("Measured Distance = %.1f cm" % dist)
            print("ligtht value:%.1f "% light_value)
            
            if(dist <100):
                #start record the video
                print("Vehicle may be detected")
                if light_value==1:
                    GPIO.output(LED_Control, True)
                
                else:
                    GPIO.output(LED_Control, False)
                subprocess.run(command3, shell=True)
                print("video temp file cleared")
                subprocess.run(command.split())
                subprocess.run(command2, shell=True)
                subprocess.run(detection_command.split())
                subprocess.call(command3, shell=True)
                print("video temp file deleted")
            else:
                GPIO.output(LED_Control, False)

            time.sleep(1)
    finally:
        GPIO.cleanup()
if __name__ == '__main__':
    main()
