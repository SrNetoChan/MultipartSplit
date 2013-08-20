# -*- coding: utf-8 -*-
"""
/***************************************************************************
MultipartSplit
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
# Import the PyQt and QGIS libraries
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
# from splitmultipartdialog import SplitMultipartDialog


class SplitMultipart:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/splitmultipart"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale", type=str)[0:2]

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/splitmultipart_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        # self.dlg = SplitMultipartDialog() APAGAR!?

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/splitmultipart/icon.svg"),
            u"Split Selected Multipart features", self.iface.mainWindow())
        self.action.setEnabled(False)
        
        # connect to signals for button behavior
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        QObject.connect(self.iface, SIGNAL("currentLayerChanged(QgsMapLayer*)"), self.toggle)

        # Add toolbar button and menu item
        self.iface.advancedDigitizeToolBar().addAction(self.action)
        self.iface.editMenu().addAction(self.action)
    
    def toggle(self):
        mc = self.canvas
        layer = mc.currentLayer()
        
        # Decide whether the plugin button is enable or disable
        if layer <> None:
            if layer.isEditable(): #AND layer.selectedFeatureCount() != 0:
                self.action.setEnabled(True)
                QObject.connect(layer,SIGNAL("editingStopped()"),self.toggle)
                QObject.disconnect(layer,SIGNAL("editingStarted()"),self.toggle)
                # set enable
            else:
                self.action.setEnabled(False)
                QObject.connect(layer,SIGNAL("editingStarted()"),self.toggle)
                QObject.disconnect(layer,SIGNAL("editingStopped()"),self.toggle)
                # set disable

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.editMenu().removeAction(self.action)
        self.iface.advancedDigitizeToolBar().removeAction(self.action)

    # run method that performs all the real work
    def run(self):
        			
        layer = self.iface.mapCanvas().currentLayer()
        if not layer.isEditable():
            # If no editable layer is selected, throw a message and return
            self.iface.messageBar().pushMessage(QCoreApplication.translate('Multipart split plugin',"Multipart split plugin"), \
               QCoreApplication.translate('Multipart split plugin','Please select an editable vector layer'),2)
            return None
        else:
            provider = layer.dataProvider()
            new_features = []
            n_of_splitted_features = 0
            n_of_new_features = 0

            layer.beginEditCommand("Split features")
            for feature in layer.selectedFeatures():
                geom = feature.geometry()
                # if feature geometry is multipart starts split processing
                if geom != None:
                    if geom.isMultipart():
                        n_of_splitted_features += 1
                        temp_feature = QgsFeature()
                        
                        # Get attributes from original feature
                        new_attributes = feature.attributes()
                        for j in range(new_attributes.__len__()):
                            if provider.defaultValue(j) != None:
                                new_attributes[j] = provider.defaultValue(j)
                        temp_feature.setAttributes(new_attributes)
                            
                        # Get parts geometries from original feature
                        parts = geom.asGeometryCollection ()
                                
                        # from 2nd to last part create a new features using their
                        # single geometry and the attributes of the original feature
                        
                        for i in range(1,len(parts)):
                            temp_feature.setGeometry(parts[i])
                            new_features.append(QgsFeature(temp_feature))
                        # update feature geometry to hold first part single geometry
                        # (this way one of the output feature keeps the original Id)
                        feature.setGeometry(parts[0])
                        layer.updateFeature(feature)

            # add new features to layer
            n_of_new_features = len(new_features)
            if n_of_new_features > 0:
                layer.addFeatures(new_features, False)
                layer.endEditCommand()
                message = "Splited " + str(n_of_splitted_features) + " multipart feature(s) into " + \
                str(n_of_new_features + n_of_splitted_features) + " singlepart ones."
            else:
                layer.destroyEditCommand()
                message = "No multipart features selected."
            
            # inform user about the end of the process and the results
            
            # self.iface.mainWindow().statusBar().showMessage(message)
            self.iface.messageBar().pushMessage("Multipart split plugin",message,0,10)
