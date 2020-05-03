from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 
from customer import customerList
from user import userList
from animal import animalList
from event import eventList
from transaction import transactionList
import pymysql,json,time

from flask_session import Session  #serverside sessions

app = Flask(__name__,static_url_path='')

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/set')
def set():
    session['time'] = time.time()
    return 'set'
    
@app.route('/get')
def get():
    return str(session['time'])

@app.route('/')
def home():
    return render_template('test.html', title='Test2', msg='Welcome!')
  
'''
======================================================================
START CUSTOMER PAGES 
======================================================================
'''  
@app.route('/customers')
def customers():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
    c = customerList()
    c.getAll()
    
    print(c.data)
    #return ''
    return render_template('customer/customers.html', title='Customer List',  customers=c.data)
    
@app.route('/customer')
def customer():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
    
    c = customerList()
    if request.args.get(c.pk) is None:
        return render_template('error.html', msg='No customer id given.')  

    c.getById(request.args.get(c.pk))
    if len(c.data) <= 0:
        return render_template('error.html', msg='Customer not found.')  
    
    print(c.data)
    return render_template('customer/customer.html', title='Customer ',  customer=c.data[0])  
    
@app.route('/newcustomer',methods = ['GET', 'POST'])
def newcustomer():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    if request.form.get('fname') is None:
        c = customerList()
        c.set('fname','')
        c.set('lname','')
        c.set('email','')
        c.set('password','')
        c.set('subscribed','')
        c.add()
        return render_template('customer/newcustomer.html', title='New Customer',  customer=c.data[0]) 
    else:
        c = customerList()
        c.set('fname',request.form.get('fname'))
        c.set('lname',request.form.get('lname'))
        c.set('email',request.form.get('email'))
        c.set('password',request.form.get('password'))
        c.set('subscribed',request.form.get('subscribed'))
        c.add()
        if c.verifyNew():
            c.insert()
            print(c.data)
            return render_template('customer/savedcustomer.html', title='Customer Saved',  customer=c.data[0])
        else:
            return render_template('customer/newcustomer.html', title='Customer Not Saved',  customer=c.data[0],msg=c.errorList)
            
@app.route('/savecustomer',methods = ['GET', 'POST'])
def savecustomer():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    c = customerList()
    c.set('id',request.form.get('id'))
    c.set('fname',request.form.get('fname'))
    c.set('lname',request.form.get('lname'))
    c.set('email',request.form.get('email'))
    c.set('password',request.form.get('password'))
    c.set('subscribed',request.form.get('subscribed'))
    c.add()
    if c.verifyNew():
        c.update()
        print(c.data)
        return render_template('customer/savedcustomer.html', title='Customer Saved',  customer=c.data[0])
    else:
        return render_template('customer/newcustomer.html', title='Customer Not Saved',  customer=c.data[0],msg=c.errorList)
    print(c.data)
    #return ''
    return render_template('customer/savedcustomer.html', title='Customer Saved',  customer=c.data[0])
'''
======================================================================
END CUSTOMER PAGES 
======================================================================
'''   
'''
======================================================================
START USER PAGES
======================================================================
'''

@app.route('/users')
def users():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    u = userList()
    u.getAll()
    
    print(u.data)
    #return ''
    return render_template('user/users.html', title='User List',  users=u.data)
    
@app.route('/user')
def user():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    u = userList()
    if request.args.get(u.pk) is None:
        return render_template('error.html', msg='No user id given.')  

    u.getById(request.args.get(u.pk))
    if len(u.data) <= 0:
        return render_template('error.html', msg='User not found.')  
    
    print(u.data)
    return render_template('user/user.html', title='User ',  user=u.data[0])  

@app.route('/newuser',methods = ['GET', 'POST'])
def newuser():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    if request.form.get('userFName') is None:
        u = userList()
        u.set('userFName','')
        u.set('userLName','')
        u.set('userEmail','')
        u.set('userPassword','')
        u.set('userType','')
        u.add()
        return render_template('user/newuser.html', title='New User',  user=u.data[0]) 
    else:
        u = userList()
        u.set('userFName',request.form.get('userFName'))
        u.set('userLName',request.form.get('userLName'))
        u.set('userEmail',request.form.get('userEmail'))
        u.set('userPassword',request.form.get('userPassword'))
        u.set('userType',request.form.get('userType'))
        u.add()
        if u.verifyNew():
            u.insert()
            print(u.data)
            return render_template('user/saveduser.html', title='User Saved',  user=u.data[0])
        else:
            return render_template('user/newuser.html', title='User Not Saved',  user=u.data[0],msg=u.errorList)
 
