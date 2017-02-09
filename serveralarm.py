import paramiko
import time
import socket
import sys

class ServerAlarm(object):
	"""docstring for ServerAlarm"""
	def __init__(self):
		super(ServerAlarm, self).__init__()
		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
		self.chan = None
		self.error = 'No error founds while connecting'
		print self.error

	def connect(self, ip, uname, pw):
		try:
			self.client.connect(ip, username=uname, password=pw)
			self.chan = self.client.invoke_shell()
			print "successfull connected to %s"%ip
			self.chan.settimeout(5.0)
			self.error = 'No error founds while connecting'
			return True
		except Exception, e:
			self.error = e
			self.chan = None
			return False

	def getfeedback(self, regcode = ']$'):
		try:
			print time.strftime("%Y-%m-%d %H:%M:%S"), ": waiting for reply until timeout..."
			buff = ''
			while buff.find(regcode) == -1:
				resp = self.chan.recv(9999999)
				buff += resp
			print buff
			return buff
		except socket.timeout:
			print time.strftime("%Y-%m-%d %H:%M:%S"), "Time out while waiting for response from server. Program will exits."
			sys.exit(1)
		except Exception as e:
			print e
			sys.exit(1)



	def __del__(self):
		self.client.close()

	def  getdiskspace(self):
		if self.chan is not None:
			self.getfeedback()
			print "begin get disk space ..."
			self.chan.send("df -h\n")
			r1 = self.getfeedback()
			self.chan.send("exit\n")
			return "<pre>" + str(r1) + "</pre>"
		else:
			return "Unable to accomply because channel is NULL"

	def getasmspace(self):
		if self.chan is not None:
			# self.getfeedback()
			print "begin get asm space ..."
			self.chan.send("su - oracle\n")
			self.getfeedback("]$")
			self.chan.send(". oraenv\n")
			self.getfeedback("] ?")
			self.chan.send("+ASM1\n")
			self.getfeedback("]$")
			self.chan.send("asmcmd\n")
			self.getfeedback("ASMCMD>")
			self.chan.send("lsdg\n")
			r1 = self.getfeedback("ASMCMD>")
			self.chan.send("exit\n")
			self.chan.send("exit\n")
			#self.chan.send("exit\n")
			return "<pre>" + r1 + "</pre>"

if __name__ == '__main__':
	srv = ServerAlarm()
	srv.connect('192.168.1.1', 'khanhnn', '123456')
	abc = srv.getdiskspace()
	print abc
	# print abc.split('\r\n')
	# print str(srv.error)
	# timeout = time.time() + 5
	# while 1 and (time.time() <= timeout):
	# 	print "."
	# 	time.sleep(2)
