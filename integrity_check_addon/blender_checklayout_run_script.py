import time
import re
import integrity_checker
from imp import reload

reload(integrity_checker)
ci = integrity_checker.check_file_integrity()

if __name__ == "__main__":
    ci.check_all()
