#!/usr/bin/python
#https://bandcamp.com/tag/surf-rock
import re,json,os,sys
import time
import random
import requests

if (len(sys.argv) < 2):
    print 'a simple command line bandcamp radio - https://github.com/pvacey/bandcamp_radio'
    print '\nusage: \n    '+sys.argv[0]+' <url>'
    print '    '+sys.argv[0]+' https://bandcamp.com/tag/indie-rock\n'
    exit()
url = sys.argv[1]

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
    tmp = re.findall('trackinfo : (\[[^\]]+\])', html)
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

# get list of albums
albums =[]
tagpage= requests.get(url).text
tmp = re.findall('class="item ">[\W\w]+?(?=<a)([\W\w]+?)(?=<\/li)',tagpage)
for a in tmp:
    a_link = re.findall('href="([^"]+)',a)
    albums.append(a_link[0])
    #print a_link[0]

print '''
    ___               __                      ___          ___
   / _ )___ ____  ___/ /______ ___ _  ___    / _ \___ ____/ (_)__
  / _  / _ `/ _ \/ _  / __/ _ `/  ' \/ _ \  / , _/ _ `/ _  / / _ \\
 /____/\_,_/_//_/\_,_/\__/\_,_/_/_/_/ .__/ /_/|_|\_,_/\_,_/_/\___/
                                   /_/
'''

while True:
    url = albums[random.randrange(len(albums))]
    #print '[Selecting random album] '+ url
    play_random_song(url)
    time.sleep(2)
