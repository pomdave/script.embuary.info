#!/usr/bin/python
# coding: utf-8

########################
import os
import xbmc
import xbmcaddon
import xml.etree.ElementTree as ET
import xbmcvfs
from xml.dom import minidom

########################
from resources.lib.helper import *
########################

def fave(params):

    # Define the favorite item
    FAV_CALL = remove_quotes(params.get('fcall', ''))
    FAV_THUMB = params.get('fthumb', '')
    FAV_NAME = remove_quotes(params.get('fname', ''))
    FAV_ID = remove_quotes(params.get('fid', ''))
    
    if FAV_CALL == 'tv':
            FAV_ACTION = "ActivateWindow(10025,plugin://plugin.video.fenlight/?mode=build_season_list&tmdb_id=" + FAV_ID + ",return)"
    elif FAV_CALL == 'movie':
            FAV_ACTION = "ActivateWindow(10025,plugin://plugin.video.fenlight/?mode=playback.media&media_type=movie&tmdb_id=" + FAV_ID + ",return)"
    #log('Fave: params ' + str(FAV_CALL) + str(FAV_THUMB) + str(FAV_NAME) + str(FAV_ID),force=True)
    #log('Fave: params ' + str(FAV_ACTION),force=True)
    # Get Kodi user data path
    #addon_data_path = xbmc.translatePath('special://userdata')
    #favourites_path = os.path.join(addon_data_path, 'favourites.xml')
    #userdata_path = xbmcvfs.translatePath("special://profile/")
    #favourites_path = os.path.join(userdata_path, "favourites.xml")
    
    # uncomment for default favorites path
    #favourites_path = xbmcvfs.translatePath('special://profile/favourites.xml')
    # uncomment/edit for substituted favorites path
    favourites_path = r"\\192.168.1.2\Kodi\Shared\userdata\favourites.xml"
    #log('Fave: path ' + favourites_path,force=True)

    # Create root if file doesn't exist
    if not os.path.exists(favourites_path):
        root = ET.Element("favourites")
        tree = ET.ElementTree(root)
    else:
        tree = ET.parse(favourites_path)
        root = tree.getroot()

    # Check if already exists
    exists = any(fav.get("name") == FAV_NAME for fav in root.findall("favourite"))

    if not exists:
        fav = ET.SubElement(root, "favourite", name=FAV_NAME, thumb=FAV_THUMB)
        fav.text = FAV_ACTION
        #prettify
        indent(root)
        #write
        tree.write(favourites_path, encoding="utf-8", xml_declaration=True)
        xbmc.executebuiltin('Notification(Favorites, Added successfully, 3000)')
    else:
        xbmc.executebuiltin('Notification(Favorites, Already exists, 3000)')

    return  

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            