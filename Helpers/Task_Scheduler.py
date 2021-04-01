"""  Module Task_Scheduler.py
module who contains the class Task_scheduler
"""
import threading


class Task_Scheduler(threading.Thread):
    """
          Class to create a thread who run a given task at a given interval with args

            contains a function run and stop to run or stop the task

            :param interval: timedelta
            :param execute: function to execute
            :param args: args to pass in the execute function

    """

    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        """
                function to stop running the execute function
                :Example:

                >>> Task_Scheduler.stop()
        """
        self.stopped.set()
        self.join()

    def run(self):
        """
            function to run the execute function
            :Example:

            >>> Task_Scheduler.run()
        """
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)
