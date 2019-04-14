#!/usr/bin/python3
#
#  
# This is a python3 demo of controlling a Nanotec CL3-E-1-0F stepping motor controller using CANopen with PiCAN2 board.
#
# http://skpang.co.uk/catalog/pican2-canbus-board-for-raspberry-pi-2-p-1475.html
#
# Make sure PiCAN driver is installed first http://skpang.co.uk/blog/archives/1165
# 
# Then install the following:
# pip install python-can
# pip3 install canopen
#
# This programs requires the CL3.eds file to be in the same directory as the pican2_canopen_test.py file
#
# 14-04-19 SK Pang
#

import RPi.GPIO as GPIO
import canopen
import os
import time

led = 22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led,GPIO.OUT)

os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")  # Bring up can0 driver
time.sleep(0.1)

network = canopen.Network()
network.connect(channel='can0', bustype='socketcan')

node_id = 2
node = network.add_node(node_id, 'CL3.eds')		# Set node id and load eds file
node.nmt.state = 'OPERATIONAL'

node.sdo['Modes of operation'].raw = 0x02		# Set velocity mode
node.sdo['Polarity'].raw = 0x00					# Set clockwise
node.sdo['Peak current'].raw = 1000				# Set peak current to 1000mA
node.sdo['vl velocity acceleration'][2].raw = 2 # Set acceleration
node.sdo['vl velocity deceleration'][2].raw = 1 # Set deceleration

node.sdo['Controlword'].raw = 0x0				# Set DS402 Power State machine
node.sdo['Controlword'].raw = 0x80
node.sdo['Controlword'].raw = 0x06
node.sdo['Controlword'].raw = 0x07
node.sdo['Controlword'].raw = 0x0f

print('run')
GPIO.output(led,True)

node.sdo['vl target velocity'].raw = 100		# Set target speed
time.sleep(3)

print('Stopping')
node.sdo['vl target velocity'].raw = 0			# Stop
time.sleep(1)

node.sdo['Polarity'].raw = 0x40					# Set counter clockwise

node.sdo['vl target velocity'].raw = 100		# Set target speed
time.sleep(3)

print('Stopping')
node.sdo['vl target velocity'].raw = 0x00       # Stop
time.sleep(3)

node.nmt.state = 'STOPPED'

GPIO.output(led,False)