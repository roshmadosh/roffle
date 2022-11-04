import datetime
from enum import Enum

# for coloring console output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ColorStatus(Enum):
    SUCCESS = 'success',
    INFO = 'info',
    ERROR = 'error'

def console_logger(message: str, status = ColorStatus.INFO) -> None:
    color = bcolors.WARNING

    if status is ColorStatus.ERROR:
        color = bcolors.FAIL
    elif status is ColorStatus.SUCCESS:
        color = bcolors.OKGREEN
    else:
        color = bcolors.WARNING
    
    print(f"{color}{datetime.datetime.now()}: {message}{bcolors.ENDC}")