# -*- coding: utf-8 -*-
'''
Copyright (C) 2017                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 3 of the License, or      
(at your option) any later version.                                    

This program is distributed in the hope that it will be useful,        
but WITHOUT ANY WARRANTY; without even the implied warranty of         
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
GNU General Public License for more details.                           

You should have received a copy of the GNU General Public License      
along with this program. If not, see <http://www.gnu.org/licenses/>  
'''

import urllib
import urllib2
import re
import os
import sys
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon

mysettings = xbmcaddon.Addon(id='plugin.video.adulthideout')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home,
                                        'logos\\'))
homemenu = xbmc.translatePath(os.path.join(home, 'resources', 'playlists'))

# Define Webpages
hentaigasm = 'http://hentaigasm.com/'


def menulist():
    try:
        mainmenu = open(homemenu, 'r')
        content = mainmenu.read()
        mainmenu.close()
        match = re.compile('#.+,(.+?)\n(.+?)\n').findall(content)
        return match
    except:
        pass


def make_request(url):
    try:
        req = urllib2.Request(url)
        if yespornplease in url:
            req.add_header(
                'User-Agent',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/23.0.1271.64 Safari/537.11'
            )
        else:
            req.add_header(
                'User-Agent',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
            )
        response = urllib2.urlopen(req, timeout=60)
        link = response.read()
        response.close()
        return link
    except urllib2.URLError as e:
        print('We failed to open "%s".') % url
        if hasattr(e, 'code'):
            print('We failed with error code - %s.') % e.code
        elif hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)


def home():
    add_dir('... [COLOR red]  Home  [/COLOR]...', '', None, icon, fanart)


# define main directory and starting page
def main():
    add_dir('Hentaigasm [COLOR green] Videos[/COLOR]', hentaigasm, 2,
            logos + 'hentaigasm.png', fanart)


# Search
def search():
    try:
        keyb = xbmc.Keyboard('', '[COLOR blue]Enter search text[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText())
        if 'hentaigasm' in name:
            url = hentaigasm + '/?s=' + searchText
            start(url)
    except:
        pass


def start(url):
    home()
    if 'hentaigasm' in url:
        add_dir('[COLOR lime]hentaigasm     [COLOR red]Search[/COLOR]',
                hentaigasm, 1, logos + 'hentaigasm.png', fanart)
        add_dir('[COLOR lime]Categories[/COLOR]', hentaigasm, 29,
                logos + 'hentaigasm.png', fanart)
        content = make_request(url)
        match = re.compile(
            'title="(.+?)" href="(.+?)">\s*\s*.+?\s*\s*.+?<img src="(.+?)"'
        ).findall(content)
        for name, url, thumb in match:
            thumb = thumb.replace(' ', '%20')
            if "Raw" in name:
                add_link('[COLOR lime] [Raw] [/COLOR]' + name, url, 4, thumb,
                         fanart)
            else:
                add_link('[COLOR yellow] [Subbed] [/COLOR]' + name, url, 4,
                         thumb, fanart)
        try:
            match = re.compile("<a href='([^']*)' class=\"next\">»").findall(
                content)
            add_dir('[COLOR blue]Next  Page  >>>>[/COLOR]', match[0], 2,
                    logos + 'hentaigasm.png', fanart)
        except:
            pass


def hentaigasm_categories(url):
    home()
    content = make_request(url)
    match = re.compile("<a href='http://hentaigasm.com/tag/([^']+)'").findall(
        content)
    for url in match:
        name = url.replace('http://hentaigasm.com/tag/', '').replace('/', '')
        add_dir(name, 'http://hentaigasm.com/tag/' + url, 2,
                logos + 'hentaigasm.png', fanart)



def resolve_url(url):
    content = make_request(url)
    if 'hentaigasm' in url:
        media_url = re.compile('file: "(.+?)",').findall(content)[0]
    else:
        media_url = url
    item = xbmcgui.ListItem(name, path=media_url)
    item.setMimeType('video/mp4')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    return


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


def add_dir(name, url, mode, iconimage, fanart):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(
        mode) + "&name=" + urllib.quote_plus(
            name) + "&iconimage=" + urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(
        name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "overlay": "6"})
    liz.setProperty('fanart_image', fanart)
    ok = xbmcplugin.addDirectoryItem(
        handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def add_link(name, url, mode, iconimage, fanart):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(
        mode) + "&name=" + urllib.quote_plus(
            name) + "&iconimage=" + urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(
        name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', fanart)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    try:
        liz.setContentLookup(False)
    except:
        pass
    liz.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(
        handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok


params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    iconimage = urllib.unquote_plus(params["iconimage"])
except:
    pass

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "iconimage: " + str(iconimage)

if mode == None or url == None or len(url) < 1:
    main()

elif mode == 1:
    search()

elif mode == 2:
    start(url)

elif mode == 3:
    media_list(url)

elif mode == 4:
    resolve_url(url)

elif mode == 29:
    hentaigasm_categories(url)

elif mode == 70:
    item = xbmcgui.ListItem(name, path=url)
    item.setMimeType('video/mp4')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
