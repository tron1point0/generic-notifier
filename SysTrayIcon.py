from PyQt4 import QtGui,QtCore
import Common

class SysTrayIcon(QtGui.QSystemTrayIcon):
	iconPixmap,throbberPixmap = None,None

	checkSignal = QtCore.pyqtSignal()
	settingsSignal = QtCore.pyqtSignal()
	quitSignal = QtCore.pyqtSignal()

	throbberStartSignal = QtCore.pyqtSignal()
	throbberStopSignal = QtCore.pyqtSignal()
	messageCountSignal = QtCore.pyqtSignal(int)

	def __init__(self, icon, parent=None):
		QtGui.QSystemTrayIcon.__init__(self,icon,parent)
		menu = QtGui.QMenu(parent)
		self.iconPixmap = QtGui.QPixmap(Common.icon)
		self.throbberPixmap = QtGui.QPixmap(Common.throbber)

		checkAction = QtGui.QAction("Check mail",parent)
		settingsAction = QtGui.QAction("Settings...",parent)
		quitAction = QtGui.QAction("Quit",parent)

		checkAction.triggered.connect(self.checkSignal)
		settingsAction.triggered.connect(self.settingsSignal)
		quitAction.triggered.connect(self.quitSignal)
		self.throbberStartSignal.connect(self.showThrobber)
		self.throbberStopSignal.connect(self.hideThrobber)
		self.messageCountSignal.connect(self.updateMessageCount)

		menu.setTitle(Common.appName)
		menu.setDefaultAction(checkAction)
		menu.addAction(checkAction)
		menu.addAction(settingsAction)
		menu.addSeparator()
		menu.addAction(quitAction)

		self.setContextMenu(menu)

	def updateMessageCount(self, count):
		if count > 0:
			newPixmap = QtGui.QPixmap(self.iconPixmap)
			painter = QtGui.QPainter(newPixmap)
			painter.drawText(0,0,36,36,QtCore.Qt.AlignCenter,str(count))
			self.setIcon(QtGui.QIcon(newPixmap))
			painter.end()
		else:
			self.setIcon(QtGui.QIcon(self.iconPixmap))

	def showThrobber(self):
		newPixmap = QtGui.QPixmap(self.iconPixmap)
		painter = QtGui.QPainter(newPixmap)
		painter.drawPixmap(9,9,self.throbberPixmap)
		self.setIcon(QtGui.QIcon(newPixmap))
		painter.end()

	def hideThrobber(self):
		self.setIcon(QtGui.QIcon(self.iconPixmap))

	def quit(self):
		exit(0)