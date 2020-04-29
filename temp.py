'''
======================================================================
START EVENT PAGES
======================================================================
'''

@app.route('/events')
def events():
    '''    
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    '''
    e = eventList()
    e.getAll()
    
    print(e.data)
    return render_template('event/events.html', title='Event List',  events=e.data)
    
@app.route('/event')
def event():
    '''
    if checkSession() == False: #check to make sure user is logged in	
        return redirect('login')
    '''
    e = eventList()
    if request.args.get(e.pk) is None:
        return render_template('error.html', msg='No event id given.')  

    e.getById(request.args.get(e.pk))
    if len(e.data) <= 0:
        return render_template('error.html', msg='Event not found.')  
    
    print(e.data)
    return render_template('event/event.html', title='Event Details',  event=e.data[0])
    
@app.route('/newevent',methods = ['GET', 'POST'])
def newevent():
    if request.form.get('eventType') is None:
        e = eventList()
        e.set('eventType','')
        e.set('eventAmount','')
        e.set('userID','')
        e.add()
        return render_template('event/newevent.html', title='New Event',  event=e.data[0]) 
    else:
        e = eventList()
        e.set('eventID',request.form.get('eventID'))
        e.set('eventAmount',request.form.get('eventAmount'))
        e.set('userID',request.form.get('userID'))
       
        e.add()
        if e.verifyNew():
            e.insert()
            print(e.data)
            return render_template('event/savedevent.html', title='event Saved',  event=e.data[0])
        else:
            return render_template('event/newevent.html', title='event Not Saved',  event=e.data[0],msg=e.errorList)
            
@app.route('/saveevent',methods = ['GET', 'POST'])
def saveevent():
    e = eventList()
    e.set('eventID',request.form.get('eventID'))
    e.set('eventType',request.form.get('eventType'))
    e.set('eventAmount',request.form.get('eventAmount'))
    e.set('userID',request.form.get('userID'))
    
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