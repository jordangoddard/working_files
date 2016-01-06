__author__ = 'Jeff.Bell'

## Module for printing and logging for Snapshot
#
# @todo set global for log that can be turned on to log all info, error,
# and warning printing

import os
import inspect

class Log(object):
    class __Log:
        """
        Singleton
        """
        def __init__(self, log_path="C:/temp/snapshot_logs/", log_to_file=False):
            self.log_path = log_path
            self.log_name = None
            #print("Log to file: %s" % log_to_file)
            self.log_to_file = log_to_file
            self._setup()

        def info(self, text, message="   INFO"):
            print("%s: %s" % (message, text))
            if self.log_to_file:
                logf = open("%s/%s" % (self.log_path, self.log_name), "a")
                logf.write("%s: %s\n" % (message, text))
                logf.close()

        def warning(self, text, message="WARNING"):
            self.info(message=message, text=text)

        def error(self, text, message="  ERROR"):
            self.info(message=message, text=text)

        def _setup(self):
            import os
            import datetime
            # Make sure the output path exists
            #print("Log path: %s" % self.log_path)
            if not os.path.exists(self.log_path):
                try:
                    os.makedirs(self.log_path, 0x0777)
                except:
                    print("ERROR: can't create log path %s" % self.log_path)
            self.log_name = "%s_%s.log" % ("date_time", "user.name")
            #self.log_name = "%s_%s.log" % (datetime.datetime.time(), "user.name")

    instance = None
    def __new__(cls, *args, **kwargs): # __new__ always a classmethod
        if not Log.instance:
            Log.instance = Log.__Log(*args, **kwargs)
        else:
            Log.instance.__init__(*args, **kwargs)
        return Log.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)