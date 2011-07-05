#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import relay
import os
import gtk

os_name=os.name

def gui_init(port):
	import gui
	MainWindow = gui.Gui(port)
	gtk.main()
			
if (os_name=="nt"):
	import gui
	file_config = file('turnon.cfg', 'r')
	gui_init(str(file_config.readline()[0:-1]))
	
elif (os_name=="posix"):
	import argparse
		
	parser = argparse.ArgumentParser(description='Control TurnON device from computer')
	parser.add_argument('-gui', help="Run TurnON with GUI", action='store_true', default=False)
	parser.add_argument('-p', help="Set the port is connected to Relay Card", action='store', default = 'none')
	parser.add_argument('-test', help="Run test to check connection with relay", action='store_true', default=False)
	parser.add_argument('-i', help="Info about status of all relays", action='store_true', default=False)
	parser.add_argument('-t', help="Turn single relay", action='store',nargs=2, type=int)
	parser.add_argument('-s', help="Set all relays", action='store')
	args = parser.parse_args()
	
	if (args.p == 'none'):
		file_config = file('turnon.cfg', 'r')
		
		if (args.gui):
			gui_init(str(file_config.readline()[0:-1]))
		else:
			import text
			text_mode = text.Text(str(file_config.readline()[0:-1]))
		
	else:
		if (args.gui):
			gui_init(args.p)
		else:
			import text
			text_mode = text.Text(args.p)
		
	if (args.test):
		text_mode.test()
		
	elif (args.i):
		text_mode.status()
		
	elif (args.t):
		text_mode.set_single(args.t)
		
	elif (args.s):
		text_mode.set_all(args.s)
		
else:
	print "Unsupported OS"
	exit()


