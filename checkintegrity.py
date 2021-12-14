import hashlib
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class CheckIntegrity():

    def __init__(self,filename):
        self.filename = filename

    def run(self):
        sha256_hash = hashlib.sha256()
        file = open(self.filename, 'rb')
        content = file.read()
        sha256_hash.update(content)
        self.digest = sha256_hash.hexdigest()
        file.close()

    def __str__(self):
        return self.digest

##DEBUG
check_integrity = CheckIntegrity("main.py")
check_integrity.run()
print(check_integrity)
