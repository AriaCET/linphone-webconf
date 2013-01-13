#!/usr/bin/python2
import subprocess

class pjsua(object):
	def __init__(self,logfile=None):
			super(pjsua, self).__init__()
			self.process=None
			self.logfile=logfile
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
		if self.process == None:
			return
		pid = self.process.pid
		print ("stoping pjsua:" + str(pid))
		(stdoutdata, stderrdata) = self.process.communicate('q')
		self.printlog(stdoutdata)
		self.process =None

	def printlog(self,log):
		if self.logfile == None:
			return
		out = open(self.logfile,"a")
		out.write("\n\n")
		out.write(log)
		out.close()


	def restart(self):
		print ("pjsua restarting..")
		self.stop()
		self.start()

	def __del__(self):
		self.stop()
		
