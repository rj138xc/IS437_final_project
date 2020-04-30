import pymysql
from baseObject import baseObject
class animalList(baseObject):
    def __init__(self):
        self.setupObject('animals')
        
    def verifyNew(self,n=0):
        self.errorList = []
        
        if len(self.data[n]['animalName']) == 0:
            self.errorList.append("name cannot be blank.")
        if len(self.data[n]['animalType']) == 0:
            self.errorList.append("Type cannot be blank.")
            
        #Add if statements for validation of other fields
        #age maybe
  
        if len(self.errorList) > 0:
            return False
        else:
            return True