@app.route('/newusercustomer',methods = ['GET', 'POST']) 
def newusercustomer():
#customer facing
    if request.form.get('userFName') is None:
        u = userList()
        u.set('userFName','')
        u.set('userLName','')
        u.set('userEmail','')
        u.set('userPassword','')
        u.set('userType','')
        u.add()
        return render_template('user/newusercustomer.html', title='New User',  user=u.data[0]) 
    else:
        u = userList()
        u.set('userFName',request.form.get('userFName'))
        u.set('userLName',request.form.get('userLName'))
        u.set('userEmail',request.form.get('userEmail'))
        u.set('userPassword',request.form.get('userPassword'))
        u.set('userType','customer')
        u.add()
        
        
        if u.verifyNew():
            u.insert()
            print(u.data)
            return render_template('user/saveduser.html', title='User Saved',  user=u.data[0])
        else:
            return render_template('user/newusercustomer.html', title='User Not Saved',  user=u.data[0],msg=u.errorList)
            
@app.route('/saveuser',methods = ['GET', 'POST'])
def saveuser():
#customer facing
    u = userList()
    u.set('userID',request.form.get('userID'))
    u.set('userFName',request.form.get('userFName'))
    u.set('userLName',request.form.get('userLName'))
    u.set('userEmail',request.form.get('userEmail'))
    u.set('userPassword',request.form.get('userPassword'))
    u.set('userType',request.form.get('userType'))
    u.add()
    if u.verifyNew():
        u.update()
        print(u.data)
        return render_template('user/saveduser.html', title='User Saved',  user=u.data[0])
    else:
        return render_template('user/newuser.html', title='User Not Saved',  user=u.data[0],msg=u.errorList)

'''
======================================================================
END USER PAGES 
======================================================================
'''    
'''
======================================================================
START ANIMAL PAGES
======================================================================
'''

@app.route('/animals')
def animals():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    a = animalList()
    a.getAll()
    
    print(a.data)
    #return ''
    return render_template('animal/animals.html', title='Animal List',  animals=a.data)
    
@app.route('/animal')
def animal():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    u = userList()
    u.getAll()
    
    a = animalList()
    if request.args.get(a.pk) is None:
        return render_template('error.html', msg='No animal id given.')  

    a.getById(request.args.get(a.pk))
    if len(a.data) <= 0:
        return render_template('error.html', msg='Animal not found.')  
    
    print(a.data)
    return render_template('animal/animal.html', title='Animal',  animal=a.data[0], users = u.data)
    
@app.route('/newanimal',methods = ['GET', 'POST'])
def newanimal():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    u = userList()
    u.getAll()
        
    if request.form.get('animalName') is None:
        a = animalList()
        a.set('animalName','')
        a.set('animalType','')
        a.set('animalBreed','')
        a.set('animalAge','')
        a.set('animalGender','')
        a.set('animalSize','')
        a.set('animalPhoto','')
        a.set('animalStatus','')
        a.set('userID','')
        a.add()
        return render_template('animal/newanimal.html', title='New Animal',  animal=a.data[0], users=u.data) 
    else:
        a = animalList()
        a.set('animalName',request.form.get('animalName'))
        a.set('animalType',request.form.get('animalType'))
        a.set('animalBreed',request.form.get('animalBreed'))
        a.set('animalAge',request.form.get('animalAge'))
        a.set('animalGender',request.form.get('animalGender'))
        a.set('animalSize',request.form.get('animalSize'))
        a.set('animalPhoto',request.form.get('animalPhoto'))
        a.set('animalStatus',request.form.get('animalStatus'))
        a.set('userID',request.form.get('userID'))
        
        if request.form.get('animalPhoto') == '':
            a.set('animalPhoto','noPhoto.jpg')
        
        a.add()
        if a.verifyNew():
            a.insert()
            print(a.data)
            return render_template('animal/savedanimal.html', title='Animal Saved',  animal=a.data[0], users=u.data)
        else:
            return render_template('animal/newanimal.html', title='Animal Not Saved',  animal=a.data[0],msg=a.errorList, users=u.data)
            
