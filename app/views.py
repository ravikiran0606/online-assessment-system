from app import app,models,lm
import os
from flask_login import LoginManager,login_required,login_user,logout_user
from app.db_create import db_session
from flask_openid import OpenID
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, render_template, json, request, redirect, session, url_for
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

@app.route('/')
def main():
    return render_template('index.html')

# Staff Views

@app.route('/showStaffDash')
@login_required
def showStaffDash():
	lst = models.Test.query.all();
	return render_template('staffdash.html',lst=lst )

@app.route('/showAddTest')
@login_required
def showAddTest():
	oq = models.Objective.query.all()
	bq = models.BigQuestion.query.all()
	return render_template('addtest.html',oq=oq,bq=bq)

@app.route('/showObjective')
@login_required
def showObjective():
	return render_template('objective.html')

@app.route('/showBigQ')
@login_required
def showBigQ():
	return render_template('bigquestion.html')

@app.route('/showResult',methods=['POST'])
@login_required
def showResult():
	t_id = request.form['testid']
	lst = models.Result.query.filter(models.Result.test_id == t_id)
	return render_template('results.html',lst=lst)

@app.route('/addBigQ',methods = ['POST'])
@login_required
def addBigQ():
	q_id = request.form['questid']
	q_desc = request.form['questdesc']
	keywords = request.form['keywords']
	mark = request.form['mark']

	q = models.BigQuestion(q_id,q_desc,keywords,mark)
	db_session.add(q)
	db_session.commit()
	flash("Successfully Added.")
	return redirect(url_for('showBigQ'))

@app.route('/addObj',methods = ['POST'])
@login_required
def addObj():
	q_id = request.form['questid']
	q_desc = request.form['questdesc']
	ch1 = request.form['ch1']
	ch2 = request.form['ch2']
	ch3 = request.form['ch3']
	c_ch = request.form['correctch']

	q = models.Objective(q_id,q_desc,ch1,ch2,ch3,c_ch)
	db_session.add(q)
	db_session.commit()
	flash("Successfully Added.")
	return redirect(url_for('showObjective'))

@app.route('/addTest',methods = ['POST'])
@login_required
def addTest():
	test_id = request.form['testid']
	test_name = request.form['testname']
	total_marks = request.form['total']
	subject = request.form['subname']
	obj1 = request.form['obj1']
	obj2 = request.form['obj2']
	obj3 = request.form['obj3']
	obj4 = request.form['obj4']
	obj5 = request.form['obj5']
	big1 = request.form['bq1']
	big2 = request.form['bq2']

	t = models.Test(test_id,test_name,total_marks,subject,obj1,obj2,obj3,obj4,obj5,big1,big2)
	db_session.add(t)
	db_session.commit()
	flash("Successfully Added.")
	return redirect(url_for('showAddTest'))


# Student Views

@app.route('/showStudentDash')
@login_required
def showStudentDash():
	lst = models.Test.query.all();
	rt = models.Result.query.all();
	return render_template('studentdash.html',lst=lst,rt=rt)

@app.route('/showAttendTest', methods = ['POST','GET'])
@login_required
def showAttendTest():
	t_id = request.form['testid'];
	t = models.Test.query.get(t_id)
	q1 = models.Objective.query.get(t.obj1)
	q2 = models.Objective.query.get(t.obj2)
	q3 = models.Objective.query.get(t.obj3)
	q4 = models.Objective.query.get(t.obj4)
	q5 = models.Objective.query.get(t.obj5)
	b1 = models.BigQuestion.query.get(t.big1)
	b2 = models.BigQuestion.query.get(t.big2)
	return render_template('attendtest.html',t=t,q1=q1,q2=q2,q3=q3,q4=q4,q5=q5,b1=b1,b2=b2)

@app.route('/validate', methods=['POST'])
@login_required
def validate():
	t_id = request.form['testid']
	u_id = request.form['userid']
	a1 = request.form['q1']
	a2 = request.form['q2']
	a3 = request.form['q3']
	a4 = request.form['q4']
	a5 = request.form['q5']
	b11 = request.form['b1']
	b22 = request.form['b2']

	t = models.Test.query.get(t_id)
	q1 = models.Objective.query.get(t.obj1)
	q2 = models.Objective.query.get(t.obj2)
	q3 = models.Objective.query.get(t.obj3)
	q4 = models.Objective.query.get(t.obj4)
	q5 = models.Objective.query.get(t.obj5)
	b1 = models.BigQuestion.query.get(t.big1)
	b2 = models.BigQuestion.query.get(t.big2)

	mark = 0
	if(q1.c_choice == int(a1)):
		mark = mark+1
	if(q2.c_choice == int(a2)):
		mark = mark+1
	if(q3.c_choice == int(a3)):
		mark = mark+1
	if(q4.c_choice == int(a4)):
		mark = mark+1
	if(q5.c_choice == int(a5)):
		mark = mark+1

	cnt1 = 0
	key1 = b1.keywords.split()
	ans1 = b11.split()

	for i in key1:
		flag = 0
		for j in ans1:
			if i == j:
				flag=1
				break
		if flag == 1:
			cnt1 = cnt1+1

	temp = cnt1 * 10
	temp = temp / len(key1)
	mark = mark + temp

	cnt2 = 0
	key2 = b2.keywords.split()
	ans2 = b22.split()

	for i in key2:
		flag = 0
		for j in ans2:
			if i == j:
				flag=1
				break
		if flag == 1:
			cnt2 = cnt2+1

	temp = cnt2 * 10
	temp = temp / len(key2)
	mark = mark + temp

	r = models.Result(t_id,u_id,mark)
	db_session.add(r);
	db_session.commit();
	flash("Successfully Submitted! Your Mark is "+ str(mark))
	return redirect(url_for('showStudentDash'))


# Profile View 

@app.route('/showStaffProfile')
def showStaffProfile():
	return render_template('staffprofile.html')


@app.route('/showStudentProfile')
def showStudentProfile():
	return render_template('studentprofile.html')

# Login and SignUp Views


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods = ['POST','GET'])
def signUp():
	if request.method == 'POST':
		name = request.form['usernamesignup'];
		email_id = request.form['emailsignup'];
 		user_id = request.form['useridsignup'];
		password = request.form['passwordsignup'];
		user_type = request.form['user_typesignup'];

		if name and email_id and user_id and password and user_type:
			u = models.User(name,email_id,int(user_id),password,user_type)
			db_session.add(u)
			db_session.commit() 
			flash("Successfully Registered.")
			return redirect(url_for('showSignUp'))
		else:
			flash("Please enter all the details.")
			return redirect(url_for('showSignUp'))

	else:
		return redirect(url_for('showSignUp'))

@app.route('/showSignin')
def showSignin():
	return render_template('signup.html')

@app.route('/signIn',methods = ['POST','GET'])
def signIn():
	if request.method == 'POST':
 		user_id = request.form['useridsignin'];
		password = request.form['passwordsignin'];

		u = models.User.query.filter(models.User.user_id == user_id)

		user = None
		for i in u:
			if i.password == password:
				user = i

		if not user:
			flash("Incorrect User ID or Password.") 
			return redirect(url_for('showSignin'))
		else:
			login_user(user)
			if user.user_type == "student":
				return redirect(url_for('showStudentDash'))
			else:
				return redirect(url_for('showStaffDash'))
	else:
		return redirect(url_for('showSignin'))
		

@lm.user_loader
def load_user(user_id):
	user = None
	u = models.User.query.filter(models.User.user_id == user_id)
	for i in u:
		if i.user_id == user_id:
			user = i
			break
	return user

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main'))