import web
web.config.debug = False
import os
from requests import get
from user_agents import parse
import pytz
from datetime import datetime
import random
from discord_webhook import DiscordWebhook
from bs4 import BeautifulSoup
import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from replit import db 
from easypydb import DB

###################################################
############# API UNDER DEVELOPMENT ###############
###################################################
authdb = DB("sso_tokens", os.environ["DB_TOKEN"])
authdb.autosave = True
authdb.autoload = True

devdb = DB("dev", os.environ["DB_TOKEN"])
devdb.autosave = True
devdb.autoload = True


os.system("clear")

render = web.template.render('templates/')
urls = (
	'/l/(.*)', 'short',
	'/add', 'add',
	'/', 'index',
	'/dash', 'index',
	'/edit/(.*)', 'edit',
	'/edit', 'edit2',
	'/delete', 'delete',
	'/details', 'url_info',
	'/info/(.*)/(.*)', 'public_info',
	  '/demo', 'demo',
	'/qrcode', 'qrcode',
	'/qrcode/view/(.*)', 'qrcodeview',
	'/shortweb', 'shortweb',
	'/namec', 'namec',
	'/login', 'login',
	'/signup', 'signup',
	'/bot/guild', 'botg',
	'/bot/dm', 'botd',
	'/bot_info', "bot_info",
	'/bmlet', 'bmlet',
	'/sitemap', 'sitemap',
	'/sitemap.xml', 'sitemapxml',
	'/(.*)', 'short2',
	'/api/docs', 'apidocs',
	'/api/add', 'apiadd',
	'/api/me', 'apime',
	'/api/edit', 'apiedit',
	'/api/delete', 'apidelete',
	'/api/details', 'apidetails'
	)

#os.system("clear")


app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'))
def notfound():
	return web.notfound(render.notfound())

class sitemapxml:
	def GET(self):
		web.header("Content-Type", 'application/xml')
		return open("static/sitemap.xml", "rb").read()

class sitemap:
	def GET(self):
		return render.sitemap()

