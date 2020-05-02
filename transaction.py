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
        if int(self.data[n]['transactionAmount']) <= 0:
            self.errorList.append("amount must be greater than 0.")
            
        now = datetime.now()
        dts = now.strftime("%d/%m/%Y %H:%M:%S")
        self.data[n]['transactionDate'] = str(now)
        
        if len(self.errorList) > 0:
            return False
        else:
            return True
            
    def addByDefault(self, transactionID, transactionType, transactionAmount, userID):
        t = transactionList()
        t.set('transactionID',transactionID)
        t.set('transactionType',transactionType)
        t.set('transactionAmount',transactionAmount)
        t.set('userID',userID)
        t.add()
        t.verifyNew()
        t.insert()

    
    
        