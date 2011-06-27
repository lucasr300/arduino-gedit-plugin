# -*- coding: utf-8 -*-

# config.py -- Config dialog
#
# Copyright (C) 2011 - Lucas R. Martins
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Parts from "Interactive Python-GTK Console" (stolen from epiphany's console.py)
#     Copyright (C), 1998 James Henstridge <james@daa.com.au>
#     Copyright (C), 2005 Adam Hooper <adamh@densi.com>
# Bits from gedit Python Console Plugin
#     Copyrignt (C), 2005 Raphaël Slinckx

import os
import gtk

class ArduinoConfigDialog(object):

    def __init__(self):
        object.__init__(self)
        self._dialog = None

    def dialog(self):
        if self._dialog is None:
            self._ui = gtk.Builder()
            self._ui.add_from_file('config.ui')
         
            self._ui.connect_signals(self)
            
            self._dialog = self._ui.get_object('dialog-config')
            self._dialog.show_all()
        else:
            self._dialog.present()
        
        return self._dialog
    
    def on_dialog_config_response(self, dialog, response_id):
        self._dialog.destroy()

    def on_dialog_config_destroy(self, dialog):
        self._dialog = None
   
        self._ui = None
   
# ex:et:ts=4:
