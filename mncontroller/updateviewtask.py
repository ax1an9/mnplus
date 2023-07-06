import sched
import time
import threading

class ViewUpdater(threading.Thread):
    def __init__(self,netview):
        super().__init__()
        self.netview=netview
        self._stop_event = threading.Event()

    def run(self):
        """
        更新任务
        """
        while not self._stop_event.is_set():
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),"update net top view...")
            self.task()
            time.sleep(5)

    def stop(self):
        self._stop_event.set()
    def task(self):
        self.netview.all_update()

