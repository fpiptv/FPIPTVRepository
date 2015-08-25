#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 by lihattv.com
import urllib
import urllib2
import socket
import sys
import re
import os
import xbmcplugin
import xbmcgui
import xbmcaddon

pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
viewfanart = addon.getSetting("fanart") == "true"
showlogo = addon.getSetting("logo") == "true"
server = str(addon.getSetting("server"))
quality = str(addon.getSetting("quality"))
urlMain = "http://lihattv.us/?q=Gotham"
logo = xbmc.translatePath('special://home/addons/'+addonID+'/icon.png')
xbmcplugin.setContent(pluginhandle, 'movies')
getLang = addon.getLocalizedString

def index():
    addDir(getLang(40001), urlMain, 'channel', logo)
    addDir(getLang(40101), "", "search", logo)
    xbmcplugin.endOfDirectory(pluginhandle)
	
def channel(path):
    content = _url(path)
    root = re.compile('.+?dir="(.+?)".+?channel="(.+?)".+?img="(.+?)"').findall(content)
    for url, title, thumb in root:
        addDir(title, url, "channel", thumb, "Category")
    link = re.compile('.+?url="(.+?)".+?title="(.+?)".+?img="(.+?)"').findall(content)
    for url, title, thumb in link:
        addLink(title, url, "player", thumb, title+" TV Channel")
    xbmcplugin.endOfDirectory(pluginhandle)

def player(url):
    content = _url(url+"&q="+quality)
    match = re.compile('stream="(.+?)"', re.DOTALL).findall(content)
    listitem = xbmcgui.ListItem(path=match[0])
    xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def _url(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = response.read()
    response.close()
    return content

def _params(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

def addLink(name, url, mode, iconimage, desc="", year="2014"):
    if (iconimage==' ') or (not showlogo):
        iconimage=logo
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    list = xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    list.setInfo(type="Video", infoLabels={"Title": name, "Genre": "Live TV", "Plot": desc, "director": "LihatTV", "writer": "LihatTV", "Year": year})
    list.setProperty('IsPlayable', 'true')
    if viewfanart:
        list.setProperty("fanart_image", iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=list)
    return ok

def addDir(name, url, mode, iconimage, type="", desc="", year="2014"):
    if (iconimage==' ') or (not showlogo):
        iconimage=logo
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)+"&channelThumb="+urllib.quote_plus(iconimage)
    list = xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    list.setInfo(type="Video", infoLabels={"Title": name, "Genre": "Live TV", "Year": year})
    if viewfanart:
        list.setProperty("fanart_image", iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=list, isFolder=True)
    return ok

def search():
    keyboard = xbmc.Keyboard('', getLang(40101))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        query = keyboard.getText().replace(" ", "+")
        channel(urlMain+"&s="+query)

params = _params(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
type = urllib.unquote_plus(params.get('type', ''))

if mode == 'player':
    player(url)
elif mode == 'channel':
    channel(url)
elif mode == 'search':
    search()
else:
    index()
