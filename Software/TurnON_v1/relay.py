#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time

class Relay:
	
	def __init__(self, port):
		'''To init relay module yot musy set serial port ID'''
		
		self.ser = serial.Serial(port, 9600, timeout=1)
		time.sleep(1)
		
	def frame_is_ok(self, relay_answer):
		'''This funkction check correctness of frame received from device.
		In argument function get string with message from device.
		If format of frame is OK function return True. If format is bad
		function return False'''
		
		if relay_answer[0] == 'R' and relay_answer[-1] == '\r':
			return True			
		else:
			return False
	
	def test(self):
		'''This function check connection with device. If connection is OK
		function return True. If trasmitted data are bad function return False'''
		self.ser.write("RDn")
		relay_answer = self.ser.read(19)
		
		if relay_answer == "RelayCardByBigBen\n\r":
			return True			
		else:
			return False
			
	
	def command_was_execute(self):
		'''Function check that send command was execute.
		Funtion can return following values:
		0 - Everything was execute without problems
		-1 - Error with frame format
		1 - Command execute with sobe errors
		2 - Device received data with bad frame
		3 - Device received unknown command
		4 - Device received command with bad argument
		5 - Unknown error '''
		
		relay_answer = self.ser.read(6)
		
		if self.frame_is_ok(relay_answer) :
			pass			
		else:
			return -1
			
		if relay_answer == "Rcok\n\r":
			return 0
		elif relay_answer == "Rcer\n\r":
			return 1
		elif relay_answer == "Rerror01\n\r":
			return 2
		elif relay_answer == "Rerror02\n\r":
			return 3
		elif relay_answer == "Rerror03\n\r":
			return 4
		elif relay_answer == "Rerror04\n\r":
			return 5		
			
	def status(self):
		'''Function return string with current status of all relays
		Example return value: "111000"
		1 means "relay is turn on"
		0 means "relay is turn off"
		Function return False if was problem with format of frame'''
				
		self.ser.write("RIn")
		relay_answer = self.ser.read(9)
		
		if self.frame_is_ok(relay_answer):
			pass
		else:
			return False
		
		return relay_answer[1:8]
				
	def turn_all(self, user_command):
		'''Function get string with status of relays that must by set.
		Example string: "110011"
		In strang can't be no others chars. Only '1' and '0'.
		'1' means "turn on relay"
		'0' means "turn off relay"
		Function can return False if something go wrong and print in console text with error
		Function print "Bad user command" if get command have others chars than "1" and "0".
		"Error. Code: ..." means other error (got to "command_was_execute" funtion).
		If everything was executed without problems function return True '''
		
		relay_command = "RS"
		
		for i in range(0, 6):
			if user_command[i] == '0' or user_command[i] == '1':
				relay_command += user_command[i]				
			else:
				print "Bad user command"
				return False
				
		relay_command += 'n'
		self.ser.write(relay_command)
		tmp = self.command_was_execute()
		
		if tmp == 0:
			return True
		else:
			print "Error. Code:", tmp
			return False
	
	def turn(self, relay_number, command):
		'''Function gets 2 argument. First "relay_number" means number (1-6) of relay who you want set
		If number is bad function return False and print "Bad relay number".
		Second argument "command" means state of this relay that you want set (only "1" and "0").
		If everything was execute without problems function return True'''
		
		if relay_number<1 or relay_number>6:
			print "Bad relay number"
			return False
		else:
			pass 

			
		status_all = self.status()
		relay_number -= 1
		relay_command = status_all[0:relay_number] + command + status_all[relay_number+1:]
		self.turn_all(relay_command)
		return True
