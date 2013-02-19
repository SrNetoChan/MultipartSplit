# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SplitMultipartDialog
                                 A QGIS plugin
 Split selected multipart features during edit session
                             -------------------
        begin                : 2013-01-17
        copyright            : (C) 2013 by Alexandre Neto
        email                : senhor.neto@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from ui_splitmultipart import Ui_SplitMultipart
# create the dialog for zoom to point


class SplitMultipartDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_SplitMultipart()
        self.ui.setupUi(self)
