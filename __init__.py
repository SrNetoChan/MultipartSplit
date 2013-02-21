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
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "Multipart Split"


def description():
    return "Split selected multipart features during edit session"


def version():
    return "Version 0.2"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "1.8"

def author():
    return "Alexandre Neto"

def email():
    return "senhor.neto@gmail.com"

#def category():
#  return "Vector"

def classFactory(iface):
    # load SplitMultipart class from file SplitMultipart
    from splitmultipart import SplitMultipart
    return SplitMultipart(iface)
