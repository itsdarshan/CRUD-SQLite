from flask import Flask, render_template, request
import sqlite3 as sql 

app = Flask(__name__)

#database connection
conn = sql.connect('database.db')
conn.execute('CREATE TABLE stt14(id NUMBER, nm TEXT, addr TEXT, pc TEXT, ct TEXT)')
conn.close()


#routing to home page
@app.route('/')
def home():
	return render_template('home.html')

#routing to new record enter 
@app.route('/enternew')
def new_student():
	return render_template('webform.html')

#routing to new record add   
@app.route('/addrec',methods = ['POST','GET'])
def addrec():
	if request.method == 'POST':
		try:
			id = request.form['id']
			nm = request.form['nm']
			add = request.form['add']
			ct = request.form['ct']
			pc = request.form['pc']

			with sql.connect('database.db') as con:
				curr = con.cursor()
				curr.execute('INSERT INTO stt14(id,nm,addr,pc,ct) values (?,?,?,?,?)',(id,nm,add,pc,ct))
				con.commit()
				msg = 'record added successfully '

		except:
			con.rollback()
			msg = 'error occured'
			
		finally:
			return render_template('result.html',msg = msg)
			con.close()

@app.route('/list')
def list():
	con = sql.connect('database.db')
	con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("select * from stt14")
	rows = cur.fetchall()
	return render_template('list.html',rows = rows)
	return render_template('home.html',rows = rows)
	
@app.route("/delete")  
def delete():  
    return render_template("deleterecord.html")  


@app.route("/deleterecord",methods = ['POST'])
def deleterecord():
	id = request.form["id"]
	with sql.connect("database.db") as con:
		try:
			cur = con.cursor()
			cur.execute("delete from stt14 where id = ?",id)
			msg = "record successfully deleted"
		except:
			msg = "can't be deleted"
		finally:	
			return render_template("deleterecord.html",msg = msg)

@app.route("/update")
def update():
	return render_template('update.html')

@app.route('/updaterecord',methods=['POST'])
def updaterecord():
	id = request.form['id']
	nm = request.form['nm']
	add = request.form['add']
	ct = request.form['ct']
	pc = request.form['pc']
	with sql.connect('database.db') as con:
		try:	
			cur = con.cursor()
			cur.execute('update stt14 set nm=?,addr=?,ct=?,pc=? where id = ?',(nm,add,ct,pc,id))
			msg1= "record successfully updated"
		except:
			msg1 = 'error'
		finally:
			return render_template('update.html',msg1= msg1)
if __name__ == '__main__':
	app.run(debug=True)
