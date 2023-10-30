from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def create_observer(filename, fun):

    class Event(FileSystemEventHandler):
        def dispatch(self, event):            
            fun(event)
            
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, filename, recursive=True)
    observer.start()
    return observer