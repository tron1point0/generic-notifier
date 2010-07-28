import sys
from PyQt4 import QtGui
import SysTrayIcon,SettingsWindow,PollingDaemon,Common

app = QtGui.QApplication(sys.argv)

poller = PollingDaemon.PollingDaemon()
settings = SettingsWindow.SettingsWindow(poller.account)
trayIcon = SysTrayIcon.SysTrayIcon(QtGui.QIcon(Common.icon), settings)

trayIcon.show()

trayIcon.quitSignal.connect(trayIcon.quit)
trayIcon.settingsSignal.connect(settings.show)
trayIcon.checkSignal.connect(poller.getUnreadMessages)
poller.passConfigToSettingsWindow.connect(settings.settingsFromPollingDaemon)
poller.passStartFetchingMessages.connect(trayIcon.throbberStartSignal)
poller.passDoneFetchingMessages.connect(trayIcon.throbberStopSignal)

poller.getUnreadMessages()

app.exec_()