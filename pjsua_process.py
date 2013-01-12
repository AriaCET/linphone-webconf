#!/usr/bin/python2
import subprocess

class pjsua(object):
	def __init__(self):
			super(pjsua, self).__init__()
			self.process=None
			self.start()

	def start(self):
		import shlex
		if not self.process == None:
			self.stop()
		args = shlex.split("pjsua --config-file pjsua.cfg")
		self.process = subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		if self.process.pid == 0:
			return False
		else :
			print ("pjsua started:" +str(self.process.pid))
			return True

	def stop(self):
		print ("stoping pjsua:" + str(self.process.pid))
		(stdoutdata, stderrdata) = self.process.communicate('q')
		self.process =None

	def restart(self):
		print ("pjsua restarting..")
		self.stop()
		self.start()

	def __del__(self):
		self.stop()
		