@app.route('/adoptable')
def adoptable():
#customer facing
    a = animalList()
    animalType = ''
    animalType = request.args.get('animalType', animalType)
    if animalType is None or animalType == '':
        a.getByField('animalStatus','available')
        return render_template('animal/adoptable.html', title='Adoptable Animals',  animals=a.data, type='Animal') 
    else:
        a.getByFields('animalType',animalType,'animalStatus','available')
        return render_template('animal/adoptable.html', title='Adoptable Animals',  animals=a.data, type=animalType) 
        
    return render_template('animal/adoptable.html', title='Adoptable Animals',  animals=a.data)
    
            
@app.route('/saveanimal',methods = ['GET', 'POST'])
def saveanimal():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    a = animalList()
    a.set('animalID',request.form.get('animalID'))
    a.set('animalName',request.form.get('animalName'))
    a.set('animalType',request.form.get('animalType'))
    a.set('animalBreed',request.form.get('animalBreed'))
    a.set('animalAge',request.form.get('animalAge'))
    a.set('animalGender',request.form.get('animalGender'))
    a.set('animalSize',request.form.get('animalSize'))
    a.set('animalPhoto',request.form.get('animalPhoto'))
    a.set('animalStatus',request.form.get('animalStatus'))
    a.set('userID',request.form.get('userID'))
    
    if request.form.get('animalPhoto') == '':
            a.set('animalPhoto','noPhoto.jpg')
            
    a.add()
    print('00000000000 saveanimal animal age: ' , a.data[0]['animalAge'])
    if a.verifyNew():
        a.update()
        print(a.data)
        return render_template('animal/savedanimal.html', title='Animal Saved',  animal=a.data[0])
    else:
        return render_template('animal/newanimal.html', title='Animal Not Saved',  animal=a.data[0], msg=a.errorList)
        
        
@app.route('/pickanimaltype',methods = ['GET','POST'])
def pickanimaltype():
    #customer facing
    return render_template('animal/pickanimaltype.html', title='Adoption')

@app.route('/viewanimal')
def viewanimal():
    #customer facing
    a = animalList()
    if request.args.get(a.pk) is None:
        return render_template('error.html', msg='No animal id given.')  

    a.getById(request.args.get(a.pk))
    if len(a.data) <= 0:
        return render_template('error.html', msg='Animal not found.')  
    
    print(a.data)
    return render_template('animal/viewanimal.html', title='Animal',  animal=a.data[0])
    
  
'''
======================================================================
END ANIMAL PAGES 
======================================================================
'''
'''
======================================================================
START TRANSACTION PAGES
======================================================================
'''

@app.route('/transactions')
def transactions():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    t = transactionList()
    t.getAll()
    
    #print(t.data)
    return render_template('transaction/transactions.html', title='Transaction List',  transactions=t.data)
    
@app.route('/transaction')
def transaction():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    u=userList()
    u.getAll()
        
    t = transactionList()
    if request.args.get(t.pk) is None:
        return render_template('error.html', msg='No transaction id given.')  

    t.getById(request.args.get(t.pk))
    if len(t.data) <= 0:
        return render_template('error.html', msg='Transaction not found.')  
    
    #print(t.data)
    return render_template('transaction/transaction.html', title='Transaction Details',  transaction=t.data[0], users=u.data)
    
@app.route('/newtransaction',methods = ['GET', 'POST'])
def newtransaction():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    u=userList()
    u.getAll()
        
    if request.form.get('transactionType') is None:
        t = transactionList()
        t.set('transactionDate','')
        t.set('transactionType','')
        t.set('transactionAmount','')
        t.set('userID','')
        t.add()
        return render_template('transaction/newtransaction.html', title='New Transaction',  transaction=t.data[0], users=u.data) 
    else:
        t = transactionList()
        t.set('transactionID',request.form.get('transactionID'))
        t.set('transactionDate',request.form.get('transactionDate'))
        t.set('transactionType',request.form.get('transactionType'))
        t.set('transactionAmount',request.form.get('transactionAmount'))
        t.set('userID',request.form.get('userID'))
        t.add()
        
        if t.verifyNew():
            t.insert()
            #print(t.data)
            return render_template('transaction/savedtransaction.html', title='Transaction Saved',  transaction=t.data[0])
        else:
            return render_template('transaction/newtransaction.html', title='Transaction Not Saved',  transaction=t.data[0] ,msg=t.errorList, users=u.data)
            
