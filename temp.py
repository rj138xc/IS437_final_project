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
    return render_template('users.html', title='User List',  users=u.data)
    
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
    return render_template('user.html', title='User ',  user=u.data[0])  
@app.route('/newuser',methods = ['GET', 'POST'])
def newuser():
    if request.form.get('fname') is None:
        u = userList()
        u.set('userFName','')
        u.set('userLName','')
        u.set('userEmail','')
        u.set('userPassword','')
        u.set('userType','')
        u.add()
        return render_template('newuser.html', title='New User',  user=u.data[0]) 
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
            return render_template('saveduser.html', title='User Saved',  user=u.data[0])
        else:
            return render_template('newuser.html', title='User Not Saved',  user=u.data[0],msg=u.errorList)
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
    print(u.data)
    #return ''
    return render_template('saveduser.html', title='User Saved',  user=u.data[0])
    
'''
======================================================================
END USER PAGES 
======================================================================
'''