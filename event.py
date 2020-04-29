import pymysql
from datetime import datetime
from baseObject import baseObject
class eventList(baseObject):
    def __init__(self):
        self.setupObject('events')
        
    def verifyNew(self,n=0):
        self.errorList = []
        
        if len(self.data[n]['eventName']) == 0:
            self.errorList.append("name cannot be blank.")
        if len(self.data[n]['eventType']) == 0:
            self.errorList.append("Type cannot be blank.")
            
        #Add if statements for validation of other fields
        #age maybe
        
        now = datetime.now()
        dts = now.strftime("%d/%m/%Y %H:%M:%S")
        self.data[n]['eventScheduleDate'] = str(now)
  
        if len(self.errorList) > 0:
            return False
        else:
            return True
   