@app.route('/newdonation',methods = ['GET', 'POST'])
def newdonation():
#customer facing, must be logged in user
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')

    if request.form.get('transactionAmount') is None:
        t = transactionList()
        t.set('transactionDate','')
        t.set('transactionType','')
        t.set('transactionAmount','')
        t.set('userID','')
        t.add()
        return render_template('transaction/newdonation.html', title='New Donation',  transaction=t.data[0]) 
    else:
        t = transactionList()
        t.set('transactionID',request.form.get('transactionID'))
        t.set('transactionType',request.form.get('transactionType'))
        t.set('transactionAmount',request.form.get('transactionAmount'))
        t.set('userID',session['user']['userID'])
        t.add()
        
        if t.verifyNew():
            t.insert()
            #print(t.data)
            return render_template('transaction/saveddonation.html', title='Donation Successful',  transaction=t.data[0])
        else:
            return render_template('transaction/newdonation.html', title='Donation Unsuccessful',  transaction=t.data[0],msg=t.errorList)
    
@app.route('/newadoptiontransaction',methods = ['GET', 'POST'])
def newadoptiontransaction():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    print(request.args.getlist('param'))
        
    a = animalList()
    animalID = ''
    animalID = request.args.get('animalID')
    a.getById(animalID)

    if len(a.data) <= 0:
        return render_template('error.html', msg='Animal not found.')  
    
    adoptionFee = 0
    if a.data[0]['animalType'] == 'Dog':
        adoptionFee = 150
    elif a.data[0]['animalType'] == 'Cat':
        adoptionFee = 50
    
    if request.form.get('transactionType') is None:
        t = transactionList()
        t.set('transactionDate','')
        t.set('transactionType','')
        t.set('transactionAmount','')
        t.set('userID','')
        t.add()
        return render_template('transaction/newadoptiontransaction.html', title='New Adoption Transaction',  transaction=t.data[0], animal=a.data[0], fee=adoptionFee) 
    else:
        t = transactionList()
        t.set('transactionID',request.form.get('transactionID'))
        t.set('transactionType',request.form.get('transactionType'))
        t.set('transactionAmount',request.form.get('transactionAmount'))
        t.set('userID',session['user']['userID'])
        t.add()
        
        if t.verifyNew():
            t.insert()
            #print(t.data)
            return render_template('event/adoptionevent.html', title='Adoption Transaction Saved',  transaction=t.data[0], animal=a.data[0], fee=adoptionFee)
        else:
            return render_template('transaction/newadoptiontransaction.html', title='Adoption Transaction Not Saved',  transaction=t.data[0] ,msg=t.errorList, animal=a.data[0], fee=adoptionFee)

@app.route('/savedonation',methods = ['GET', 'POST'])
def savedonation():
#customer facing
    t = transactionList()
    t.set('transactionID',request.form.get('transactionID'))
    t.set('transactionType',request.form.get('transactionType'))
    t.set('transactionAmount',request.form.get('transactionAmount'))
    t.set('userID',session['user']['userID'])
    t.add()
    
    if t.verifyNew():
        t.update()
        print("after update",t.data)
        return render_template('transaction/saveddonation.html', title='Donation successful',  transaction=t.data[0])
    else:
        return render_template('transaction/newdonation.html', title='Donation unsuccessful',  transaction=t.data[0],msg=t.errorList)
            
@app.route('/savetransaction',methods = ['GET', 'POST'])
def savetransaction():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    t = transactionList()
    t.set('transactionID',request.form.get('transactionID'))
    t.set('transactionType',request.form.get('transactionType'))
    t.set('transactionAmount',request.form.get('transactionAmount'))
    t.set('userID',session['user']['userID'])
    t.add()
    
    if t.verifyNew():
        t.update()
        print("after update",t.data)
        return render_template('transaction/savedtransaction.html', title='Transaction Saved',  transaction=t.data[0])
    else:
        return render_template('transaction/newtransaction.html', title='Transaction Not Saved',  transaction=t.data[0],msg=t.errorList)
    

'''
======================================================================
END TRANSACTION PAGES 
======================================================================
'''
'''
======================================================================
START EVENT PAGES
======================================================================
'''

@app.route('/events')
def events():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    e = eventList()
    e.getAll()
    
    #print(e.data)
    return render_template('event/events.html', title='Event List',  events=e.data)
    
@app.route('/event')
def event():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    allAnimals = animalList()
    allAnimals.getAll()
        
    e = eventList()
    if request.args.get(e.pk) is None:
        return render_template('error.html', msg='No event id given.')  

    e.getById(request.args.get(e.pk))
    if len(e.data) <= 0:
        return render_template('error.html', msg='Event not found.')  
    
    #print(e.data)
    return render_template('event/event.html', title='Event Details',  event=e.data[0], al = allAnimals.data)
    
