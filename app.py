import os
import shutil
import csv
import sys
from flask import Flask,render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_bootstrap import Bootstrap
import pandas as pd
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)

df = pd.read_csv('static/food.csv')

# Configurations
app.config['SECRET_KEY'] = 'blah blah blah blah'

class NameForm(FlaskForm):
	name = StringField('Name', default="Bruce Springsteen")
	submit = SubmitField('Submit')

class NameFormnamesearch(FlaskForm):
	pname = StringField('image name')
	submit = SubmitField('Show Picture')

class PriceForm(FlaskForm):
	price1 = StringField('lower bound Price',validators=[DataRequired(message= 'This field is required')])
	price = StringField('upper bound Price',validators=[DataRequired(message= 'This field is required')])
	submit = SubmitField('Show picture and Description')

class NameFormupdatecaption(FlaskForm):
	foodname = StringField('Food Name')
	new_description = StringField('Update Descriptiion')
	submit = SubmitField('Update')

class NameFormDelete(FlaskForm):
	pname = StringField('Image Name',validators=[DataRequired(message= 'This field is required')])
	submit = SubmitField('Delete')


# ROUTES!
@app.route('/',methods=['GET','POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		name = form.name.data
		return render_template('index.html',form=form,name=name)
	return render_template('index.html',form=form,name=None)

@app.route('/Question5',methods=['GET','POST'])
def Question5():
	form = NameForm()
	return render_template('Question 5.html',form=form)

@app.route('/Question6',methods=['GET','POST'])
def Question6():
	form = NameFormnamesearch()
	if form.validate_on_submit():
		pname=form.pname.data
		images=df[df.Picture == pname].Picture.values
		price=df[df.Picture == pname].Price.values
		description=df[df.Picture == pname].Description.values
		return render_template('Question 6.html',form=form,pname=pname,image=images,price=price,description=description )
	return render_template('index.html',form=form,name=None)

@app.route('/Question7',methods=['GET','POST'])
def Question7():
	form = PriceForm()
	if form.validate_on_submit():
		price = form.price.data
		price1= form.price1.data
		images = df[df.Price < price].Picture.values
		description=df[ df.Price < price].Description.values
		return render_template('Question 7.html',form=form,image=images,description=description)
	return render_template('index.html',form=form,name=None)

@app.route('/Question8',methods=['GET','POST'])
def Question8():
	form = NameFormupdatecaption()
	if form.validate_on_submit():
		name = form.foodname.data
		image = df[df.Food==name].Picture.values
		new_description = form.new_description.data
		prev_description = df[df.Food==name].Description.values
		df.at[df.Food==name, 'Description'] = new_description 
		df.to_csv('static/food.csv', index=False) 
		return render_template('Question 8.html',form=form,name= name,image = image,new_description=new_description,prev_description=prev_description)
	return render_template('index.html',form=form,name=None)

@app.route('/deleteRow',methods=['GET','POST'])
def deleteRow():
	data= []
	with open('static/names.csv',"r") as file_csv:
			
			csvfile = csv.reader(file_csv)
			for row in csvfile:
				data.append(row)

	form = NameFormDelete()

	if form.validate_on_submit():
		name = form.pname.data
		length= len(data)
		for i in range(0,length-1,1):
			if data[i][0] == name:
				length= length-1
				del data[i]
				
		with open('static/names.csv', 'w', newline='') as file:     
			write = csv.writer(file) 
			write.writerows(data)
		# data.to_csv('static/names.csv')
		return render_template('deleteRow.html',form=form,rows=data,name= name ,deleteRow=True)
	return render_template('deleteRow.html',form=form, rows=data, deleteRow=True)

@app.route('/help')
def help():
	text_list = []
	# Python Version
	text_list.append({
		'label':'Python Version',
		'value':str(sys.version)})
	# os.path.abspath(os.path.dirname(__file__))
	text_list.append({
		'label':'os.path.abspath(os.path.dirname(__file__))',
		'value':str(os.path.abspath(os.path.dirname(__file__)))
		})
	# OS Current Working Directory
	text_list.append({
		'label':'OS CWD',
		'value':str(os.getcwd())})
	# OS CWD Contents
	label = 'OS CWD Contents'
	value = ''
	text_list.append({
		'label':label,
		'value':value})
	return render_template('help.html',text_list=text_list,title='help')

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
	return render_template('404.html',title='404')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
	return render_template('500.html',title='500')

port = int(os.getenv('PORT', '3000'))
app.run(host='0.0.0.0', port=port)