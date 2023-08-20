#importing required commands
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import matplotlib.pyplot as plt
import numpy as np


#initializing the app and connecting to database
app  = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tracker.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#tables
class tracker(db.Model):
	Sno = db.Column(db.Integer,primary_key = True,autoincrement=True)
	UserName = db.Column(db.String(100))
	ID = db.Column(db.Integer)
	Name = db.Column(db.String(100))
	Description = db.Column(db.String(100))
	TrackerType = db.Column(db.Integer)

class tracker_log(db.Model):
	ID = db.Column(db.Integer,primary_key = True,autoincrement=True)
	Time = db.Column(db.String(100))
	UserName = db.Column(db.String(100))
	Tracker = db.Column(db.Integer,db.ForeignKey('tracker.ID'))
	Value = db.Column(db.Integer)
	Note = db.Column(db.String(100))
n=""
#main code
@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=="GET":
		return render_template("login.html")
	elif request.method=="POST":
		n = request.form["user"]
		return render_template("dashboard.html",n=n)
s = n	
@app.route('/login/dashboard',methods=['GET'])
def dashboard():
	if request.method=="GET":
		return render_template("dashboard.html")

@app.route('/login/dashboard/addtrac',methods=['GET','POST'])
def addtrac():
	if request.method=="POST":
		user_name = request.form["username"]
		id = request.form["id"]
		name = request.form["name"]
		descp = request.form["desc"]
		tt = request.form["tt"]
		if int(id)==1 or int(id)==2 or int(id)==3:
			data = tracker(UserName=user_name,ID=id,Name=name,Description=descp,TrackerType=tt)
			db.session.add(data)
			db.session.commit()	
			return render_template("traccreated.html")
		else:
			return render_template("error.html")

	return render_template("addtrac.html")

@app.route('/login/dashboard/edittrac',methods=['GET','POST'])
def edittrac():
	if request.method=="POST":
		user_name = request.form["username"]
		id = request.form["id"]
		des = request.form["des"]
		edittracker = tracker.query.filter_by(UserName=user_name,ID=id).first()
		if bool(edittracker)==True:
			edittracker.Description = des
			db.session.add(edittracker)
			db.session.commit()
			return render_template('editsuccess.html')
		else:
			return render_template('error.html')
	return render_template('edittrac.html')

@app.route('/login/dashboard/viewt/<string:usern>',methods=['GET','POST'])
def viewt(usern):
	list = tracker.query.filter_by(UserName=usern).all()
	return render_template('viewt.html',list=list)

@app.route('/login/dashboard/viewtrac',methods=['GET','POST'])
def viewtrac():
	if request.method=="POST":
		user_name = request.form["username"]
		return redirect('/login/dashboard/viewt/{0}'.format(user_name))
	return render_template('viewtrac.html')

@app.route('/login/dashboard/deletrac',methods=['GET','POST'])
def deletrac():
	if request.method=="POST":
		user_name = request.form["username"]
		id = request.form["id"]
		deltrac = tracker.query.filter_by(UserName=user_name,ID=id).first()
		if bool(deltrac)==True:
			db.session.delete(deltrac)
			db.session.commit()
			return render_template('delesuccess.html')
		else:
			return render_template('error.html')
	return render_template('deletrac.html')

@app.route('/login/dashboard/c',methods=['GET'])
def create():
	if request.method=="GET":
		return render_template("createlist.html")

@app.route('/login/dashboard/c/multiple',methods=['GET','POST'])
def createm():
	if request.method=="POST":
		t = datetime.datetime.now()
		user_name = request.form["username"]
		tracker_no = request.form["trackerno"]
		value = request.form["ID"]
		n = request.form["note"]
		dattrac = tracker.query.filter_by(UserName=user_name,ID=tracker_no).all()
		for i in dattrac:		
			if int(tracker_no)==3:
				data = tracker_log(Time=t,UserName=user_name,Tracker=int(tracker_no),Value=value,Note=n)
				db.session.add(data)
				db.session.commit()	
				return render_template("createsuccess.html")
			else:
				return render_template("error.html")
		return render_template("error.html")
	return render_template("createm.html")