@app.route('/newevent',methods = ['GET', 'POST'])
def newevent():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    #elif session['user']['userType'] == 'customer':
    #    return redirect('login')
    
        
    if request.form.get('eventType') is None:
        t = transactionList()
        t.set('transactionType','')
        t.set('transactionAmount','')
        t.set('userID','')
        t.add()
    
        e = eventList()
        e.set('eventType','')
        e.set('eventScheduleDate','')
        e.set('eventCompletedDate','')
        e.set('eventName','')
        e.set('eventResult','')
        e.set('animalID','')
        e.set('userID','')
        e.set('transactionID','')
        e.add()
        
        allAnimals = animalList()
        allAnimals.getAll()
        return render_template('event/newevent.html', title='New Event',  event=e.data[0], al = allAnimals.data) 
    else:
        t = transactionList()
        t.set('transactionType',request.form.get('eventType'))
        t.set('transactionAmount',0)
        t.set('userID',session['user']['userID'])
        t.add()
        
        e = eventList()
        e.set('eventID',request.form.get('eventID'))
        e.set('eventType',request.form.get('eventType'))
        e.set('eventCompletedDate',request.form.get('eventCompletedDate'))
        e.set('eventName',request.form.get('eventName'))
        e.set('eventResult',request.form.get('eventResult'))
        e.set('animalID',request.form.get('animalID'))
        e.set('userID',session['user']['userID'])
        #e.set('transactionID',request.form.get('transactionID'))
       
        e.add()
        if e.verifyNew():
            t.verifyNew()
            t.insert()
            
            e.set('transactionID',t.data[0]['transactionID'])
            e.add()
            e.insert()
            
            #print('eventdata:',e.data)
            #print('transactiondata:',t.data)
            return render_template('event/savedevent.html', title='event Saved',  event=e.data[0])
        else:
            return render_template('event/newevent.html', title='event Not Saved',  event=e.data[0],msg=e.errorList)
            
@app.route('/newappointment',methods = ['GET', 'POST'])
def newappointment():
#customer facing
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    
    userID = session['user']['userID']
    animals = animalList()
    animals.getByField('userID',str(userID))
        
    if request.form.get('eventType') is None:
        t = transactionList()
        t.set('transactionType','')
        t.set('transactionAmount','')
        t.set('userID','')
        t.add()
    
        e = eventList()
        e.set('eventType','')
        e.set('eventScheduleDate','')
        e.set('eventCompletedDate','')
        e.set('eventName','')
        e.set('eventResult','')
        e.set('animalID','')
        e.set('userID','')
        e.set('transactionID','')
        e.add()
        
        allAnimals = animalList()
        allAnimals.getAll()
        return render_template('event/newappointment.html', title='New Event',  event=e.data[0], animals=animals.data, user=session['user']['userFName']) 
    else:
        t = transactionList()
        t.set('transactionType',request.form.get('eventType'))
        t.set('transactionAmount',0)
        t.set('userID',session['user']['userID'])
        t.add()
        
        e = eventList()
        e.set('eventID',request.form.get('eventID'))
        e.set('eventType',request.form.get('eventType'))
        e.set('eventCompletedDate',request.form.get('eventCompletedDate'))
        e.set('eventName',request.form.get('eventName'))
        e.set('eventResult',request.form.get('eventResult'))
        e.set('animalID',request.form.get('animalID'))
        e.set('userID',session['user']['userID'])
        #e.set('transactionID',request.form.get('transactionID'))
       
        e.add()
        if e.verifyNew():
            t.verifyNew()
            t.insert()
            
            e.set('transactionID',t.data[0]['transactionID'])
            e.add()
            e.insert()
            
            #print('eventdata:',e.data)
            #print('transactiondata:',t.data)
            return render_template('event/savedappointment.html', title='event Saved',  event=e.data[0])
        else:
            return render_template('event/newappointment.html', title='event Not Saved',  event=e.data[0],msg=e.errorList, user=session['user']['userFName'], animals=animals.data)

            
