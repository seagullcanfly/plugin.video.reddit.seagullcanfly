#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, urllib2, cookielib
import string, os, re, time, datetime
from posixpath import basename, dirname
from urlparse import urlparse

import xbmc, xbmcgui, xbmcplugin, xbmcaddon

import demjson
import glob
import unicodedata 

pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon('plugin.video.reddit.bc')
pluginpath = addon.getAddonInfo('path')     
BASE = 'http://www.reddit.com/r'
COOKIEFILE = os.path.join(pluginpath,'resources','reddit-cookies.lwp')

confluence_views = [500,501,502,503,504,508]

def listCategories():
    
    #Videos
    addDir("Videos - Whats Hot", BASE+'/videos/hot.json', 'listVideos', '')
    addDir("Videos - New", BASE+'/videos/new.json', 'listVideos', '')
    addDir("Videos - Controversial", BASE+'/videos/controversial.json', 'listVideos', '')
    addDir("Videos - Top", BASE+'/videos/top.json', 'listVideos', '')
    
    #Custom Subreddits (these can be added in settings)
    subreddits = addon.getSetting("subreddits")
    if subreddits.lower() != "default":
        subreddits = subreddits.split(',')
        for subreddit in sorted(subreddits):
            subreddit = subreddit.strip()
            addDir(subreddit.title()+" - What's Hot", BASE+'/'+subreddit+'.json', 'listVideos', '')
    
    # Default Subreddits (these can be selected in settings)
    default_subreddits = ['kpop,', 'music', 'musicvideos', 'listentothis', 'documentary', 'documentaries',
                          'climbingvids', 'artisan', 'artisanvideos', 'obscuremedia', 'conspiracydocumentary',
                          'rocketlaunches', 'sciencevideos', 'carcrash', 'derailed', 'policechases', 'cringe']
    for subreddit in sorted(default_subreddits):
        if addon.getSetting(subreddit) == "true":
            addDir(subreddit.title() + " - What's Hot", BASE + '/' + subreddit + '.json', 'listVideos', '')
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
    if before:
        addDir('(Previous Page)', url.split('?')[0]+'?count=25&before='+before, 'listUpdate', '')
    if after:
        addDir('(Next Page)', url.split('?')[0]+'?count=25&after='+after, 'listUpdate', '')
    for video in videos:
        permalink = video['data'].get('permalink')
        if permalink:
            comment_page = "http://www.reddit.com" + permalink + '.json'
        else:
            comment_page = False
        if video['data']['domain'] == 'youtube.com':
            postTitle = video['data']['title'].replace('/n','')
            postTitle = postTitle.replace("&amp;", "&")
            url = video['data']['url']
            try:
                thumbnail = video['data']['media']['oembed']['thumbnail_url']
            except:
                thumbnail = ''
            try:
                videoTitle = video['data']['media']['oembed']['title']
            except:
                videoTitle = ''
            try:
                videoTitle = video['data']['media']['oembed']['title']
            except:
                videoTitle = ''
            try:
                plot = video['data']['media']['oembed']['description']
            except:
                plot = ''
                infoLabels={"Title": postTitle, 'plot': plot.replace("&amp;","&")}
            try:
                youtubeID = url.split('v=')[1].split('&')[0]
                youtubeurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubeID
                addLink(postTitle, videoTitle, youtubeurl, mode, thumbnail,
                        infoLabels=infoLabels, comment_page = comment_page)
            except:
                print url + 'did not work'
        elif video['data']['domain'] == 'youtu.be':
            postTitle = video['data']['title'].replace('/n','')
            url = video['data']['url']
            try:
                thumbnail = video['data']['media']['oembed']['thumbnail_url']
            except:
                thumbnail = ''
            try:
                videoTitle = video['data']['media']['oembed']['title']
            except:
                videoTitle = ''
            try:
                videoTitle = video['data']['media']['oembed']['title']
            except:
                videoTitle = ''
            try:
                plot = video['data']['media']['oembed']['description']
            except:
                plot = ''
                infoLabels={"Title": postTitle, 'plot': plot}
            try:
                youtubeID = urlparse(url)
                youtubeurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % basename(youtubeID.path)
                addLink(postTitle, videoTitle, youtubeurl, mode, thumbnail,
                        infoLabels=infoLabels, comment_page = comment_page)
            except:
                print url
        elif video['data']['domain'] == 'liveleak.com':
            postTitle = video['data']['title'].replace('/n','')
            url = video['data']['url']
            try:
                thumbnail = video['data']['media']['oembed']['thumbnail_url']
            except:
                thumbnail = ''
            try:
                videoTitle = video['data']['media']['oembed']['title']
            except:
                videoTitle = ''
            try:
                videoTitle = video['data']['media']['oembed']['title']
            except:
                videoTitle = ''
            try:
                plot = video['data']['media']['oembed']['description']
            except:
                plot = ''
                infoLabels={"Title": postTitle, 'plot': plot}
            try:
                req = urllib2.Request(url)
                req.add_header('User-Agent',
                               'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('file: "(.+?)",').findall(link)
                for url in match:
                     addLink(postTitle, videoTitle, url, mode, thumbnail, infoLabels=infoLabels)
                match=re.compile('src="http://www.youtube.com/embed/(.+?)?rel=0').findall(link)
                for url in match:
                    youtubeurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
                    addLink(postTitle, videoTitle, youtubeurl, mode, thumbnail,
                            infoLabels=infoLabels, comment_page = comment_page)
            except:
                print url
    xbmcplugin.setContent(pluginhandle, 'episodes')
    #xbmc.executebuiltin("Container.SetViewMode("+str(confluence_views[3])+")")
    ### I think this might be where it was switching back to the view I don't like.
    xbmcplugin.endOfDirectory(pluginhandle, updateListing=updateListing)

def listUpdate():
    listVideos(params["url"], updateListing=True)
 
# Common
def addLink(postTitle, videoTitle, url, mode, iconimage, fanart=False, infoLabels=False, comment_page = False):
    if comment_page:
        comment_data = getURL(comment_page)
        comment_stuff = demjson.decode(comment_data)[1]['data']
        comments = comment_stuff['children']
        comment_body_list = []
        for comment in comments[0:10]:
            comment_body = comment['data'].get('body')
            if comment_body:
                try:
                    comment_body_list.append(comment_body.strip())
                except:
                    print "Most likely a unicode error."
    ok = True
    liz = xbmcgui.ListItem(postTitle, videoTitle,
                           iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setProperty('IsPlayable', 'true')
    if infoLabels:
        liz.setInfo(type="Video", infoLabels=infoLabels)
        if comment_body_list:
            tuple_list = []
        for comment in comment_body_list[0:9]:
            comment_tuple = (comment, 'XBMC.Notification(!,' + comment +')')
            tuple_list.append(comment_tuple)
            liz.addContextMenuItems(tuple_list)
    if fanart:
        liz.setProperty('fanart_image', fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
    return ok


def addDir(name, url, mode, iconimage, fanart=False, infoLabels=False):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    if infoLabels:
        liz.setInfo(type="Video", infoLabels=infoLabels)
    if fanart:
        liz.setProperty('fanart_image', fanart)
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
