import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Event(FileSystemEventHandler):
    def dispatch(self, event):
        print("in.csv was modified!")

if __name__ == "__main__":    
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, "in.csv", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()