@app.route('/adoptionevent',methods = ['GET', 'POST'])    
def adoptionevent():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
        
    an = animalList()
    animalID = ''
    animalID = request.args.get('animalID')
    an.getById(animalID)
    #print('a.data before :', an.data[0]) 
    #print('USER:',session['user']['userID'])
    if session['user']['userID'] <= 0:
        return redirect('login')
    an.data[0]['animalStatus'] = 'Adopted'
    an.data[0]['userID'] = session['user']['userID']
    an.add()
    #print('an.data[0][animalStatus]', an.data[0]['animalStatus'])    
    '''
    a.set('animalStatus','Adopted')
    a.set('userID',session['user']['userID'])
    a.add()
    '''
    #print('a.data after :', an.data[0])
    an.update()

    if len(an.data) <= 0:
        return render_template('error.html', msg='Animal not found.')  

        
    t = transactionList()
    transactionID = ''
    transactionID = request.args.get('transactionID')
    t.getById(transactionID)

    if len(t.data) <= 0:
        return render_template('error.html', msg='Transaction not found.')  

        
    e = eventList()
    e.set('eventType','Adoption')
    e.set('eventCompletedDate','n/a')
    e.set('eventName','Adoption of '+an.data[0]['animalName'])
    e.set('eventResult','n/a')
    e.set('animalID',an.data[0]['animalID'])
    e.set('userID',session['user']['userID'])
    e.set('transactionID',transactionID)
   
    e.add()
    if e.verifyNew():
        e.insert()
        print(e.data)
        return render_template('event/adoptionsuccessful.html', title='event Saved',  event=e.data[0])
    else:
        return render_template('event/adoptionevent.html', title='event Not Saved',  event=e.data[0],msg=e.errorList)

@app.route('/adoptionSuccessful',methods = ['GET', 'POST'])
def adoptionSuccessful():
#cusomter facing
    e = eventList()
    
    return render_template('event/adoptionsuccessful.html', title='event Saved',  event=e.data[0])
    
                    
@app.route('/saveevent',methods = ['GET', 'POST'])
def saveevent():
#TODO unsure
    e = eventList()
    e.set('eventID',request.form.get('eventID'))
    e.set('eventType',request.form.get('eventType'))
    e.set('eventCompletedDate',request.form.get('eventCompletedDate'))
    e.set('eventName',request.form.get('eventName'))
    e.set('eventResult',request.form.get('eventResult'))
    e.set('animalID',request.form.get('animalID'))
    e.set('userID',session['user']['userID'])
    e.set('transactionID',request.form.get('transactionID'))
       
    e.add()
    if e.verifyNew():
        e.update()
        print(e.data)
        return render_template('event/savedevent.html', title='event Saved',  event=e.data[0])
    else:
        return render_template('event/newevent.html', title='event Not Saved',  event=e.data[0],msg=e.errorList)
    
''' 
======================================================================
END EVENT PAGES 
======================================================================
'''
    
@app.route('/login', methods = ['GET','POST'])	
def login():	
    #check login	
    #set session	
    #redirect to menu	
    #check session on login pages	
    if request.form.get('email') is not None and request.form.get('password') is not None:	
        u = userList()	
        if u.tryLogin(request.form.get('email'),request.form.get('password')):	
            print('login successful')	
            session['user'] = u.data[0]	
            session['active'] = time.time()	
            if session['user']['userType'] == 'customer':
                return redirect('main')	
            elif session['user']['userType'] == 'employee':
                return redirect('mainadmin')	
        else:  	
            print('login failed')	
            return render_template('login.html', title='Login', msg='Incorrect credentials')	
    else:	
        if 'msg' not in session.keys() or session['msg'] is None:	
            m = 'Type your email and password to continue'	
        else:	
            m = session['msg']	
            session['msg'] = None	
        return render_template('login.html', title='Login', msg=m)	
    	
@app.route('/logout', methods = ['GET','POST'])	
def logout():	
    del session['user']	
    del session['active']	
    return render_template('login.html', title='Login', msg='You have logged out successfully.')
   
def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']#time since last login
        print(timeSinceAct)
        if timeSinceAct > 300:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False   
    
@app.route('/mainadmin')
def mainadmin():
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    elif session['user']['userType'] == 'customer':
        return redirect('login')
        
    userinfo = 'Hello, ' + session['user']['userFName'] + ' ' + session['user']['userLName'] + ' (' + session['user']['userType'] + ')'
    return render_template('mainadmin.html', title='Main menu', msg = userinfo) 

@app.route('/main')
def main():
    return render_template('main.html', title='Main menu')     
       
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
   app.secret_key = '1234'
   app.run(host='127.0.0.1',debug=True)
   
   
   
   
   
   
   
   