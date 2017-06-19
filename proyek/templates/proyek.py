from flask import Flask, render_template, session, redirect, url_for, escape, request
import sqlite3 as sql
app = Flask(__name__)
app.secret_key = 'none'

@app.route('/')
def home():
   return render_template('home.html')
   
@app.route('/list')
def list():
   con = sql.connect("sepatu.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from sepatu")
   
   rows = cur.fetchall();
   return render_template('list.html', rows = rows)

@app.route('/listadmin')
def listadmin():
   con = sql.connect("sepatu.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from sepatu")
   
   rows = cur.fetchall();
   return render_template('listadmin.html', rows = rows)
   
@app.route('/deletepesanan',methods = ['POST', 'GET'])
def deletepesanan():
   con = sql.connect("sepatu.db")
   con.row_factory = sql.Row
   pesanId = request.form['postPesananId']

   cur = con.cursor()
   print(pesanId)
   cur.execute("delete from pesan where pesanId=?", (pesanId,))
   con.commit()

   return order()
   
@app.route('/deletesepatu',methods = ['POST', 'GET'])
def deletesepatu():
   con = sql.connect("sepatu.db")
   con.row_factory = sql.Row
   sepatuId = request.form['postSepatuId']

   cur = con.cursor()
   print(sepatuId)
   cur.execute("delete from sepatu where sepatuId=?", (sepatuId,))
   con.commit()

   return listadmin()
   
@app.route('/order')
def order():
   con = sql.connect("sepatu.db")
   con.row_factory = sql.Row
   username = session['username']

   cur = con.cursor()
   cur.execute("select * from user where email=?", [username])
   rows = cur.fetchone();
   userId = rows['userId']
   
   cur.execute("select * from sepatu")
   rows = cur.fetchall();
  
   cur.execute("select * from pesan where userId=?", (userId,))
   rows2 = cur.fetchall();
  
   return render_template('order.html',rows=rows, rows2=rows2)

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/addsepatu')
def addsepatu():
   return render_template('addsepatu.html')

@app.route('/detailsepatu',methods = ['POST', 'GET'])
def detailsepatu():
   id = request.args.get('id')
   con = sql.connect("sepatu.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from sepatu where sepatuId=?", id)

   rows = cur.fetchone();
   
   return render_template('detailSepatu.html', row = rows)

@app.route('/pesansepatu',methods = ['POST', 'GET'])
def pesansepatu():
   if request.method == 'POST':
      try:
         username = session['username']
         sepatuId = request.form['postSepatuId']
         print(sepatuId)
         con = sql.connect("sepatu.db")
         con.row_factory = sql.Row 
   
         cur = con.cursor()
         cur.execute("select * from user where email=?", [username])
         rows = cur.fetchone();
         userId = rows['userId']
         with sql.connect("sepatu.db") as con:
            cur = con.cursor()
            print(userId)
            print(sepatuId)
            cur.execute("INSERT INTO pesan (sepatuId, userId) VALUES (?,?)",(sepatuId, userId))
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return list()

@app.route('/tambahsepatu',methods = ['POST', 'GET'])
def tambahsepatu():
   if request.method == 'POST':
      try:
         name = request.form['postName']
         description = request.form['postDescription']
         imageUrl = request.form['postImageUrl']
         ukuran = request.form['postUkuran']
         price = request.form['postPrice']
         
         with sql.connect("sepatu.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO sepatu(name, description, imageUrl, ukuran, price) VALUES (?,?,?,?,?)",(name, description, imageUrl, ukuran, price) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return home()
         
@app.route('/edit',methods = ['POST', 'GET'])
def edit():
   con = sql.connect("sepatu.db")
   con.row_factory = sql.Row
   sepatuId = request.form['postSepatuId']

   cur = con.cursor()
   cur.execute("select * from sepatu where sepatuId=?", [sepatuId])
   row = cur.fetchone();
   
   cur.execute("select * from sepatu where sepatuId=?",[sepatuId])
   row = cur.fetchall();
   print(row)
  
   return render_template("edit.html",rows = row)
   
@app.route('/editsepatu',methods = ['POST', 'GET'])
def editsepatu():
   if request.method == 'POST':
      try:
         name = request.form['postName']
         description = request.form['postDescription']
         imageUrl = request.form['postImageUrl']
         ukuran = request.form['postUkuran']
         price = request.form['postPrice']
         sepatuId = request.form['postSepatuId']
         print name, description, imageUrl, ukuran, price, sepatuId
         
         con = sql.connect("sepatu.db")
         cur = con.cursor()

         cur.execute("UPDATE sepatu SET name=?, description=?, imageUrl=?, ukuran=?, price=? WHERE sepatuId=?",(name, description, imageUrl, ukuran, price, sepatuId))
             
         con.commit()
      except Exception as e:
         print e
         con.rollback()
      finally:
         return listadmin()
         
@app.route('/formregister',methods = ['POST', 'GET'])
def formregister():
   if request.method == 'POST':
      try:
         email = request.form['postEmail']
         password = request.form['postPassword']
         
         with sql.connect("sepatu.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO user (email, password) VALUES (?,?)",(email,password) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return home()
         

@app.route('/formlogin',methods = ['POST', 'GET'])
def formlogin():
   if request.method == 'POST':
      email = request.form['postEmail']
      password = request.form['postPassword']
      con = sql.connect("sepatu.db")
      con.row_factory = sql.Row
   
      cur = con.cursor()
      cur.execute('SELECT COUNT(*) FROM user WHERE email=? AND password=?', (email, password))
   
      rows = cur.fetchone()

      if rows[0] == 1:
         session['username'] = request.form['postEmail']

         return home()
      else:
         return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return home()
@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == '__main__':
   app.debug = True
   app.run('0.0.0.0', 5111)
