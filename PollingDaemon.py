from PyQt4 import QtCore
import Common,sys,ConfigParser,thread,time,base64

class PollingDaemon(QtCore.QObject):
	account = {'username': None,'password': None}

	readSettingsSignal = QtCore.pyqtSignal()
	getUnreadMessagesSignal = QtCore.pyqtSignal()
	showNotificationSignal = QtCore.pyqtSignal((QtCore.QString,),(QtCore.QString,QtCore.QString))
	passNotificationToQt = QtCore.pyqtSignal()
	passConfigToSettingsWindow = QtCore.pyqtSignal()
	passStartFetchingMessages = QtCore.pyqtSignal()
	passDoneFetchingMessages = QtCore.pyqtSignal()
	passUpdateMessageCount = QtCore.pyqtSignal(int)

	def __init__(self, parent=None):
		QtCore.QObject.__init__(self,parent)
		self.readSettingsSignal.connect(self.readSettings)
		self.getUnreadMessagesSignal.connect(self.getUnreadMessages)
		self.showNotificationSignal.connect(self.showNotification)

		timer = QtCore.QTimer(self)
		timer.timeout.connect(self.getUnreadMessages)
		timer.start(int(Common.interval) * 60 * 1000)

	def readSettings(self):
		parser = ConfigParser.SafeConfigParser()
		if parser.read([Common.rcFile]) != []:
			for k in self.account.keys():
				try:
					if k == "password":
						self.account[k] = base64.b64decode(parser.get('account',k))
					else:
						self.account[k] = parser.get('account',k)
				except ConfigParser.NoSectionError:
					self.passConfigToSettingsWindow.emit()
		else:
			self.passConfigToSettingsWindow.emit()

	def getUnreadMessages(self):
		self.passStartFetchingMessages.emit()
		thread.start_new_thread(self.tGetUnreadMessages,())

	def tGetUnreadMessages(self):
		self.readSettings()
		count = self.unreadMessagesCallback()
		self.passDoneFetchingMessages.emit()
		self.passUpdateMessageCount.emit(int(count))

	def unreadMessagesCallback(self):
		pass
		return 0

	def showNotification(self,message,title="New Message"):
		if not self.showDbusNotification(message,title):
			self.passNotificationToQt.emit()

	def showPynotifyNotification(self,message,title):
		try:
			import pynotify
			if pynotify.init(Common.appName):
				note = pynotify.Notification(str(title),str(message),Common.icon)
				note.show()
				return True
			else:
				return False
		except ImportError:
			return False

	def showDbusNotification(self,message,title):
		try:
			import dbus
			bus = dbus.SessionBus()
			noteObject = bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
			noteIface = dbus.Interface(noteObject, 'org.freedesktop.Notifications')
			noteIface.Notify(Common.appName,0,Common.icon,str(title),str(message),[],{},-1)
		except ImportError:
			return False