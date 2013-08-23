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

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/splitmultipart/icon.svg"),
            QCoreApplication.translate('Multipart split', u"Split Parts of Selected Features"), self.iface.mainWindow())
        self.action.setEnabled(False)
        
        # connect to signals for button behavior
        self.action.triggered.connect(self.run)
        self.iface.currentLayerChanged.connect(self.toggle)
        self.canvas.selectionChanged.connect(self.toggle)

        # Add toolbar button and menu item
        self.iface.advancedDigitizeToolBar().addAction(self.action)
        self.iface.editMenu().addAction(self.action)
    
    def toggle(self):
        layer = self.canvas.currentLayer()
        
        # Decide whether the plugin button is enable or disable
        if layer:
            # set enable
            if layer.isEditable() and layer.selectedFeatureCount() > 0:
                self.action.setEnabled(True)
                layer.editingStopped.connect(self.toggle)
                try:
                    layer.editingStarted.disconnect(self.toggle)
                except:
                    pass
            # set disable    
            else:
                self.action.setEnabled(False)
                layer.editingStarted.connect(self.toggle)
                try:
                    layer.editingStopped.disconnect(self.toggle)
                except:
                    pass

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.editMenu().removeAction(self.action)
        self.iface.advancedDigitizeToolBar().removeAction(self.action)

    # run method that performs all the real work
    def run(self):
        			
        layer = self.canvas.currentLayer()
        if layer:
            provider = layer.dataProvider()
            new_features = []
            n_of_splitted_features = 0
            n_of_new_features = 0

            layer.beginEditCommand(QCoreApplication.translate('Multipart split','Split feature(s) parts'))
            # Iterate over all selected feature to find multipart features
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
                message = QCoreApplication.translate('Multipart split', "Splited %d multipart feature(s) into %d singlepart ones.") %(n_of_splitted_features,n_of_new_features + n_of_splitted_features)
            else:
                layer.destroyEditCommand()
                message = QCoreApplication.translate('Multipart split',"No multipart features selected.")
                    
            # inform user about the end of the process and the results
            self.iface.messageBar().pushMessage("Multipart split plugin",message,0)
            
        # If no layer is selected inform the user
        else:
            message = QCoreApplication.translate('Multipart split',"Please select an editable layer")
            self.iface.messageBar().pushMessage("Multipart split",message,1)
