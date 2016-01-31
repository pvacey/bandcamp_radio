#!/usr/bin/python
import re,json,os,sys
import time
import random
import requests

if (len(sys.argv) < 2):
    print 'a simple command line bandcamp radio - https://github.com/pvacey/bandcamp_radio'
    print 'usage: \n    '+sys.argv[0]+' <tag>'
    print 'example: \n    '+sys.argv[0]+' ambient'
    exit()

def get_album_links(tag):
    print '***Retrieving Album Data***'
    albums =[]
    for i in range(1,11):
        #for i in range(1,2): # only do 1 page for testing purposes
        url = 'https://bandcamp.com/tag/'+tag+'?page='+str(i)
        tagpage = requests.get(url).text
        tmp = re.findall('href="(.+?)"\s+title',tagpage)
        if len(tmp) == 0:
            print '[ERROR] tag "%s" is not valid' % tag
            exit()
        for a in tmp:
            albums.append(a)
    return albums

def play_random_song(the_url):
    #grab the html of the album page
    html = requests.get(the_url).text
    #grab album title
    tmp = re.findall('current:\s({.+(?=},)}),',html)
    albumdetails = json.loads(tmp[0])
    title = albumdetails['title']
    #grab artist name, this does not use json because of bad formatting on the page
    tmp = re.findall('artist: "([^"]+)"',html)
    artist = tmp[0]
    # grab the array of tracks
    tmp = re.findall('trackinfo\s*:\s*(\[.*}])', html)
    trackinfo = json.loads(tmp[0])

    try:
        track = trackinfo[random.randrange(len(trackinfo))]
        fileurl = 'http:'+track['file']['mp3-128']
        print '-------------------------------'
        print 'Track: '+track['title']
        print 'Album: '+title
        print 'Artist: '+artist
        print the_url
        print '-------------------------------'
        cmd = 'mpv \"'+fileurl+'\" --no-video '
        os.system(cmd)
    except:
        print '[ERROR] cannot play song, skipping'


print '''
    ___               __                      ___          ___
   / _ )___ ____  ___/ /______ ___ _  ___    / _ \___ ____/ (_)__
  / _  / _ `/ _ \/ _  / __/ _ `/  ' \/ _ \  / , _/ _ `/ _  / / _ \\
 /____/\_,_/_//_/\_,_/\__/\_,_/_/_/_/ .__/ /_/|_|\_,_/\_,_/_/\___/
                                   /_/
'''

url = sys.argv[1]
tag = sys.argv[1]
# get list of albums
albums = get_album_links(tag)
'''
albums =[]
tagpage= requests.get(url).text
tmp = re.findall('class="item ">[\W\w]+?(?=<a)([\W\w]+?)(?=<\/li)',tagpage)
for a in tmp:
    a_link = re.findall('href="([^"]+)',a)
    albums.append(a_link[0])
    #print a_link[0]
'''
while True:
    url = albums[random.randrange(len(albums))]
    #print '[Selecting random album] '+ url
    play_random_song(url)
    time.sleep(2)
