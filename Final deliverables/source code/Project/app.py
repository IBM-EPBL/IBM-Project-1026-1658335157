from turtle import st
from flask import Flask,render_template,request,redirect,url_for,session
from markupsafe import escape

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31929;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bxv32119;PWD=pddAoeX0uA0i3RZv",'','')
print ("Database connection established", conn)

app = Flask(__name__)



@app.route('/')
def home():
  return render_template('index.html')

@app.route('/usersignup')
def usersignup():
  return render_template('usersignup.html')

@app.route('/adminsignup')
def adminsignup():
  return render_template('adminsignup.html')

@app.route('/userlogin')
def userlogin():
  return render_template('usersignin.html')

@app.route('/adminlogin')
def adminlogin():
  return render_template('adminsignin.html')

@app.route('/adminnotify')
def adminnotify():
    message = Mail(from_email="rohansri2002@gmail.com",to_emails="praveenmahen2001@gmail.com",subject="Out of stock",html_content="<p>Some products are out of stock please check it out</p>")
    
    try:
     sg = SendGridAPIClient("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")
     response = sg.send(message)
     return render_template('userpanel.html',msg="Admin have been notified through mail")
    except Exception as e:
     print(e)
     return render_template('userpanel.html',msg="Error")
     

   


 
    


@app.route('/userregisteration',methods = ['POST', 'GET'])
def userregistration():
  if request.method == 'POST':

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirmpassword = request.form['confirmpassword']
   

    sql = "SELECT * FROM USER_DATA WHERE USER_EMAIL=? "
    
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('index.html', msg="You are already a user, please login using your details")
    else:
      insert_sql = "INSERT INTO USER_DATA VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, password)
      ibm_db.bind_param(prep_stmt, 4, confirmpassword)
      
      ibm_db.execute(prep_stmt)
      message = Mail(from_email="rohansri2002@gmail.com",to_emails=email,subject="User Registration",html_content="<p>You have been successfully registered as a user.</p>")
    
    try:
     sg = SendGridAPIClient("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")
     response = sg.send(message)
     return render_template('usersignin.html',msg="Registration successfull. Please login using your credentials")
    except Exception as e:
     print(e)
     
    

   
     return render_template('usersignin.html',msg="unable to send message to your mail" )
    


@app.route('/usercheck',methods = ['POST', 'GET'])
def usercheck():
    
   if request.method == 'POST':
    
    email = request.form['email']
    password = request.form['password']

    sql = "SELECT * FROM USER_DATA WHERE USER_EMAIL=? and USER_PASSWORD= ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,password)
    
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
      sql = "SELECT USER_NAME FROM USER_DATA WHERE USER_EMAIL=?"
      stmt = ibm_db.prepare(conn, sql)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      account = ibm_db.fetch_assoc(stmt)
      message = Mail(from_email="rohansri2002@gmail.com",to_emails=email,subject="User registration",html_content="<p>You have been successfully registered as a user.</p>")
    
      try:
       sg = SendGridAPIClient("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")
       response = sg.send(message)
       return render_template('userpanel.html',msg=account)
      except Exception as e:
        print(e)
     
      
      
    else:
      return render_template('index.html', msg="Your login credentials are not mached with our records.Please login correctly or signup")

@app.route('/adminregistration',methods = ['POST', 'GET'])
def adminregistration():
  if request.method == 'POST':

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirmpassword = request.form['confirmpassword']
    ece = request.form['secretkey']
    
    if ece:


      sql = "SELECT * FROM ADMIN_DATA WHERE ADMIN_EMAIL=? "
    
      stmt = ibm_db.prepare(conn, sql)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      account = ibm_db.fetch_assoc(stmt)
      
      if account:
         return render_template('adminsignin.html', msg="You are already an admin, please login using your details")
      else:
       insert_sql = "INSERT INTO ADMIN_DATA VALUES (?,?,?,?)"
       prep_stmt = ibm_db.prepare(conn, insert_sql)
       ibm_db.bind_param(prep_stmt, 1, name)
       ibm_db.bind_param(prep_stmt, 2, email)
       ibm_db.bind_param(prep_stmt, 3, password)
       ibm_db.bind_param(prep_stmt, 4, confirmpassword)
      
       ibm_db.execute(prep_stmt)
       
       return render_template('adminsignin.html',msg="Admin registration successfull.Please login with your credentials." )
    else: 
      return render_template('adminsignin.html',msg="Your secret key is invalid provide it correctly" )



@app.route('/admincheck',methods = ['POST', 'GET'])
def admincheck():
    
   if request.method == 'POST':
    
    email = request.form['email']
    password = request.form['password']

    sql = "SELECT * FROM ADMIN_DATA WHERE ADMIN_EMAIL=? and ADMIN_PASSWORD= ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,password)
    
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
      sql = "SELECT ADMIN_NAME FROM ADMIN_DATA WHERE ADMIN_EMAIL=?"
      stmt = ibm_db.prepare(conn, sql)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      account = ibm_db.fetch_assoc(stmt)
      
      return render_template('adminpanel.html',msg=account)
     
       
    else:
      return render_template('adminsignin.html',msg="Your login credentials are not matched with our records.Please login correctly or signup" )



@app.route('/adminpanel',methods = ['POST', 'GET'])
def adminpanel():
  if request.method == 'POST':

    id = request.form['id']
    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']
   

    sql = "SELECT * FROM PRODUCT_DATA WHERE PRODUCT_NAME=? and PRODUCT_ID=? "
    
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.bind_param(stmt,2,id)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    
    if account:

      return render_template('adminpanel.html', msg="Product already added")
    else:
      insert_sql = "INSERT INTO PRODUCT_DATA VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, id)
      ibm_db.bind_param(prep_stmt, 2, name)
      ibm_db.bind_param(prep_stmt, 3, price)
      ibm_db.bind_param(prep_stmt, 4, stock)
      
      ibm_db.execute(prep_stmt)
    
   
    return render_template('adminpanel.html',msg="Product successfully added" )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


  
     
