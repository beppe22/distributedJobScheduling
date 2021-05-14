from threading import Thread


class Updater(Thread):
    def __init__(self, owner):
        Thread.__init__(self)
        self.owner = owner
        self.update_port = None
        self.leader_ip = None
        self.leader_port = None

    def send_job_count(self, ):
        pass

    def update_th(self, ):
        pass

    def run(self):
        pass