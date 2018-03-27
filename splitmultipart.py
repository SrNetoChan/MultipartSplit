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
from __future__ import absolute_import
from builtins import range
from builtins import object
from qgis.core import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
import os.path

# Initialize Qt resources from file resources.py
#from . import resources_rc

class SplitMultipart(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale", type=str)[0:2]
        
        if QFileInfo(self.plugin_dir).exists():
            localePath = os.path.join(self.plugin_dir,
                                      "i18n",
                                      "splitmultipart_{}.qm".format(locale))

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(os.path.join(self.plugin_dir, "icon.svg")),
            self.tr(u"Split Feature(s) Parts"),
            self.iface.mainWindow())
        self.action.setEnabled(False)
        
        # connect to signals for button behavior
        self.action.triggered.connect(self.run)
        self.iface.currentLayerChanged["QgsMapLayer *"].connect(self.toggle)
        self.canvas.selectionChanged.connect(self.toggle)

        # Add toolbar button and menu item
        self.iface.advancedDigitizeToolBar().addAction(self.action)
        self.iface.editMenu().addAction(self.action)
    
    # function to activate or deactivate the plugin buttons
    def toggle(self):
        # get current active layer 
        layer = self.canvas.currentLayer()
        
        if layer and layer.type() == layer.VectorLayer:
            # disconnect all previously connect signals in current layer
            try:
                layer.editingStarted.disconnect(self.toggle)
            except:
                pass
            try:
                layer.editingStopped.disconnect(self.toggle)
            except:
                pass
            
            # check if current layer is editable and has selected features
            # and decide whether the plugin button should be enable or disable
            if layer.isEditable():
                if layer.selectedFeatureCount() > 0:
                    self.action.setEnabled(True)
                else:
                    self.action.setEnabled(False)
                layer.editingStopped.connect(self.toggle)
            # layer is not editable    
            else:
                self.action.setEnabled(False)
                layer.editingStarted.connect(self.toggle)
        else:
            self.action.setEnabled(False)
    
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.editMenu().removeAction(self.action)
        self.iface.advancedDigitizeToolBar().removeAction(self.action)

    # run method that performs all the real work
    def run(self):
        layer = self.canvas.currentLayer()
        provider = layer.dataProvider()
        n_of_splitted_features = 0
        n_of_new_features = 0

        layer.beginEditCommand(QCoreApplication.translate('Multipart split','Split feature(s) parts'))
        # Iterate over all selected feature to find multipart features
        for feature in layer.selectedFeatures():
            geom = feature.geometry()
            # if feature geometry is multipart starts split processing
            if geom != None:
                if geom.isMultipart():
                    new_features = []
                    n_of_splitted_features += 1
                    temp_feature = QgsFeature()
                    # Get attributes from original feature
                    new_attributes = feature.attributes()
                    
                    # When attribute is a Primary Key, replace by default value
                    ### This is not working well with spatialite provider###
                    for j in provider.pkAttributeIndexes():
                        if provider.defaultValue(j):
                            new_attributes[j] = provider.defaultValue(j)
                        else:
                            new_attributes[j] = QPyNullVariant(int)
                            
                    temp_feature.setAttributes(new_attributes)
                        
                    # Get parts geometries from original feature
                    parts = geom.asGeometryCollection ()
                            
                    # from 2nd to last part create a new features using their
                    # single geometry and the attributes of the original feature
                    
                    # Convert part to multiType to prevent errors in Spatialite
                    for part in parts:
                        part.convertToMultiType()
                   
                    for i in range(1,len(parts)):
                        n_of_new_features += 1
                        temp_feature.setGeometry(parts[i])
                        temp_feature.geometry().convertToMultiType()
                        new_features.append(QgsFeature(temp_feature))
                    # update feature geometry to hold first part single geometry
                    # (this way one of the output features keeps the original Id)
                    feature.setGeometry(parts[0])
                    layer.updateFeature(feature)
                    layer.addFeatures(new_features)

        # End process and inform user about the results
        if n_of_new_features > 0:
            layer.endEditCommand()
            message = QCoreApplication.translate('Multipart split', "Splited %d multipart feature(s) into %d singlepart ones.") %(n_of_splitted_features,n_of_new_features + n_of_splitted_features)
        else:
            layer.destroyEditCommand()
            message = QCoreApplication.translate('Multipart split',"No multipart features selected.")

        self.iface.messageBar().pushMessage("Multipart split plugin",message,0,10)


    def tr(self, text):
        return QCoreApplication.translate("Multipart split", text)