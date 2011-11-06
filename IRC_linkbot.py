#!/usr/local/bin/env python3.1
# -*- coding: iso-8859-15 -*-
""" An IRC bot that does multiple things with urls"""

import socket
import string
from mechanize import Browser
from sgmllib import SGMLParser

#Join Irc
net = '' #Insert the Irc network eg(irc.blah@blah.com)
port = 6667
nick = '' #The nick you wan the bot to have eg(blah)
channel = '#test,#lobby' #Channels the bot will join
owner = '' #Owner of the bot
ident = '' #user used to identify with server
readbuffer = ''

#Connect the bot
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((net,port))
s.send('USER '+ident+' '+net+' bla :'+owner+'\r\n')
s.send('NICK '+nick+'\r\n')
s.send('JOIN '+chan+'\r\n')
print(s.recv(4096))

#Display text properly
keysss = {'&#039;':'\'','&#39;':'\'','&#8217;':'\'','&#x20AC;':'€','(':'',')':'','@':''}

#Array to hold link values
global linkz
linkz = []

#fill array with links already in file
def fillOld():
    global linkz
    try:
        with open("Links.txt", "r") as f:
            content = f.readlines() 
            linkz = content 
        print(linkz)
    except IOError, e:
        pass

#add link and title to a text file
def appendFile(linkage):
    with open("Links.txt", "a") as f:
        f.write(linkage)
    print('Added to File!')

#add link to my webpage
def appendWeb(linkage, web):
    with open("pages/page_4.html", "a") as f:
        f.write('<p><a href="'+web+'">'+linkage+'</a></p>')
    print('Added to Web!')

#replace words in text with dictionary values
def replace(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text

#Get the title of the linked page
def getTitle(url):
    b = Browser()
    try:
        b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        b.set_handle_robots(False)
        b.open(url)
        page = b.response().read()
        try:
            title = string.split(page, '<title>')
            pageTitle = string.split(title[1],'</title>')
            result = pageTitle[0]
        except IndexError, e:
            return ''
        return result
    except IOError, e:
        return ''
        
class TextExtracter(SGMLParser):
    def __init__(self):
        self.text = []
        SGMLParser.__init__(self)
    def handle_data(self, data):
        self.text.append(data)
    def getvalue(self):
        return ''.join(ex.text)

fillOld() #fill array with old links
while True:
    link = '' #stores link
    head = '12Title: ' #type of link
    totalLink = '' #For file storage
    readbuffer=readbuffer+s.recv(4096)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop()
    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)
        print(line)

    if(line[0]=='PING'):
        s.send('PONG '+line[1]+'\r\n')
        
    if(line[1]=='PRIVMSG') and len(line) > 2:
        for n in range(3,len(line)):
            if 'http://' in line[n]:
                link = line[n]
                if n == 3:
                    l = line[n]
                    link = l[1:]
                    print(link)
            elif 'www.' in line[n] and 'http://' not in line[n]:
                link = 'http://'+line[n]
                if n == 3:
                    l = line[n]
                    link = 'http://'+l[1:]
        
        if link != '':
            link = replace(link, keysss)
            t = getTitle(link)  #Get the title of the webpage
            t = string.strip(t)
            t = replace(t, keysss)
            
            #Custom coloured headings
            if '- YouTube' in t:
                head = '1,16You16,5Tube: '
                z = string.split(t, '- YouTube')
                t = z[0]
            if 'Redbrick' in t:
                head = '5Redbrick: '
                z = string.split(t, '|')
                t = z[0]
            if 'xkcd' in t:
                head = '15xkcd: '
                z = string.split(t, ':')
                t = z[1]
            if ' - Imgur' in t:
                head = '16imgur: '
                z = string.split(t, ' - Imgur')
                t = z[0]
            if ' | Techdirt' in t:
                head = ' 2Tech12dirt: '
                z = string.split(t, ' | Techdirt')
                t = z[0]            
            if 'www.google.' in link:
                head = '2,15G5,15o7,15o2,15g3,15l5,15e: '
            if 'http://www.reddit.com/' in link:
                head = '15ಠ_ಠ: '
            if 'http://www.rte.ie/' in link:
                head = '16,2RTE: '
                z = string.split(t, ' - RT')
                t = z[0]
                
            #Print Title to channel
            print(t)
            if t != '' and link != '':
                totalLink = link+' || '+t+'\n'
                #if link hasn't been before add it to file
                if totalLink not in linkz:
                    appendFile(totalLink) #Add to file
                    ex = TextExtracter()    
                    ex.feed(totalLink)
                    totalLin = ex.getvalue() #Prevent xss
                    linkz.append(totalLin) #Add to linkz[]
                    appendWeb(totalLin, link)
                    
                s.send('PRIVMSG '+line[2]+' :'+head+t+'\r\n')
    
    if(line[0]=='PING'):
        s.send('PONG '+line[1]+'\r\n')               