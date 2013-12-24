#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, urllib2, cookielib
import string, os, re, time, datetime
from posixpath import basename, dirname
from urlparse import urlparse

import xbmc, xbmcgui, xbmcplugin, xbmcaddon

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import demjson
import glob
import unicodedata 

pluginhandle = int(sys.argv[1])

addon = xbmcaddon.Addon('plugin.video.reddit.bc')
pluginpath = addon.getAddonInfo('path')

BASE = 'http://www.reddit.com/r'
COOKIEFILE = os.path.join(pluginpath,'resources','reddit-cookies.lwp')

confluence_views = [500,501,502,503,504,508]

# Root listing
def listCategories():
    addDir("Videos - Whats Hot",              BASE+'/videos/hot.json',                  'listVideos', '')
    addDir("Videos - New",                    BASE+'/videos/new.json',                  'listVideos', '')
    addDir("Videos - Controversial",          BASE+'/videos/controversial.json',        'listVideos', '')
    addDir("Videos - Top",                    BASE+'/videos/top.json',                  'listVideos', '')
    addDir("Music - Hot",                     BASE+'/music/hot.json',                   'listVideos', '')    
    addDir("Music Videos - Hot",              BASE+'/MusicVideos/hot.json',             'listVideos', '')
    addDir("Listen To This - Hot",            BASE+'/listentothis/hot.json',            'listVideos', '')
    addDir("K-Pop - Hot",                     BASE+'/kpop/hot.json',                    'listVideos', '')
    addDir("Documentary - Hot",               BASE+'/documentary/hot.json',             'listVideos', '')
    addDir("Documentaries - Hot",             BASE+'/documentaries/hot.json',           'listVideos', '')
    addDir("Climbing Vids - Hot",             BASE+'/climbingvids/hot.json',            'listVideos', '')
    addDir("Artisan - Hot",                   BASE+'/artisan/hot.json',                 'listVideos', '')
    addDir("Artisan Videos - Hot",            BASE+'/ArtisanVideos/hot.json',           'listVideos', '')
    addDir("Obscure Media - Hot",             BASE+'/ObscureMedia/hot.json',            'listVideos', '')
    addDir("Conspiracy Documentary - Hot",    BASE+'/conspiracydocumentary/hot.json',   'listVideos', '')
    addDir("Rocket Launches - Hot",           BASE+'/rocketlaunches/hot.json',          'listVideos', '')
    addDir("Science Videos - Hot",            BASE+'/sciencevideos/hot.json',           'listVideos', '')
    addDir("Car Crash - Hot",                 BASE+'/carcrash/hot.json',                'listVideos', '')
    addDir("Derailed - Hot",                  BASE+'/Derailed/.json',                   'listVideos', '')
    addDir("Police Chases - Hot",             BASE+'/PoliceChases/hot.json',            'listVideos', '')
    addDir("Cringe - Hot",                    BASE+'/cringe/hot.json',                  'listVideos', '')
    xbmcplugin.endOfDirectory(pluginhandle)
    
