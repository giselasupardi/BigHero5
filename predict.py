from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def index():
	import json
	# open map for encoded label in model
	mapper = json.load(open('mapping_data.json'))
	return render_template('index.html', mapper = mapper)

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

		# open map for mode of data
		modes = json.load(open('mapping_mode.json'))

		# process the input data
		## age
		age = request.form['age']
		## workclass
		req = " " + request.form['workclass']
		if req in mapper["workclass"]:
			if req == " ?":
				workclass = modes["workclass"]
			else:
				workclass = mapper["workclass"][req]
		else: # ganti jadi modus, ambil dari file eksternal
			workclass = modes["workclass"]
		## fnlwgt
		fnlwgt = request.form['fnlwgt']
		## education
		req = " " + request.form['education']
		if req in mapper["education"]:
			education = mapper["education"][req]
		else: # ganti jadi modus, ambil dari file eksternal
			education = modes["education"]
		## education-num
		ed_num = request.form['education-num']
		## marital-status
		req = " " + request.form['marital-status']
		if req in mapper["m_status"]:
			m_status = mapper["m_status"][req]
		else: # ganti jadi modus, ambil dari file eksternal
			m_status = modes["m_status"]
		## occupation
		req = " " + request.form['occupation']
		if req in mapper["occupation"]:
			if req == " ?":
				occupation = modes["occupation"]
			else:
				occupation = mapper["occupation"][req]
		else: # ganti jadi modus, ambil dari file eksternal
			occupation = modes["occupation"]
		## relationship
		req = " " + request.form['relationship']
		if req in mapper["relationship"]:
			relationship = mapper["relationship"][req]
		else: # ganti jadi modus, ambil dari file eksternal
			relationship = modes["relationship"]
		## race
		req = " " + request.form['race']
		if req in mapper["race"]:
			race = mapper["race"][req]
		else: # ganti jadi modus, ambil dari file eksternal
			race = modes["race"]
		## sex
		req = " " + request.form['sex']
		if req in mapper["sex"]:
			sex = mapper["sex"][req]
		else: # ganti jadi modus, ambil dari file eksternal
			sex = modes["sex"]
		## capital-gain
		c_gain = request.form['capital-gain']
		## capital-loss
		c_loss = request.form['capital-loss']
		## hours-per-week
		hpw = request.form['hours-per-week']
		## native-country
		req = " " + request.form['native-country']
		if req in mapper["n_country"]:
			if req == " ?":
				n_country = modes["n_country"]
			else:
				n_country = mapper["n_country"][req]
		else: # ganti jadi modus, ambil dari file eksternal
			n_country = modes["n_country"]

		atribut = [workclass, relationship, c_gain, c_loss, education, ed_num, m_status, sex, occupation]
		dataframe = pd.DataFrame([atribut])
		
		# load model
		model = joblib.load('model_pembelajaran.pkl')
		# predicting
		prediction = model.predict(dataframe)

		dict = {'label':prediction[0]}
		return render_template('result.html', result = dict)

		# return ret
	else:
		return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug = "True")