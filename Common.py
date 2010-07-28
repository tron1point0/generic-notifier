import ConfigParser,os

appName = "appName"
rcFile = appName + "rc"

parser = ConfigParser.RawConfigParser()
if parser.read(rcFile) != []:
	icon = parser.get("application","icon")
	throbber = parser.get("application","throbber")
	interval = parser.get("application","interval")
else:
	icon = os.getcwd()+"/icon.png"
	throbber = "throbber.gif"
	interval = 5
	parser.add_section("application")
	parser.set("application","icon",icon)
	parser.set("application","throbber",throbber)
	parser.set("application","interval",interval)
	with open(rcFile, 'w') as config:
		parser.write(config)