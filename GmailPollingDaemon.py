import PollingDaemon,imaplib

def stripTags(string):
	import re
	pattern = re.compile(r'<[^<]*?>')
	return pattern.sub('',string)

class GmailPollingDaemon(PollingDaemon.PollingDaemon):
	def unreadMessagesCallback(self):
		mail = imaplib.IMAP4_SSL("imap.gmail.com")
		count = 0

		try:
			mail.login(str(self.account['username']),str(self.account['password']))
			mail.select() # Defaults to 'INBOX'
			typ,data = mail.search(None, 'UNSEEN')
			for message in data[0].split():
				typ,data = mail.fetch(message, '(BODY.PEEK[HEADER.FIELDS (from)]<6.56> BODY.PEEK[HEADER.FIELDS (subject)]<9.56> BODY.PEEK[1]<0.200>)') # IMAP Magic
				msgString = "<b>Subject:</b> "+data[0][1].strip()+"\n"\
				+"<b>From:</b> "+data[1][1].strip()+"\n"+stripTags(data[2][1].decode("utf_8","ignore")).strip()
				self.showNotificationSignal.emit(msgString)
				count += 1
			mail.logout()
		except Exception as exception:
			print exception
			self.passConfigToSettingsWindow.emit()
		return count