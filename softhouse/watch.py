import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def create_observer(filename, fun):
    """
    Creates an observer which watches for changes in directory of `filename` 
    and runs the function `fun` whenever an update is detected.
    """    

    logging.debug("Creating watchdog observer")

    class Event(FileSystemEventHandler):
        def dispatch(self, event):            
            fun(event)
            
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, filename, recursive=True)
    observer.start()
    return observer