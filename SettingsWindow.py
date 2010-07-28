from PyQt4 import QtGui,QtCore
import Common,ConfigParser,base64

class SettingsWindow(QtGui.QWidget):
	options = {}
	parser = ConfigParser.SafeConfigParser()

	def __init__(self,required,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.setWindowTitle("Settings")
		layout = QtGui.QGridLayout()
		self.setLayout(layout)

		rowCount = 0
		parser = self.parser
		parser.read(Common.rcFile)

		for option in required:
			try:
				parser.get("account",option)
			except ConfigParser.NoSectionError:
				parser.add_section("account")
				parser.set("account",option,"")
			except ConfigParser.NoOptionError:
				parser.set("account",option,"")

		for section in parser.sections():
			layout.addWidget(QtGui.QLabel(section.title()),rowCount,0,1,2)
			self.options[section] = {}
			rowCount += 1
			for option in parser.options(section):
				layout.addWidget(QtGui.QLabel(option.title()),rowCount,0)
				self.options[section][option] = QtGui.QLineEdit()
				self.options[section][option].setText(parser.get(section,option))
				if option == "password":
					self.options[section][option].setEchoMode(QtGui.QLineEdit.Password)
					self.options[section][option].setText(base64.b64decode(parser.get(section,option)))
				layout.addWidget(self.options[section][option],rowCount,1)
				rowCount += 1
		save = QtGui.QPushButton("Save")
		cancel = QtGui.QPushButton("Cancel")

		layout.addWidget(save,rowCount,0)
		layout.addWidget(cancel,rowCount,1)

		save.clicked.connect(self.saveEvent)
		cancel.clicked.connect(self.closeEvent)

	def settingsFromPollingDaemon(self):
		self.show()

	def saveEvent(self,event=None):
		for section in self.options:
			for option in self.options[section]:
				self.parser.set(section,option,str(self.options[section][option].text()))
				if option == "password":
					self.parser.set(section,option,base64.b64encode(str(self.options[section][option].text())))
		with open(Common.rcFile,'w') as rcFile:
			self.parser.write(rcFile)
		self.closeEvent()

	def closeEvent(self,event=None):
		self.hide()
		if event is not None: event.ignore()