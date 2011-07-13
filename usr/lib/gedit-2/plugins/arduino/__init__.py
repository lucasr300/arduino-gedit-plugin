# -*- coding: utf-8 py-indent-offset: 4 -*-
#
#	Gedit Arduino Integration plugin
#	Copyleft (C) 2011 lrmartins.com
#
#	Author: Lucas R. Martins <lukasrms (at) )gmail.com>
#
#	This program is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; either version 2 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program; if not, write to the Free Software
#	Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# 	TODO: Bug: Gedit doesn't save the file automatically. User needs save the file before compiling.

import gedit
import gtk
import gettext
import os
import fileinput
import time
import serial
import sys


class ArduinoPlugin(gedit.Plugin):
	
	def activate(self, window):

		self._window = window
		self._doc = self._window.get_active_document()
		self._st = self._window.get_statusbar()
		manager = self._window.get_ui_manager()  

		self._action_group = gtk.ActionGroup("GeditArduinoPluginActions")

		self._action_group.add_actions([
			('arduino-templates',
				None,
				_('Exemplos de Código'),
				None,
				_('Open the code samples directory'),
				self.show_templates),
			('arduino-verificar',
				None,
				_('Verificar/Compilar'), 
				None,
				_('Compile and look for errors in current sketch'),
				self.compilar),		
			('arduino-enviar', 
				None,
				_('Upload'),
				'F7',
				_('Upload and send to Arduino'),
				self.upload),
			('arduino-settings', 
				None,
				_('Configurações'),
				None,
				_("Open the Arduino plugin's settings dialog"),
				self.create_configure_dialog)])	

		self._merge_id = manager.new_merge_id()
		manager.insert_action_group(self._action_group, -2)	
		manager.add_ui(self._merge_id, '/MenuBar/ToolsMenu/ToolsOps_4',
		'arduino-templates', 'arduino-templates', gtk.UI_MANAGER_MENUITEM, False)
		manager.add_ui(self._merge_id, '/MenuBar/ToolsMenu/ToolsOps_4',
		'arduino-settings', 'arduino-settings', gtk.UI_MANAGER_MENUITEM, False)
		manager.add_ui(self._merge_id, '/MenuBar/ToolsMenu/ToolsOps_4',
		'arduino-verificar', 'arduino-verificar', gtk.UI_MANAGER_MENUITEM, False)
		manager.add_ui(self._merge_id, '/MenuBar/ToolsMenu/ToolsOps_4',
		'arduino-enviar', 'arduino-enviar', gtk.UI_MANAGER_MENUITEM, False)	
		
		#Read the device config
		
		try:
			for line in fileinput.input('/home/'+os.getlogin()+'/.arduino/message'):			
				pass
		except:
			
			# Display the warning message
			w = gtk.MessageDialog(None,
			gtk.DIALOG_DESTROY_WITH_PARENT,
			gtk.MESSAGE_ERROR,
			gtk.BUTTONS_OK,
			'')
			
			msg = 'Devido a uma limitação do GEdit, o plugin as vezes não salva o arquivo automaticamente. '
			msg += 'Por favor, clique em salvar antes de compilar e fazer upload do código.<br> <br>'
			msg += 'ATENÇÃO: Esta versão só compila código para o AtMega328.'
			
			self._st.flash_message(0,'Plugin Arduino carregado.')
			w.set_markup('<b>Plugin Arduino carregado.</b>\n'+msg)
			w.run()			
			w.hide()
			w = None
			
			os.system('touch /home/'+os.getlogin()+'/.arduino/message')

	def compilar(self, window):

		temp_build_dir = '/tmp/arduino-gedit-'+str(time.time()*12121212)
		self.compilado_com_sucesso = False
		
		# Updating the current document
		self._st.flash_message(0,'Compilando. Por favor aguarde...')
		self._doc = self._window.get_active_document()
		self._doc.save(0)

		# Wait for GEdit saves the file.
		while self._window.get_state() != 0:
			pass										

		# Replace vars and execute the compile script
		for line in fileinput.input("/usr/lib/gedit-2/plugins/arduino/compile.sh"):

			saida = line
			saida = saida.replace("{!sketch-name}", self._doc.get_short_name_for_display().replace('.cpp',''))
			saida = saida.replace("{!sketch-path}",	self._doc.get_uri_for_display())
			saida = saida.replace("{!libs-dir}","/usr/share/gedit-2/plugins/arduino/hardware/arduino/cores/arduino/")
			saida = saida.replace("{!temp-build-dir}",temp_build_dir)
			saida = saida.replace("{!cpu-full}",'-mmcu=atmega328p -DF_CPU=16000000L -DARDUINO=21')
			saida = saida.replace("{!cpu}",'-mmcu=atmega328p')
			print saida
			os.system(saida)

		# Successfully? Hex file exists?
		try:
			# Reading log file
			error_msg = ''

			for line in fileinput.input(self._doc.get_uri_for_display()+'.log'):
				error_msg = error_msg+line+'\n'

			# Ugly, not?
			error_msg = error_msg.replace(temp_build_dir+'/'+str(self._doc.get_short_name_for_display()+':'),'Linha ')
			
			if error_msg == '':
				# No errors found			
				self._st.flash_message(0,'Compilação concluída.')
			else:
				# Display the error message
				w = gtk.MessageDialog(None,
				gtk.DIALOG_DESTROY_WITH_PARENT,
				gtk.MESSAGE_ERROR,
				gtk.BUTTONS_OK,
				'')

				self._st.flash_message(0,'Ocorreram erros ao compilar.')
				w.set_markup('<b>Ocorreram erros ao compilar.</b>\n'+error_msg)
				w.run()			
				w.hide()
				w = None

		except:
			# No errors found
			self.compilado_com_sucesso = True
			self._st.flash_message(0,'Compilação concluída')
			
			return True


	def is_configurable(self):
		return True

	def create_configure_dialog(self, window):
		
		from threading import Thread
		
		def porta(self):
			
			comando = 'zenity --entry ' + \
			'--text="Informe a porta serial ou clique em Ok para usar a padrão:" ' + \
			'--entry-text="/dev/ttyACM0" > ~/.arduino/device'
			
			os.system('mkdir -p ~/.arduino/')
			os.system(comando)
			
		
		th=Thread( target=porta, args = ( self, ) )
		th.start()
		

	def show_templates(self, window):

		f = gtk.FileChooserDialog('Selecione o arquivo',self._window,gtk.FILE_CHOOSER_ACTION_OPEN,('Abrir',1,'Cancelar',2))
		f.set_filename('/usr/share/arduino/examples/ArduinoISP/')
		r = f.run()
		f.hide()

		if r == 1:
			try:
				self._window.create_tab(True)	 
				new_doc = self._window.get_active_document()	
				template = ''

				for line in fileinput.input(f.get_filename()):			
					template = template + line 

				new_doc.set_text(template)

			except:
				st.flash_message(0,'Erro ao carregar o arquivo')
				
	def upload(self,window):
		
		#Read the device config
		
		try:
			for line in fileinput.input('/home/'+os.getlogin()+'/.arduino/device'):			
				device = line 
		except:
			self.create_configure_dialog(window)
			self.upload(window)
			return
			
		
		self.compilar(window)
			
		if self.compilado_com_sucesso == True:
			
			# Reset the board
			
			ser = serial.Serial(device)
			ser.setDTR(1)
			time.sleep(0.5)
			ser.setDTR(0)
			ser.close()
			
			
			# Uploads it.
			comando = "avrdude.real -p {!part} -P {!device} -U {!filename} -c arduino"
			comando = comando.replace('{!part}','m328p')
			comando = comando.replace('{!device}',device)
			comando = comando.replace('{!filename}',self._doc.get_uri_for_display() + '.hex')
			
			try:
				os.system(comando)
				st.flash_message(0,'Upload concluido')
				
			except:
				
				w = gtk.MessageDialog(None,
				gtk.DIALOG_DESTROY_WITH_PARENT,
				gtk.MESSAGE_ERROR,
				gtk.BUTTONS_OK,
				'')
				
				w.set_markup('Falha ao fazer upload.')
				w.run()			
				w.hide()
				w = None

	def deactivate(self, window):
		pass
