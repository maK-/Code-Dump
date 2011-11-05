"""Python Irc bot that does various mundane tasks"""

#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-
import socket
import string
import random
from mechanize import Browser
from time import strftime

net = '' #Insert the Irc network eg(irc.blah@blah.com)
port = 6667
nick = '' #The nick you wan the bot to have eg(blah)
channel = '#test,#lobby' #Channels the bot will join
owner = '' #Owner of the bot
ident = '' #user used to identify with server
readbuffer = ''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((net,port))
s.send('USER '+ident+' '+net+' bla :'+owner+'\r\n')
s.send('NICK '+nick+'\r\n')
s.send('JOIN '+channel+'\r\n')
s.send('PRIVMSG '+nick+' :Come at me bro!?\r\n')
print s.recv(4096)

#strip starting : and following !network.blah.com
def getName(x):
	nix = string.split(x,"!")
	x = nix[0]
	y = x[1:]
	return y

#make changes and replace words in text
def replace(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text

#get shadows stats
def stats(channel):
	wordreplace = { '</table>':'', '<br>':'',"<table class='simple'><tr><td class='white'><img src='spam.gif'>":'', '<td>':'  ', "<br><tr><td class='white'><img src='chatty.gif'>":'', "<br><tr><td class='white'><img src='kick.GIF'>":'', "<br><tr><td class='white'><img src='enter.png'>":'', "<tr><td class='white'><img src='clock.gif'>":'', "<tr><td class='white'><img src='tumbleweed.gif'>":'', "<tr><td class='white'><img src='curse.gif'>":'', "<tr><td class='white'><img src='hello.png'>":'', "<br><br></table><br>":'' }
	stripchannel = channel[1:]
	info = ''
	b = Browser()
	if stripchannel == 'intersocs' or 'interbots':
		b.open("http://www.redbrick.dcu.ie/~shadow/intersocs.html")
	else:
		b.open("http://www.redbrick.dcu.ie/~shadow/lobby.html")
	source = b.response().read()
	stat = string.split(source, 'Stats of Statsitude')
	stat2  = stat[1]
	stat = string.split(stat2, '<table width=80%>')
	stat2 = stat[0]
	result = replace(stat2, wordreplace)
	stat = string.split(result, "  ")
	for n in range(0,5):
		info += stat[n]+' ÏŸâ—ÏŸ '
	info2 = ' ÏŸâ—ÏŸ '
	for n in range(5,8):
		info2 += stat[n]+' ÏŸâ—ÏŸ '
	s.send('NOTICE '+channel+' :'+info[1:]+'\r\n')
	s.send('NOTICE '+channel+' :'+info2[1:]+'\r\n')

#change to circle text
def circle(fin):
	msg = ''
	bet = 'â“ â“‘ â“’ â““ â“” â“• â“– â“— â“˜ â“™ â“š â“› â“œ â“ â“ž â“Ÿ â“  â“¡ â“¢ â“£ â“¤ â“¥ â“¦ â“§ â“¨ â“©'
	betlist = string.split(bet,' ')
	alphabet = "a b c d e f g h i j k l m n o p q r s t u v w x y z"
	alphalist = string.split(alphabet,' ')
	capbet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
	caplist = string.split(capbet,' ')
	letter = ''
	
	for y in range(0,len(fin)):
		letter = fin[y]
		if letter in alphalist:
			msg += betlist[alphalist.index(letter)]+' '
		elif letter in caplist:
			msg += betlist[caplist.index(letter)]+' '
		else:
			msg += str(' ')
	return msg
	
#Generate porn url	
def generate(num):
	t = True
	while(t):	
		r = Browser()	
		url = 'http://www.redtube.com/'+str(num)
		try:
			r.open(url)
			redtube = r.response().read()
			title = string.split(redtube, 'videoTitle">')
			VideoTitle = string.split(title[1], '</h1>')
			video = VideoTitle[0].replace('videoTitle">', '')
			t = False
		except IOError, e:
			num = random.randint(100,120000)
	return ' '+video+' ['+url+']'

#Getting video list for top new uploads
def getvid(st):
	values = []
	for win in range(1,len(st)):
		video = st[win]
		vidurl = string.split(video, '"')
		url = vidurl[1]
		vidTitle = vidurl[3]
		values.append(url)
		values.append(vidTitle)
	return values
	
				
def top(hm):
	awesome = []
	br = Browser()	
	url = 'http://www.redtube.com/'
	br.open(url)
	redtube = br.response().read()
	title = string.split(redtube, '<h2 class="videoTitle">')
	titvid = getvid(title)
	
	for no in range(0,len(titvid),2):
		awesome.append(hm+titvid[no+1]+' [http://www.redtube.com'+titvid[no]+'] ')
	return awesome

#REDDIT - TIL
def tilget(n):
	br = Browser()	
	url = 'http://www.reddit.com/r/todayilearned/'
	br.open(url)
	reddit = br.response().read()
	tils = []
	redtil = ''
	redsplit = string.split(reddit, '" >TIL')
	for i in range(1, 25):
		redtil = til(redsplit[i])
		tils.append(redtil)
	return tils[n]

#stripping - TIL
def til(st):
	redsp = string.split(st, '</a>')
	thetil = 'TIL -'+redsp[0]
	return thetil	

#calculater
def answerget(q):
	b = Browser()
	b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	b.set_handle_robots(False)
	b.open('http://www.google.ie')
	b.select_form(nr=0)
	b.form['q'] = q
	b.submit()
	google = b.response().read()
	answer = string.split(google, '<b>')
	retans = string.split(answer[1], '</b>')
	return retans[0]

#retrieves a random quote
def quoteget(url):
	b = Browser()
	b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	b.set_handle_robots(False)
	b.open(url)
	quote = b.response().read()
	quot = string.split(quote, 'size=+2>\r\n')
	quot2 = string.split(quot[1], '</font>')
	quote = quot2[0].replace('<br><br>',' - ')
	return quote

#get time of a city
def timeget(city):
	b = Browser()
	b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	b.set_handle_robots(False)
	b.open('http://www.google.ie')
	b.select_form(nr=0)
	b.form['q'] = 'time '+city
	b.submit()
	t = b.response().read()
	ti = string.split(t, 'font-size:medium"><b>')
	tim = string.split(ti[1], '</b>')
	return tim[0]

#get md5 decrypted from databases
def getmd5(st):
	b = Browser()
	b.open('http://md5.noisette.ch/md5.php?hash='+st)
	passw = b.response().read()
	if '<error>' in passw:
		return 'Hash is not in database or string is not a true md5 hash'
	else:
		password = string.split(passw, '<string><![CDATA[')
		passw = password[1]
		password = string.split(passw, ']]></string>')
		return password[0]

#--------------------------
#Main Bot loop
#--------------------------
while True:
	sentence = '' #multiple words...
	readbuffer=readbuffer+s.recv(2048)
	temp=string.split(readbuffer, "\n")
	readbuffer=temp.pop()
	for line in temp:
		line=string.rstrip(line)
		line=string.split(line)
		
		if(line[0]=='PING'):
			s.send('PONG '+line[1]+'\r\n')
		
		if(line[1]=='PRIVMSG'):
			#necessary to get full sentence
			for n in range(4,len(line)):
				sentence += line[n]+' '
			print sentence
			name = line[0]
			user = getName(name)
			print 'private message from ' + user
			
			#print symbols
			if line[3] == ':!symbols':
				s.send('NOTICE '+line[2]+' :â˜® âœˆ â™‹ ì›ƒ ìœ  â˜  â˜¯ â™¥ âœŒ âœ– â˜¢ â˜£ â˜¤ âšœ â– Î£ âŠ— â™’ â™  Î© â™¤ â™£ â™§ â™¡ â™¦â™¢â™” â™• â™š â™› â˜… â˜† âœ® âœ¯ â˜„ â˜¾ â˜½ â˜¼ â˜€ â˜ â˜‚ â˜ƒ â˜» â˜º â™¬ âœ„ âœ‚ âœ† âœ‰ âœ¦ âœ§ âˆž â™‚ â™€ â˜¿ â¤ â¥ â¦ â§ â„¢ Â® Â© âœ— âœ˜ âŠ— â™’ â–¢ â–² â–³ â–¼ â–½ â—† â—‡ â—‹ â—Ž â— â—¯ Î” â—• â—” ÊŠ ÏŸ áƒ¦ å›ž â‚ª âœ“ âœ” âœ• â˜¥ â˜¦ â˜§ â˜¨ â˜© â˜ª â˜« â˜¬ â˜­ â„¢Â©Â® Â¿Â¡Â½â…“â…”Â¼Â¾ â…›â…œâ…â…ž â„… â„–â‡¨ âˆƒâˆ§âˆ  âˆ¨âˆ©âŠ‚ âŠƒâˆª Ñ‡ âˆž\r\n')
				s.send('NOTICE '+line[2]+' : â™ª â™« â™© â™¬ â™­ â™® â™¯ Â° Ã¸ â˜¼ â˜€ â˜ â˜‚ â˜ƒ â˜„ â˜¾ â˜½ â„ â˜‡ â˜ˆ âŠ™ â˜‰ â„ƒ â„‰ Â° â… âœº ÏŸ â™¥ â¤ â¥ â£ â¦ â§ â™¡ â™‹ â™‚ â™€ â˜¿ ì›ƒ ìœ  \r\n')
			
			#Print commands
			if line[3] == ':!commands':
				s.send('PRIVMSG '+line[2]+' :'+user+': !quote !til !symbols !calc !helpcalc !stats !circle !faproulette !newfap !inception !rimshot !time !md5 !tomd5 [MORE TO COME]\r\n')
			
			#Shadows stats
			if line[3] == ':!stats':
				stats(line[2])

			#Circle text
			if line[3] == ':!circle':
				msg = ''
				msg = circle(sentence)
				try:
					if len(line[4]) >= 0 :
						s.send('PRIVMSG '+line[2]+' :'+user+': '+msg+'\r\n')
				except IndexError:
						s.send('PRIVMSG '+line[2]+' :'+user+': Format => !circle <message>\r\n')
			
			#Change Nickname
			if line[3] == ':!nick':
				try:
					if len(line[4]) >= 0 and len(line[4]) <= 8:
						nick = line[4]
						s.send('NICK '+nick+'\r\n')
				except IndexError:
						s.send('PRIVMSG '+line[2]+' :'+user+': Format => !nickchange <nick>\r\n')
			#horny?
			if line[3] == ':!faproulette':
				number = random.randint(100,120000)
				link = generate(number)
				s.send('PRIVMSG '+line[2]+' :'+user+': '+link+'\r\n')
	
			#top <int> new videos
			if line[3] == ':!newfap':
				winning = []
				hmm = 'Title: '
				winning = top(hmm)
				try:
					if len(line[4]) >= 0 :
						amount = int(line[4])
						if amount > 5 :
							amount = 5
						for a in range(0,amount):
							s.send('PRIVMSG '+line[2]+' :'+user+': '+winning[a]+'\r\n')	
				except IndexError:
						s.send('PRIVMSG '+line[2]+' :'+user+': Format => !newfap <int> \r\n')
				
			#link to inception button
			if line[3] == ':!inception':	
				s.send('NOTICE '+line[2]+' :[http://inception.davepedu.com/] \r\n')

			#Reddit - TIL
			if line[3] == ':!TIL' or line[3] == ':!til':
				k = {'&amp;':'&','&quot;':'"'}
				rnum = random.randint(1,23)
				tilx = tilget(rnum)
				tilx = replace(tilx, k)
				s.send('PRIVMSG '+line[2]+' :'+user+': '+tilx+'\r\n')
			
			#rimshot
			if line[3] == ':!rimshot':
				s.send('NOTICE '+line[2]+' :[http://instantrimshot.com/] \r\n')

			#google calculator
			if line[3] == ':!calc':
				try:					
					if len(line[4]) >= 2 :
						if len(line) > 5:
							if line[5] == 'in' and len(line) > 6:
								line[4] += ' '+line[5]+' '+line[6]
						if len(line) > 7:
							line[4] == ' '+line[5]+' '+line[6]+' '+line[7]
						googkey = { '<font size=-2> </font>':'','<sup>':'','</sup>':'',' &#215; ':'','<i>':'','</i>':''}
						answer = replace(answerget(line[4]), googkey)
						s.send('PRIVMSG '+line[2]+' :'+user+': '+answer+'\r\n')
				except IndexError:
						s.send('PRIVMSG '+line[2]+' :'+user+': Format => !calc <equation>\r\n')
			
			#Calculator options	
			if line[3] == ':!helpcalc':
				s.send('PRIVMSG '+line[2]+' :'+user+': No spaces for regular equations. [http://www.googleguide.com/calculator.html]\r\n')

			#quotes
			if line[3] == ':!quote':
				site = 'http://ivyjoy.com/quote.shtml'
				quote = quoteget(site)
				s.send('NOTICE '+line[2]+' :'+quote+'\r\n')

			#world clock
			if line[3] == ':!time':
				try:	
					if len(line) == 4:
						time = timeget('Dublin')
						s.send('PRIVMSG '+line[2]+' :'+user+': It\'s '+time+' in Dublin\r\n')
				
					if len(line) == 5:
						time = timeget(line[4])
						s.send('PRIVMSG '+line[2]+' :'+user+': It\'s '+time+' in '+line[4]+'\r\n')
					
					if len(line) == 6:
						big = line[4]+' '+line[5]
						time = timeget(big)
						s.send('PRIVMSG '+line[2]+' :'+user+': It\'s '+time+' in '+big+'\r\n')
				except IndexError:
						s.send('PRIVMSG '+line[2]+' :'+user+': Format => !time <city>\r\n')

			#from md5
			if line[3] == ':!md5':
				if len(line) == 5:
					decrypted = getmd5(line[4])
					s.send('PRIVMSG '+line[2]+' :'+user+': '+decrypted+'\r\n')
				else:
					s.send('PRIVMSG '+line[2]+' :'+user+': Format => !md5 <md5-hash>\r\n')
			
			#to md5
			if line[3] == ':!tomd5':
				if len(line) == 5:
					hsh = hashlib.md5()
					hsh.update(line[4])
					h = hsh.hexdigest()
					s.send('PRIVMSG '+line[2]+' :'+user+': '+h+'\r\n')
				else:
					s.send('PRIVMSG '+line[2]+' :'+user+': Format => !tomd5 <string>\r\n')
					
					
		    #quit a channel
			if line[3] == ':!q':
				if len(line) == 5:
					s.send('PART '+line[4]+' :lulz.\r\n')
					
		    
			#join a channel
			if line[3] == ':!join':
				if len(line) == 5:
					s.send('JOIN '+line[4]+'\r\n')
