# -*- coding: utf-8 -*-

# Importing libraries
import urllib, urllib2, re, sys, os
import xbmcplugin, xbmcgui
from urllib import urlencode

# Parameters function
def getParams():

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
				param[splitparams[0]]=splitparams[1]
                            
	return param

# Link function
def addLink(title, url, image):

	item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage=image)
	item.setInfo( type='Video', infoLabels={'Title': title} )
	
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=item)
	
# Dir function
def addDir(title, url, mode, image ):

	sys_url = sys.argv[0] + '?title=' + urllib.quote_plus(title) + '&url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode)) + '&image=' + urllib.quote_plus(image)

	item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage=image)
	item.setInfo( type='Video', infoLabels={'Title': title} )

	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys_url, listitem=item, isFolder=True)


# HTML function
def getHTML(url):

	headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3', 'Content-Type':'application/x-www-form-urlencoded'}
	conn = urllib2.urlopen(urllib2.Request(url, urlencode({}), headers))
	html = conn.read()
	conn.close()
    
	return html

# Categories function
def categories():
	
	for league in highlights:	
		addDir(league, highlights[league], 20, image='')

# Matches function		
def matches(url, title):
	
	if title == 'All Matches':
		category = url.split()
		league = ''
		for index in category:
			league += getHTML(index)	
	else:
		league = getHTML(url)

	matches = re.compile('<div class="(?:.+?)"><a href="(.+?)"(?:.+?)title="(.+?) &#8211; Highlights(?:.+?)src="(.+?)"(?:.+)>').findall(league.decode('UTF-8'))

	for match, title, image in matches:
		addDir(title, match, 30, image)
	
def videos(url, title, image):		
	
	match = getHTML(url)
	video_id = re.compile('<script data-config="(?:.+?)21772/videos/v2/(.+?)/(?:.+?).json"(?:.+)>').findall(match.decode('UTF-8'))
	video = 'http://cdn.phoenix.intergi.com/21772/videos/' + video_id[0] + '/video-sd.mp4?hosting_id=21772'

	addLink(title, video, image)

params = getParams()
url    = None
title  = None
mode   = None
image = None

highlights = {		'England': 'http://www.fullmatchesandshows.com/premier-league/',
					'Spain': 'http://www.fullmatchesandshows.com/la-liga/',
					'Germany': 'http://www.fullmatchesandshows.com/bundesliga/',
					'Italy': 'http://www.fullmatchesandshows.com/category/serie-a/',  
					'Champions League': 'http://www.fullmatchesandshows.com/champions-league/'	}

highlights['All Matches'] = "%s %s %s %s %s"  % (	highlights['England'], highlights['Spain'], highlights['Germany'],
												highlights['Italy'], highlights['Champions League'])
						
try:    title = urllib.unquote_plus(params['title'])
except: pass

try:    url = urllib.unquote_plus(params['url'])
except: pass

try:    mode = int(params['mode'])
except: pass

try:    image = urllib.unquote_plus(params['image'])
except: pass

if mode == None:
    categories()

elif mode == 20:
	matches(url, title)
	
elif mode == 30:
	videos(url, title, image)

xbmcplugin.endOfDirectory(int(sys.argv[1]))