class bmlet:
	def GET(self):
		post_input = web.input(_method='post')
		post_input = list(post_input)
		i = web.input()
		short = i.short
		url = i.url
		if i.token == "188b28e3da5d553300ceb9203fe65a5ddf83af76e9e591ade809d0848f230b1b":
			if short == "null" or short == "":
				letters = ["a","b",	"c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
				#Generate a 6 letter backend, you will only run out of 6 letter backends if you auto generate more than 46656 backends.
				tries = 0
				num = 1
				for l in range(num):
					letter = random.choice(letters)
					short = short+letter
				tries = 1
				while short in db:
					for l in range(num):
						letter = random.choice(letters)
						short = short+letter
					tries += 1
					total5 = 1
					for x in range(num):
						total5 = total5*num
					if tries == total5:
						num += 1
			if short not in db:
				db[short] = {
					"url": url,
					"name": "NONE",
					"webhook": "NONE",
					"agents": "NONE",
					"user": "CoolCoderSJ"
				}
				import json
				web.header('Content-Type', 'application/json')
				web.header('Access-Control-Allow-Origin', '*')
				web.header('Access-Control-Allow-Credentials', 'true')
				web.header('Access-Control-Allow-Methods', 'GET')
				web.header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
				return json.dumps({"BACKEND":short})
			return "No."



class botg:
	def POST(self):
		post_input = web.input(_method='post')
		post_input = list(post_input)
		print(post_input, web.ctx.env)
		for item in post_input:
			if item.split(":")[0] == "URL":
				url = item.split(":")[-1]
			if item.split(":")[0] == "SHORT":
				short = item.split(":")[-1]
		if short == "":
			letters = ["a","b",	"c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
			#Generate a 6 letter backend, you will only run out of 6 letter backends if you auto generate more than 46656 backends.
			tries = 0
			num = 1
			for l in range(num):
				letter = random.choice(letters)
				short = short+letter
			tries = 1
			while short in db:
				for l in range(num):
					letter = random.choice(letters)
					short = short+letter
				tries += 1
				total5 = 1
				for x in range(num):
					total5 = total5*num
				if tries == total5:
					num += 1
		if short not in db:
			db[short] = {
					"url": url,
					"name": "NONE",
					"webhook": "NONE",
					"agents": "NONE",
					"user": "EXTERNAL"
				}
			return short
		return False

class botd:
	def POST(self):
		post_input = web.input(_method='post')
		post_input = list(post_input)
		print(post_input)

		for item in post_input:
			if item.split(":")[0] == "URL":
				url = item.split(":")[-1]
			if item.split(":")[0] == "SHORT":
				short = item.split(":")[-1]
		if short == "":
			letters = ["a","b",	"c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
			#Generate a 6 letter backend, you will only run out of 6 letter backends if you auto generate more than 46656 backends.
			tries = 0
			num = 1
			for l in range(num):
				letter = random.choice(letters)
				short = short+letter
			tries = 1
			while short in db:
				for l in range(num):
					letter = random.choice(letters)
					short = short+letter
				tries += 1
				total5 = 1
				for x in range(num):
					total5 = total5*num
				if tries == total5:
					num += 1
		if short not in db:
			db[short] = {
					"url": url,
					"name": "NONE",
					"webhook": "NONE",
					"agents": "NONE",
					"user": "EXTERNAL"
				}
			return short
		return False


class bot_info:
	def POST(self):
		#os.system("clear")
		users2 = {}
		for url in db:
			users2[url] = db[url]["user"]
		i = web.input(_method="post")
		print(i)
		s = i.short
		if s in db:
			user = users2[s]
			import ast
			try:
				query = ast.literal_eval(str(db[s]["agents"]))
			except:
				query = db[s]['agents']
			if query != 'NONE':
				clicks = 0
				chrome = 0
				ff = 0
				safari = 0
				opera = 0
				edge = 0
				mac = 0
				ipad = 0
				android = 0
				windows7 = 0
				windows10 = 0
				apple = 0
				linux = 0
				chromeos= 0
				import ast
				try:
					query = ast.literal_eval(str(db[s]["agents"]))
				except:
					query = db[s]['agents']
				for line in query:
					clicks += 1
					if "Chrome" in line:
						chrome += 1
					if "Firefox" in line:
						ff += 1
					if "Safari" in line:
						safari += 1
					if "Opera" in line:
						opera += 1
					if "Edge" in line:
						edge += 1
					if "Mac" in line:
						mac += 1
					if "iPad" in line:
						ipad += 1
					if "Android" in line:
						android += 1
					if "Windows  10" in line:
						windows10 += 1
					if "Windows  7" in line:
						windows7 += 1
					if "Apple" in line:
						apple += 1
					if "Linux" in line:
						linux += 1
					if "Chrome OS" in line:
						chromeos += 1
				dev2 = [chrome, ff, safari, opera, edge, mac, ipad, android, windows7, windows10, apple,
				linux, chromeos]
				dev = ""
				for thing in dev2:
					sep = ","
					dev = str(dev)+sep+str(thing)
				tots = str(clicks)+"|"+dev
			return tots
		return False


class login:
	def GET(self):
		##os.system("clear")
		i = web.input(code=0)
		msg = ""
		if i.code == "1":
			msg = "An error occurred while logging you in. Please try again or contact a deveoper."
		return render.login(msg)
		##os.system("clear")

	def POST(self):
		##os.system("clear")
		i = web.input()
		r = requests.post("https://sjauth.coolcodersj.repl.co/apil", data={"user":i.user, "passw":i.passw, "cn":"SJURL"})
		print(r.text)
		if r.text == "True":
			session.user = i.user
			raise web.seeother("/")
		else:
			raise web.seeother("/login?code=1")
		##os.system("clear")


class signup:
	def GET(self):
		##os.system("clear")
		i = web.input(code=0)
		msg = ""
		if i.code == "1":
			msg = "An error occurred while signing you up. Please try again or contact a deveoper."
		return render.signup(msg)
		##os.system("clear")

	def POST(self):
		##os.system("clear")
		i = web.input()
		r = requests.post("https://sjauth.coolcodersj.repl.co/apisi", data={"user":i.user, "passw":i.passw, "cn":"SJURL"})
		if r.text == "True":
			web.setcookie("logged_in", True)
			session.user = i.user
			raise web.seeother("/")
		else:
			raise web.seeother("/signup?code=1")
		##os.system("clear")



class logout:
	def GET(self):
		#os.system("clear")
		session.user = ""
		raise web.seeother("/")
		#os.system("clear")


class shortweb:
	def POST(self):
		user = session.get("user")
		#os.system("clear")
		i = web.input()
		short = i.short
		query = db[short]
		if query[3] != 'NONE':
			db[short] = {
					"url": db[short]['url'],
					"name": db[short]['name'],
					"webhook": "NONE",
					"agents": db[short]['agents'],
					"user": db[short]['user']
				}
		else:
			db[short] = {
					"url": db[short]['url'],
					"name": db[short]['name'],
					"webhook": i.webhook,
					"agents": db[short]['agents'],
					"user": db[short]['user']
				}
		raise web.seeother("/")
		#os.system("clear")



class namec:
	def POST(self):
		#os.system("clear")
		if session.get("user"):
			i = web.input()
			name = i.name
			short = i.short
			user = session.get("user")
			query = db[short]
			if name == '':
				db[short] = {
					"url": db[short]['url'],
					"name": "NONE",
					"webhook": db[short]['webhook'],
					"agents": db[short]['agents'],
					"user": db[short]['user']
				}
			else:
				db[short] = {
					"url": db[short]['url'],
					"name": name,
					"webhook": db[short]['webhook'],
					"agents": db[short]['agents'],
					"user": db[short]['user']
				}
			raise web.seeother("/")
		else:
			return render.promo()
		#os.system("clear")




class short2:
	def GET(self, short):
		#os.system("clear")
		if short != "" and short != "add" and short != "details" and short != "edit" and not short.startswith("edit") and not short.startswith("l") and short != "demo" and short != "qrcode" and not short.startswith("qrcode/view") and short != "unshortr":
			raise web.seeother("/l/"+short)
		#os.system("clear")



class qrcode:
	def POST(self):
		#os.system("clear")
		if session.get("user"):
			import pyqrcode
			import png
			from pyqrcode import QRCode
			i = web.input()
			short = "https://sjurl.tk/l/"+i.short
			qr = pyqrcode.create(short)
			qr.png("static/images/qr/"+i.short+'.png', scale = 6)
			raise web.seeother("/")
		else:
			return render.promo()
		#os.system("clear")


class qrcodeview:
	def GET(self, qrcode):
		#os.system("clear")
		if session.get("user"):
			return render.qrcodeview(qrcode)
		else:
			return render.promo()
		#os.system("clear")



class short:
	def GET(self, short):
		if short == "/" or short == "" or short == "favicon.ico":
			raise web.seeother('/dash')
		user = {}
		for url in db:
			if url != "/" and url != "x" and url != '/money' and url != "/tone" and url != "https://replit.com/@CoolCoderSJ/SJURL":
				# print(url)
				user[url] = db[url]['user']
		if short.endswith("+"):
				short1 = short.split("+")[-2]
				url = db[short1]['url']
				if not url.startswith("http"):
					url = "http://"+url
				r = get(url)
				soup = BeautifulSoup(r.text, 'html.parser')
				titles = ""
				for title in soup.find_all('title'):
					title = str(title)
					titles += str(title.split("<title>")[1].split("</title>")[0])+"\n"
				user = user[short1]

				name = db[short1]['name']
				return render.sneak(short1, url, titles, name)
		#os.system("clear")
		#os.system("clear")
		if short.split("/")[0] in db or short.split("#")[0] in db or short.split("?")[0] in db:
			if short.split("/")[0] in db:
				params = short.split(short.split("/")[0])
				params = "".join(params)
				short1 = short.split("/")[0]
			elif short.split("#")[0] in db:
				params = short.split(short.split("#")[0])
				params = "".join(params)
				short1 = short.split("#")[0]
			elif short.split("?")[0] in db:
				params = short.split(short.split("?")[0])
				params = "".join(params)
				short1 = short.split("?")[0]
			else:
				params = ""
				short1 = short.split("/")[0]
			
			safecheck = requests.post(f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={os.environ['SAFE_BROWSING_KEY']}", headers={"Content-Type": "application/json"}, data="""{
				"client": {
				"clientId": "SJURL",
				"clientVersion": "5.2"
				},
				"threatInfo": {
				"threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
				"platformTypes": ["ANY_PLATFORM"],
				"threatEntryTypes": ["URL"],
				"threatEntries": [
					{"url": '"""+db[short1]['url']+"""'}
				]
				}
			}"""
			)
			safecheck = safecheck.json()
			if db[short1]['url'] in str(safecheck):
				typ = safecheck['matches'][0]['threatType']
				platform = safecheck['matches'][0]['platformType']
				return render.dangerous(typ, platform, db[short1])


			if short1 in db:

				tz_NY = pytz.timezone('America/New_York')
				now = datetime.now(tz_NY)
				dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
				usr_str = web.ctx.env['HTTP_USER_AGENT']
				usr_agent2 = parse(usr_str)
				usr_agent = ""
				if usr_agent2.browser.family != None:
					bfamily = usr_agent2.browser.family
				else:
					bfamily = ""
				if usr_agent2.browser.version_string != None:
					bversion = usr_agent2.browser.version_string
				else:
					bversion = ""

				if usr_agent2.os.family != None:
					osfamily = usr_agent2.os.family
				else:
					osfamily = ""
				if usr_agent2.os.version_string != None:
					osversion = usr_agent2.os.version_string
				else:
					osversion = ""

				if usr_agent2.device.brand != None:
					devbrand = usr_agent2.device.brand
				else:
					devbrand = ""
				if usr_agent2.device.family != None:
					devfamily = usr_agent2.device.family
				else:
					devfamily = ""
				if usr_agent2.device.model != None:
					devmodel = usr_agent2.device.model
				else:
					devmodel = ""
				usr_agent = bfamily + "  " + bversion + "  " + osfamily + "  " + osversion + "  " + devbrand + "  " + devfamily + "  " + devmodel + "  EST TIME:  " + dt_string
				line = usr_agent
				import ast
				if db[short]['agents'] == 'NONE':
					agents = []
				else:
					try:
						agents = ast.literal_eval(str(db[short]['agents']))
					except:
						agents = db[short]['agents']
				print(len(agents))
				agents.append(line)
				print(len(agents))
				db[short] = {
					"url": db[short]['url'],
					"name": db[short]['name'],
					"webhook": db[short]['webhook'],
					"agents": agents,
					"user": db[short]['user']
				}
				url = db[short1]['url']
				if not url.startswith("https://"):
					url = "https://"+url

				if db[short]['webhook'] != 'NONE':
					webhookurl = db[short]['webhook']
					webhook = DiscordWebhook(url=webhookurl, content="A Link was visited. \n\nDetails:\nShortened Backend: "+short+"\nFull URL: "+url+"\nDevice details: "+bfamily + "  " + bversion + "  " + osfamily + "  " + osversion + "  " + devbrand + "  " + devfamily + "  " + devmodel+"\n\nTime: "+dt_string)
					webhook.execute()
				raise web.seeother(url+params)
			else:
				raise web.notfound()
		#os.system("clear")


class add:
	def GET(self):
		#os.system("clear")
		if session.get("user"):
			idk = ""
			return render.add(db, idk)
		else:
			return render.promo()
		#os.system("clear")

	def POST(self):
		user = session.get("user")
		#os.system("clear")
		i = web.input()
		short=i.short
		if short == "":
			#pass a list of letters
			letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
			#Generate a 6 letter backend, you will only run out of 6 letter backends if you auto generate more than 46656 backends.
			tries = 0
			for l in range(6):
				letter = random.choice(letters)
				short = short+letter
			tries = 1
			num = 6
			while short in db:
				for l in range(num):
					letter = random.choice(letters)
					short = short+letter
				tries += 1
				if tries == 46656:
					num += 1
		if "webhook" in i:
			if i.webhook != '':
				webhookurl = i.webhook
			else:
				webhookurl = "NONE"
		else:
			webhookurl = "NONE"
		url = i.url
		name = i.name
		if name == "":
			name = 'NONE'
		if short not in db:
			db[short] = {
					"url": url,
					"name": name,
					"webhook": webhookurl,
					"agents": "NONE",
					"user": user
				}
			return render.success(short, url)
		else:
			return render.alert()
		#os.system("clear")


class index:
	def GET(self):
		#os.system("clear")
		if session.get("user"):
			user = session.get("user")
			print(user)
			passw = ""
			shortwebs = []
			names = {}
			userlinks = {}
			for short in db:
				#DB Glitches from time to time so ignore glitched backends
				if short != "/" and short != "x" and short != '/money' and short != "/tone" and short != "https://replit.com/@CoolCoderSJ/SJURL":
					name = ""
					if db[short]['webhook'] != 'NONE':
						shortwebs.append(short)

					if db[short]['name'] != 'NONE':
						name = db[short]['name']
					names[short] = name
			print("a")
			for short in db:
				if short != "/" and short != "x" and short != '/money' and short != "/tone" and short != "https://replit.com/@CoolCoderSJ/SJURL":
					if db[short]['user'] == user:
						userlinks[short] = db[short]['url']
			print("b")
			query = []
			for short in db:
				if short != "/" and short != "x" and short != '/money' and short != "/tone" and short != "https://replit.com/@CoolCoderSJ/SJURL":
					import ast
					e = str(db[short]['agents'])
					if e == "NONE":
						e = "[]"
					try:
						e = ast.literal_eval(e)
					except:
						e = e
					query2 = e
					for line in query2:
						query.append(line)
			print("c")
			# x_axis = []
			# y_axis = []
			# for line in query:
			# 	line = line.split("2021")[0].split("EST TIME: ")[-1]
			# 	num = 0
			# 	for x in query:
			# 		if line in x:
			# 			num += 1
			# 	if line not in x_axis:
			# 		x_axis.append(line)
			# 		y_axis.append(num)
			# f = plt.figure()	
			# plt.plot(x_axis, y_axis, "r")
			# plt.savefig(f"static/images/graphs/{user}.png", transparent=True, facecolor="w")
			# f.clear()
			# plt.close(f)
			# print("d")
			return render.index(userlinks, passw, shortwebs, names, f"https://sjurl.tk/static/images/graphs/{user}.png")
		else:
			return render.promo()
		#os.system("clear")
class edit:
	def GET(self, short):
		#os.system("clear")
		if session.get("user"):
			user = session.get("user")
			user2 = db[short]['user']
			if user2 == user:
				passw = ""
				return render.edit(db, short, passw)
			else:
				raise web.seeother('/')
		else:
			return render.promo()
		#os.system("clear")


class edit2:
	def POST(self):
		#os.system("clear")
		if session.get("user"):
			i = web.input()
			newurl = i.newurl
			short = i.short
			db[short] = {
					"url": newurl,
					"name": db[short]['name'],
					"webhook": db[short]['webhook'],
					"agents": db[short]['agents'],
					"user": db[short]['user']
				}
			raise web.seeother('/')
		else:
			return render.promo()
		#os.system("clear")


class delete:
	def POST(self):
		#os.system("clear")
		user = session.get("user")
		if session.get("user"):
			i = web.input()
			short = i.short

			if os.path.exists("static/images/qr/"+short+".png"):
				os.remove("static/images/qr/"+short+".png")
			del db[short]
			raise web.seeother('/')
		else:
			return render.promo()
		#os.system("clear")


class url_info:
	def POST(self):
		#os.system("clear")
		user = session.get("user")
		if session.get("user"):
			agent = []
			i = web.input()
			s = i.short

			import ast
			if db[s]['agents'] == "NONE":
					query = []
			else:
				try:
					query = ast.literal_eval(str(db[s]['agents']))
				except:
					query = db[s]['agents']
			if query != 'NONE':
				clicks = 0
				chrome = 0
				ff = 0
				safari = 0
				opera = 0
				edge = 0
				mac = 0
				ipad = 0
				android = 0
				windows7 = 0
				windows10 = 0
				apple = 0
				linux = 0
				chromeos= 0

				import ast
				if db[s]['agents'] == "NONE":
					query = []
				else:
					try:
						query = ast.literal_eval(str(db[s]['agents']))
					except:
						query = db[s]['agents']
				for line in query:
					agent.append(line)
					clicks += 1
					if "Chrome" in line:
						chrome += 1
					if "Firefox" in line:
						ff += 1
					if "Safari" in line:
						safari += 1
					if "Opera" in line:
						opera += 1
					if "Edge" in line:
						edge += 1
					if "Mac" in line:
						mac += 1
					if "iPad" in line:
						ipad += 1
					if "Android" in line:
						android += 1
					if "Windows  10" in line:
						windows10 += 1
					if "Windows  7" in line:
						windows7 += 1
					if "Apple" in line:
						apple += 1
					if "Linux" in line:
						linux += 1
					if "Chrome OS" in line:
						chromeos += 1
				dev = [chrome, ff, safari, opera, edge, mac, ipad, android, windows7, windows10, apple,
				linux, chromeos]
				x_axis = []
				y_axis = []
				for line in query:
					line = line.split("2021")[0].split("EST TIME: ")[-1]
					num = 0
					for x in query:
						if line in x:
							num += 1
					if line not in x_axis:
						x_axis.append(line)
						y_axis.append(num)
				f = plt.figure()
				plt.plot(x_axis, y_axis, "r")
				plt.savefig(f"static/images/graphs/{user}{s}.png", transparent=True, facecolor="w")
				f.clear()
				plt.close(f)
			return render.details(agent, clicks, dev, s, f"https://sjurl.tk/static/images/graphs/{user}{s}.png")
		else:
			return render.promo()
		#os.system("clear")

class public_info:
	def GET(self, s, option):
		#os.system("clear")
		options = []
		if "221" in option:
			options.append("clicks")
		if "324" in option:
			options.append("table")
		if "239" in option:
			options.append("agents")
		if "692" in option:
			options.append("times")
		if "734" in option:
			options.append("graph")
		user = session.get("user")
		agent = []
		i = web.input()
		import ast
		if db[s]['agents'] == "NONE":
				query = []
		else:
			try:
				query = ast.literal_eval(str(db[s]['agents']))
			except:
				query = db[s]['agents']
		if query != 'NONE':
			clicks = 0
			chrome = 0
			ff = 0
			safari = 0
			opera = 0
			edge = 0
			mac = 0
			ipad = 0
			android = 0
			windows7 = 0
			windows10 = 0
			apple = 0
			linux = 0
			chromeos= 0
			import ast
			if db[s]['agents'] == "NONE":
				query = []
			else:
				try:
					query = ast.literal_eval(str(db[s]['agents']))
				except:
					query = db[s]['agents']
			for line in query:
				agent.append(line)
				clicks += 1
				if "Chrome" in line:
					chrome += 1
				if "Firefox" in line:
					ff += 1
				if "Safari" in line:
					safari += 1
				if "Opera" in line:
					opera += 1
				if "Edge" in line:
					edge += 1
				if "Mac" in line:
					mac += 1
				if "iPad" in line:
					ipad += 1
				if "Android" in line:
					android += 1
				if "Windows  10" in line:
					windows10 += 1
				if "Windows  7" in line:
					windows7 += 1
				if "Apple" in line:
					apple += 1
				if "Linux" in line:
					linux += 1
				if "Chrome OS" in line:
					chromeos += 1
			dev = [chrome, ff, safari, opera, edge, mac, ipad, android, windows7, windows10, apple,
			linux, chromeos]
			if not "times" in options:
				agent = []
				for line in query:
					e = line.split("EST")[0]
					agent.append(e)
		x_axis = []
		y_axis = []
		for line in query:
			line = line.split("2021")[0].split("EST TIME: ")[-1]
			num = 0
			for x in query:
				if line in x:
					num += 1
			if line not in x_axis:
				x_axis.append(line)
				y_axis.append(num)
		f = plt.figure()
		plt.plot(x_axis, y_axis, "r")
		plt.savefig(f"static/images/graphs/{user}{s}.png", transparent=True, facecolor="w")
		f.clear()
		plt.close(f)
		return render.public(agent, clicks, dev, options, f"https://sjurl.tk/static/images/graphs/{user}{s}.png")

		#os.system("clear")

class demo:
	def GET(self):
		return render.demo()
		#os.system("clear")
	def POST(self):
		user = "EXTERNAL"
		#os.system("clear")
		i = web.input()
		short=i.short
		if short == "":
			#pass a list of letters
			letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
			#Generate a 6 letter backend, you will only run out of 6 letter backends if you auto generate more than 46656 backends.
			tries = 0
			for l in range(6):
				letter = random.choice(letters)
				short = short+letter
			tries = 1
			num = 6
			while short in db:
				for l in range(num):
					letter = random.choice(letters)
					short = short+letter
				tries += 1
				if tries == 46656:
					num += 1
		if "webhook" in i:
			if i.webhook != '':
				webhookurl = i.webhook
			else:
				webhookurl = "NONE"
		else:
			webhookurl = "NONE"
		url = i.url
		name = i.name
		if name == "":
			name = 'NONE'
		if short not in db:
			db[short] = {
					"url": url,
					"name": name,
					"webhook": webhookurl,
					"agents": "NONE",
					"user": user
				}
			return render.success(short, url)
		else:
			return render.alert()
		#os.system("clear")

class apidocs:
	def GET(self):
		raise web.seeother("https://auth.sjurl.tk/api/docs/v2")

if __name__ == "__main__":
	app.notfound = notfound
	app.run()
