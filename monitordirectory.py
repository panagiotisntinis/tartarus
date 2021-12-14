import time
import os
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

FORMAT = '%(asctime)s %(levelname)s  %(message)s'
logging.basicConfig(format=FORMAT)

class MonitorDirectory():
    abspaths = []
    observers = []
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    go_recursively = True

    def __init__(self, *args):
        self.findpaths(*args)
        self.my_event_handler = PatternMatchingEventHandler(self.patterns, self.ignore_patterns, self.ignore_directories, self.case_sensitive)
        self.my_event_handler.on_created = self.on_created
        self.my_event_handler.on_deleted = self.on_deleted
        self.my_event_handler.on_modified = self.on_modified
        self.my_event_handler.on_moved = self.on_moved

        for path in self.abspaths:
            msg = "Monitoring {:}".format(path)
            logging.info(msg)
            observer = Observer()
            observer.schedule(self.my_event_handler, path, recursive=self.go_recursively)
            self.observers.append(observer)

    def reset(self, *args):
        self.dirs = []
        self.stop()
        msg = "Reseting paths for monitoring"
        logging.critical(msg)
        self.findpaths(*args)
        self.run()

    def on_created(self, event):
        msg = "Created {:}".format(event.src_path)
        logging.warning(msg)
        if not event.is_directory:
            pass
            #checksum(event.src_path)

    def on_deleted(self, event):
        msg = "Deleted {:}".format(event.src_path)
        logging.warning(msg)

    def on_modified(self, event):
        msg = "Modified {:}".format(event.src_path)
        logging.warning(msg)
        if not event.is_directory:
            pass
            #checksum(event.src_path)

    def on_moved(self, event):
        msg = "Moved from {:} to {}".format(event.src_path, event.dest_path)
        logging.warning(msg)
        if not event.is_directory:
            pass
            #checksum(event.dest_path)

    def run(self):
        for observer in self.observers:
            observer.start()
            msg = "Start {:}".format(str(observer))
            logging.info(msg)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        msg = "Stop monitoring"
        logging.critical(msg)
        for observer in self.observers:
            msg = "Stop {:}".format(str(observer))
            logging.critical(msg)
            observer.unschedule_all()
            msg = "Stop {:}".format(str(observer))
            logging.critical(msg)
            observer.stop()
            msg = "Stop {:}".format(str(observer))
            logging.critical(msg)
            observer.join()
            msg = "Stop {:}".format(str(observer))
            logging.critical(msg)

    def findpaths(self, *args):
        for arg in args:
            msg = "Finding absolute path of {:}".format(arg)
            logging.info(msg)
            abspath = os.path.abspath(arg)
            msg = "Listing {:} for monitoring".format(abspath)
            logging.info(msg)
            self.abspaths.append(abspath)
        self.abspaths = list(set(self.abspaths))
        msg = "Removing duplicates"
        logging.info(msg)
        self.abspaths.sort()
        for i,j in enumerate(self.abspaths):
            try:
                if self.abspaths[i] in self.abspaths[i+1]:
                    del self.abspaths[i+1]
            except IndexError:
                pass
