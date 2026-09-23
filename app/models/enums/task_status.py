from enum import Enum

class TaskStatus(str, Enum):
    PROGRES = 'PROGRES'
    FINISHED = 'FINISHED' 
    OVERDUE = 'OVERDUE'