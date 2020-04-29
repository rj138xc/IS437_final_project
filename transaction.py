import pymysql
from datetime import datetime
from baseObject import baseObject
class transactionList(baseObject):
    def __init__(self):
        self.setupObject('transactions')
        
    def verifyNew(self,n=0):
        self.errorList = []
        
        if len(self.data[n]['transactionType']) == 0:
            self.errorList.append("Must pick a type.")
        if len(self.data[n]['transactionAmount']) == 0:
            self.errorList.append("amount cannot be blank.")
            
        now = datetime.now()
        dts = now.strftime("%d/%m/%Y %H:%M:%S")
        self.data[n]['transactionDate'] = str(now)
        
        if len(self.errorList) > 0:
            return False
        else:
            return True

    
    
        