@app.route('/login/dashboard/c/running',methods=['GET','POST'])
def createnn():
	if request.method=="POST":
		t = datetime.datetime.now()
		user_name = request.form["username"]
		tracker_no = request.form["trackerno"]
		value = request.form["val"]
		n = request.form["note"]
		dattrac = tracker.query.filter_by(UserName=user_name,ID=tracker_no).all()
		for i in dattrac:
			if int(tracker_no)==2:		
				data = tracker_log(Time=t,UserName=user_name,Tracker=int(tracker_no),Value=int(value),Note=n)
				db.session.add(data)
				db.session.commit()	
				return render_template("createsuccess.html")
			else:
				return render_template("error.html")
		else:
				return render_template("error.html")
	return render_template("createnn.html")

@app.route('/login/dashboard/c/temperature',methods=['GET','POST'])
def createn():
	if request.method=="POST":
		t = datetime.datetime.now()
		user_name = request.form["username"]
		tracker_no = request.form["trackerno"]
		value = request.form["val"]
		value = int(value)
		value = 2*value
		n = request.form["note"]
		dattrac = tracker.query.filter_by(UserName=user_name,ID=tracker_no).all()
		for i in dattrac:
			if int(tracker_no)==1 :		
				data = tracker_log(Time=t,UserName=user_name,Tracker=int(tracker_no),Value=int(value),Note=n)
				db.session.add(data)
				db.session.commit()	
				return render_template("createsuccess.html")
			else:
				return render_template("error.html")
		else:
			return render_template("error.html")	
	return render_template("createn.html")

@app.route('/login/dashboard/delete',methods=['GET','POST'])
def delete():
	if request.method=="POST":
		user_name = request.form["username"]
		t = request.form["time"]
		id = request.form["id"]
		deletetrac = tracker_log.query.filter_by(Time=t,UserName=user_name,Tracker=id).first()
		if bool(deletetrac)==True:
			db.session.delete(deletetrac)
			db.session.commit()
			return render_template('delesuccess.html')
		else:
			return render_template('error.html')
	return render_template('delete.html')


@app.route('/login/dashboard/editlog',methods=['GET','POST'])
def editlog():
	if request.method=="POST":
		user_name = request.form["username"]
		ot = request.form["ot"]
		tno = request.form["tno"]
		nt = request.form["nt"]
		val = request.form["value"]
		note = request.form["note"]
		editlog = tracker_log.query.filter_by(UserName=user_name,Tracker=tno,Time=ot).first()
		if bool(editlog)==True:
			editlog.Time = nt
			editlog.Valur = val
			editlog.Note = note
			db.session.add(editlog)
			db.session.commit()
			return render_template('editsuccess.html')
		else:
			return render_template('error.html')
	return render_template('editlog.html')

@app.route('/login/dashboard/view/<string:usern>/<int:tno>',methods=['GET','POST'])
def viewing(usern,tno):
	list = tracker_log.query.filter_by(UserName=usern,Tracker=tno).all()
	return render_template('viewsuccess.html',list=list)

	
@app.route('/login/dashboard/view',methods=['GET','POST'])
def view():
	if request.method=="POST":
		user_name_v = request.form["username"]
		tn = request.form["tracno"]
		return redirect('/login/dashboard/view/{0}/{1}'.format(user_name_v,tn))

	return render_template("view.html") 

@app.route('/login/dashboard/trend',methods=['GET','POST'])	
def trend():
	l = []
	if request.method=="POST":
		user_name = request.form["username"]
		tn = request.form["tracno"]
		list = tracker_log.query.filter_by(UserName=user_name,Tracker=tn).all()
		if tn=='1':
			for i in list:
				l.append(float(i.Value))
			h = np.array(l)
			plt.plot(h)
			plt.title('TEMPERATURE')
			plt.xlabel('Temperature')
			plt.ylabel('Value')
			plt.savefig('static/plot.png')
			plt.close()
			return render_template("trendhist.html")
		elif tn=='2':
			for i in list:
				l.append(float(i.Value))
			h = np.array(l)
			plt.plot(h)
			plt.title('RUNNING')
			plt.xlabel('Running')
			plt.ylabel('Value')
			plt.savefig('static/plot.png')
			plt.close()
			return render_template("trendhist.html")
		else:
			return render_template("error.html")
	return render_template("trend.html")

if __name__ == '__main__':
    app.run(debug=True)