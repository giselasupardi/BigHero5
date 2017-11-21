from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict',methods = ['POST', 'GET'])
def predict():
	import pandas as pd
	import numpy as np
	import json
	from sklearn import preprocessing
	from sklearn import tree
	from sklearn.externals import joblib

	if request.method == 'POST':
		# open map for encoded label in model
		mapper = json.load(open('mapping_data.json'))
		# process the input data
		age = request.form['age']
		workclass = mapper["workclass"][" " + request.form['workclass']]
		fnlwgt = request.form['fnlwgt']
		education = mapper["education"][" " + request.form['education']]
		ed_num = request.form['education-num']
		m_status = mapper["m_status"][" " + request.form['marital-status']]
		occupation = mapper["occupation"][" " + request.form['occupation']]
		relationship = mapper["relationship"][" " + request.form['relationship']]
		race = mapper["race"][" " + request.form['race']]
		sex = mapper["sex"][" " + request.form['sex']]
		c_gain = request.form['capital-gain']
		c_loss = request.form['capital-loss']
		hpw = request.form['hours-per-week']
		n_country = mapper["n_country"][" " + request.form['native-country']]


		atribut = [workclass, relationship, c_gain, c_loss, education, ed_num, m_status, sex, occupation]
		dataframe = pd.DataFrame([atribut])
		# dataframe.columns['workclass', 'relationship', 'c_gain', 'c_loss', 'education', 'ed_num', 'm_status', 'sex', 'occupation']

		# load model
		model = joblib.load('model_pembelajaran.pkl')
		# predicting
		prediction = model.predict(dataframe)

		dict = {'label':prediction[0]}
		return render_template('result.html', result = dict)

		# return ret
	else:
		user = request.args.get('nm')
		return redirect(url_for('success',name = user))

if __name__ == '__main__':
	app.run(debug = "True")