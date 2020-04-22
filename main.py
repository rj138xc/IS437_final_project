from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 
from customer import customerList
from user import userList
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
    c = customerList()
    c.getAll()
    
    print(c.data)
    #return ''
    return render_template('customer/customers.html', title='Customer List',  customers=c.data)
    
@app.route('/customer')
def customer():
    if checkSession() == False: #check to make sure user is logged in	
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
        c.update()
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
    u = userList()
    u.getAll()
    
    print(u.data)
    #return ''
    return render_template('user/users.html', title='User List',  users=u.data)
    
@app.route('/user')
def user():
    if checkSession() == False: #check to make sure user is logged in	
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
@app.route('/saveuser',methods = ['GET', 'POST'])
def saveuser():
    u = userList()
    u.set('userID',request.form.get('userID'))
    u.set('userFName',request.form.get('userFName'))
    u.set('userLName',request.form.get('userLName'))
    u.set('userEmail',request.form.get('userEmail'))
    u.set('userPassword',request.form.get('userPassword'))
    u.set('userType',request.form.get('userType'))
    u.add()
    u.update()
    print('u.data: ',u.data)
    #return ''
    return render_template('user/saveduser.html', title='User Saved',  user=u.data[0])
    
'''
======================================================================
END USER PAGES 
======================================================================
'''    
    
@app.route('/login', methods = ['GET','POST'])	
def login():	
    #check login	
    #set session	
    #redirect to menu	
    #check session on login pages	
    if request.form.get('email') is not None and request.form.get('password') is not None:	
        c = customerList()	
        if c.tryLogin(request.form.get('email'),request.form.get('password')):	
            print('login successful')	
            session['user'] = c.data[0]	
            session['active'] = time.time()	
            	
            return redirect('main')	
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
        if timeSinceAct > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False   
    
@app.route('/main')
def main():
    return render_template('main.html', title='Main menu')  
       
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
   app.secret_key = '1234'
   app.run(host='127.0.0.1',debug=True)
   
   
   
   
   
   
   
   