#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__=="__main__":
	exit()
else:
	pass
	
import pygtk, gtk, gtk.glade
import relay
import json

class Gui:
	def __init__(self, port):
			
		self.gladefile = "turnon_gui.glade"
		self.wTree = gtk.glade.XML(self.gladefile)
		
		#add IDs for widgets
		self.mainWindow = self.wTree.get_widget("MainWindow")
		self.button_open = self.wTree.get_widget("button_open")
		self.button_save = self.wTree.get_widget("button_save")
		self.button_setAll = self.wTree.get_widget("button_setAll")
		self.button_options = self.wTree.get_widget("button_options")
		self.statusbar = self.wTree.get_widget("statusbar")
		
		#options window
		self.optionsWindow = self.wTree.get_widget("OptionsWindow")
		self.about_dialog = self.wTree.get_widget("aboutdialog")
		self.serial_label = self.wTree.get_widget("serial_label")
		self.serial_entry = self.wTree.get_widget("serial_entry")
		self.apply_button = self.wTree.get_widget("apply_button")
		self.cancel_button = self.wTree.get_widget("cancel_button")
		self.about_button = self.wTree.get_widget("about_button")
		
		self.button = []
		self.label = []
		self.image = []
		self.checkbutton = []
		
		self.ids_entry = [] #options window
		
				
		for i in range(1, 7):
			j=str(i)
			
			self.button.append(self.wTree.get_widget("button_relay"+j))
			self.label.append(self.wTree.get_widget("label_relay"+j))
			self.image.append(self.wTree.get_widget("image_relay"+j))
			self.checkbutton.append(self.wTree.get_widget("checkbutton_relay"+j))
			
			self.ids_entry.append(self.wTree.get_widget("ids_entry"+j)) #options window
							
		self.wTree.signal_autoconnect(self)
		
		for i in range(0, 6):
			self.button[i].connect("clicked", self.set_single, i)
		
		self.status()
		self.statusbar_context = self.statusbar.get_context_id("Serial port status")

		self.port_copy = port
		
		try:
			self.rel = relay.Relay(port)
			self.statusbar.push(self.statusbar_context, "Ready")
		except:
			self.statusbar.push(self.statusbar_context, "Failed to connect to a serial port. Change settings and restart program.")
							
	def on_MainWindow_destroy(self, widget):
		gtk.main_quit()
	
	def status(self):
		try:
			status=self.rel.status()
			
			for i in range(1, 7):
				j = i-1
				if status[j] == '1':
					self.button[j].set_label("Turn OFF")
					self.image[j].set_from_file("on.png")
			
				elif status[j] == '0':
					self.button[j].set_label("Turn ON ")
					self.image[j].set_from_file("off.png")
		
		except:
			statusbar_context = self.statusbar.get_context_id("Serial port status")
			self.statusbar.push(statusbar_context, "Failed to connect to a serial port. Change settings and restart program.")
			status = ['0', '0', '0', '0', '0', '0']	
			
		return status
	
	def set_single(self, widget, relay_number):
		status = self.status()
		
		if status[relay_number] == '0':
			self.rel.turn(relay_number+1, '1')
		elif status[relay_number] == '1':
			self.rel.turn(relay_number+1, '0')
			
		self.status()	
	
	def on_button_setAll_clicked(self, widget):
		status = self.status()
		command = "000000"
		
		for i in range(0, 6):
			j = i+1
			self.active =  self.checkbutton[i].get_active()
			
			if self.active:
				command = command[0:i]+'1'+command[j:]
			else:
				command = command[0:i]+'0'+command[j:]
				
		self.rel.turn_all(command)
		self.status()
		
	def prepare_data_save(self):
		status = self.status()


		data = [ {self.label[0].get_text() : status[0]},
			{self.label[1].get_text() : status[1]},
			{self.label[2].get_text() : status[2]},
			{self.label[3].get_text() : status[3]},
			{self.label[4].get_text() : status[4]},
			{self.label[5].get_text() : status[5]} ]
			
		return json.dumps(data)
		
	def prepare_data_open(self, data):
		return json.loads(data)
		
	def relay_label_refresh(self, relays_id):
		for i in range(0, 6):
			self.label[i].set_text( relays_id[i] )
		
	def execute_open_data(self, data):
		relays_id = []
		relays_status = []
		
		for i in range(0, 6):
			relays_id.append( "".join( data[i].keys() ) )
			relays_status.append(data[i][ relays_id[i] ])
						
		self.relay_label_refresh(relays_id)
		self.rel.turn_all(relays_status)
		self.status()
		
	def filefilter_init(self):
		filefilter = gtk.FileFilter()
		filefilter.add_pattern("*.turnon")
		return filefilter
		
	def on_button_open_clicked(self, widget):
		open_window = gtk.FileChooserDialog("Open", self.mainWindow, gtk.FILE_CHOOSER_ACTION_OPEN)
		open_window.add_button(gtk.STOCK_OPEN, 1)
		open_window.add_button(gtk.STOCK_CANCEL, 0)
		open_window.set_default_response(1)
		open_window.set_filter( self.filefilter_init() )
		
		if open_window.run():
			name_file = open_window.get_filename()
			relay_file = file(name_file, 'r')
			data = relay_file.readline()[0:]
			data_processed = self.prepare_data_open(data)
			self.execute_open_data(data_processed)
		
		open_window.destroy()
	
	def on_button_save_clicked(self, widget):
		save_window = gtk.FileChooserDialog("Save", self.mainWindow, gtk.FILE_CHOOSER_ACTION_SAVE)
		save_window.add_button(gtk.STOCK_SAVE, gtk.RESPONSE_OK)
		save_window.add_button(gtk.STOCK_CANCEL, 0)
		save_window.set_default_response(gtk.RESPONSE_OK)
		save_window.set_do_overwrite_confirmation(True)
		save_window.set_filter( self.filefilter_init() )
		
		if save_window.run(): 
			name_file = save_window.get_filename()
			
			if self.filename_is_ok(name_file):
				pass
			else:
				name_file += ".turnon"
			
			data = self.prepare_data_save()
			relay_file = file(name_file, 'w')
			relay_file.write(data)
			relay_file.flush()
		else:
			pass
		
		save_window.destroy()
		
	def filename_is_ok(self, name_file):
		if name_file[-7:] == ".turnon":
			return 1
		else:
			return 0
			
	def on_button_options_clicked(self, widget):
		for i in range(0, 6):
			tmp = self.label[i].get_text()
			self.ids_entry[i].set_text(tmp)
			
		self.serial_entry.set_text(self.port_copy)
		
		self.optionsWindow.show()
		
	def on_apply_button_clicked(self, widget):
		relays_id = []
		
		for i in range(0, 6):
			relays_id.append( self.ids_entry[i].get_text() )		
		
		self.relay_label_refresh(relays_id)
		
		new_port = self.serial_entry.get_text() + "\n"
		config_file=file("turnon.cfg", 'w')
		config_file.write(new_port)
		config_file.flush()
		
		self.optionsWindow.hide()
		
	def on_cancel_button_clicked(self, widget):
		self.optionsWindow.hide()
		
	def on_about_button_clicked(self, widget):
		self.about_dialog.run()
		self.about_dialog.hide()