def listVideos(url=False, updateListing=False):
    if not url:
        url = params["url"]
    data = getURL(url)
    videodata = demjson.decode(data)['data']
    after = videodata['after']
    before = videodata['before']
    videos = videodata['children']
    print before
    print after
    if before and before is not None:
        addDir('(Previous Page)', url.split('?')[0]+'?count=25&before='+before, 'listUpdate', '')
    if after:
        addDir('(Next Page)', url.split('?')[0]+'?count=25&after='+after, 'listUpdate', '')
    for video in videos:
        if video['data']['domain'] == 'youtube.com':
            postTitle = video['data']['title'].replace('/n','')
            url = video['data']['url']
            try:thumbnail = video['data']['media']['oembed']['thumbnail_url']
            except:thumbnail = ''
            try: videoTitle = video['data']['media']['oembed']['title']
            except: videoTitle = ''
            try: videoTitle = video['data']['media']['oembed']['title']
            except: videoTitle = ''
            try: plot = video['data']['media']['oembed']['description']
            except: plot = ''
            infoLabels={"Title": postTitle,
                        'plot': plot}
            try:
                youtubeID = url.split('v=')[1].split('&')[0]
                youtubeurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubeID
                addLink(postTitle, videoTitle, youtubeurl, mode, thumbnail, infoLabels=infoLabels)
            except:
                print url
        elif video['data']['domain'] == 'youtu.be':
            postTitle = video['data']['title'].replace('/n','')
            url = video['data']['url']
            try:thumbnail = video['data']['media']['oembed']['thumbnail_url']
            except:thumbnail = ''
            try: videoTitle = video['data']['media']['oembed']['title']
            except: videoTitle = ''
            try: videoTitle = video['data']['media']['oembed']['title']
            except: videoTitle = ''
            try: plot = video['data']['media']['oembed']['description']
            except: plot = ''
            infoLabels={"Title": postTitle,
                        'plot': plot}
            try:
                youtubeID = urlparse(url)
                youtubeurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % basename(youtubeID.path)
                addLink(postTitle, videoTitle, youtubeurl, mode, thumbnail, infoLabels=infoLabels)
            except:
                print url
        elif video['data']['domain'] == 'liveleak.com':
            postTitle = video['data']['title'].replace('/n','')
            url = video['data']['url']
            try:thumbnail = video['data']['media']['oembed']['thumbnail_url']
            except:thumbnail = ''
            try: videoTitle = video['data']['media']['oembed']['title']
            except: videoTitle = ''
            try: videoTitle = video['data']['media']['oembed']['title']
            except: videoTitle = ''
            try: plot = video['data']['media']['oembed']['description']
            except: plot = ''
            infoLabels={"Title": postTitle,
                        'plot': plot}
            try: 
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('file: "(.+?)",').findall(link)
                for url in match:
                         addLink(postTitle, videoTitle, url, mode, thumbnail, infoLabels=infoLabels)
                match=re.compile('src="http://www.youtube.com/embed/(.+?)?rel=0').findall(link)
                for url in match:
                  youtubeurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
                  addLink(postTitle, videoTitle, youtubeurl, mode, thumbnail, infoLabels=infoLabels)
            except:
                print url
    xbmcplugin.setContent(pluginhandle, 'episodes')
    xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
    xbmcplugin.endOfDirectory(pluginhandle,updateListing=updateListing)

def listUpdate():
    listVideos(params["url"],updateListing=True)
 
# Common
def addLink(postTitle, videoTitle, url, mode, iconimage, fanart=False, infoLabels=False):
    ok = True
    liz = xbmcgui.ListItem(postTitle, videoTitle, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setProperty('IsPlayable', 'true')
    if infoLabels:
        liz.setInfo(type="Video", infoLabels=infoLabels)
    if fanart:
        liz.setProperty('fanart_image',fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
    return ok


def addDir(name, url, mode, iconimage, fanart=False, infoLabels=False):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    if infoLabels:
        liz.setInfo(type="Video", infoLabels=infoLabels)
    if fanart:
        liz.setProperty('fanart_image',fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

def getURL( url , extraheader=True):
    print 'REDDIT VIDEO --> common :: getURL :: url = '+url
    cj = cookielib.LWPCookieJar()
    if os.path.isfile(COOKIEFILE):
        cj.load(COOKIEFILE, ignore_discard=True)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('Referer', 'http://www.vevo.com'),
                         ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]
    if extraheader:
        opener.addheaders = [('X-Requested-With', 'XMLHttpRequest')]
    usock=opener.open(url)
    response=usock.read()
    usock.close()
    if os.path.isfile(COOKIEFILE):
        cj.save(COOKIEFILE, ignore_discard=True)
    return response

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=urllib.unquote_plus(splitparams[1])                                        
    return param

params=get_params()
try:
    mode=params["mode"]
except:
    mode=None
print "Mode: "+str(mode)
print "Parameters: "+str(params)

if mode==None:
    listCategories()
else:
    exec '%s()' % mode