#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__=="__main__":
	exit()
else:
	pass
	
import relay

class Text:
	def __init__(self, port):
		self.rel = relay.Relay(port)
		
	#test connection
	def test(self):
		if self.rel.test()==True:
			print "Connection OK"
		else:
			print "Error with connection"
		exit()
		
	#info about relay
	def status(self):
		status=self.rel.status()
			
		for i in range(0, 6):
			if status[i]=='1':
				j = "ON"
			else:
				j = "OFF"
			
			print "Relay", i, "is Turn", j
		exit()
		
	#set single relay	
	def set_single(self, arg_t):
		tmp=arg_t
		self.rel.turn(tmp[0], str(tmp[1]))
		exit()
	
	#set all relays
	def set_all(self, arg_s):	
		if len(arg_s)!=6:
			print "Yot must set status of all relays"
			exit()
		else:
			pass
		
		self.rel.turn_all(arg_s)
		exit()	
		
	
