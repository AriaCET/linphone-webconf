import os

class Linphone:
    def __init__(self):
        self.state = False
        try:
            self.start()
        except OSError:
            print "E: Cant spin up the daemon"
            exit()
    
    def start(self):
        if(not os.system("linphonecsh init")):
            print "Daemon inited"
        else:
            raise OSError
        self.enable_autoanswer()
        self.use_bcm_card()

    def register(self,host,username,password):
        try:
            if(not os.system("linphonecsh register --host "+host+" --username "+username+" --password "+password)):
                print  "I: Registred"
                return True
        except Error:
            print "E: Registration Unsuccessful"
            return False

    def enable_autoanswer(self):
        if(not os.system("linphonecsh generic 'autoanswer enable'")):
            return True
        return False

    def use_bcm_card(self):
        if(not os.system("linphonecsh soundcard ring 2")):
            if(not os.system("linphonecsh soundcard playback 2")):
                return True
        return False

    def stop(self):
        os.system("linphonecsh exit")
    
    def __del__(self):
        self.stop
        
