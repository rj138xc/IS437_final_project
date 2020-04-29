import pymysql
from baseObject import baseObject
class userList(baseObject):
    def __init__(self):
        self.setupObject('users')
        
    def verifyNew(self,n=0):
        self.errorList = []
        
        if len(self.data[n]['userFName']) == 0:
            self.errorList.append("First name cannot be blank.")
        if len(self.data[n]['userLName']) == 0:
            self.errorList.append("Last name cannot be blank.")
        if len(self.data[n]['userEmail']) == '':
            self.errorList.append("email cannot be blank.")
        if len(self.data[n]['userPassword']) < 6:
            self.errorList.append("Username must contain at least 6 characters.")
        #TODO
        #Add if statements for validation of other fields
  
        if len(self.errorList) > 0:
            return False
        else:
            return True
    def tryLogin(self,email,pw):    
        #SELECT * FROM `customers` WHERE `email` = 'b@a.com' AND `password` = '123'
        sql = 'SELECT * FROM `' + self.tn + '` WHERE `userEmail` = %s AND `userPassword` = %s;'
        tokens = (email,pw)
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #print(sql)
        #print(tokens)
        cur.execute(sql,tokens)
        self.data = []
        n=0
        for row in cur:
            self.data.append(row)
            n+=1
        if n > 0:
            return True
        else:
            return False
    
    
    
    
    
    
    
    
    
    
        