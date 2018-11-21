from flask import Flask, render_template, request
import os
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
import cPickle as c


def load(clf_file):
    with open(clf_file) as fp:
        clf = c.load(fp)
    return(clf)

clf = load("text-classifier.mdl")
d = load("dictionary.mdl")



print("....................READY FOR USE..................................")
#Initializing the flask server
app = Flask(__name__)

#Initializing the base page
@app.route('/')
def index():
	return render_template("spammaildetection.html")

#Initializing the about page
@app.route('/About.html')
def about():
	return render_template("About.html")
#Initializing guide page
@app.route('/guide.html')
def guide():
	return render_template("guide.html")


#Initializing the predict page
@app.route('/predict.html',methods = ['POST','GET'])
def predict():
	#Getting the data from the fields
	if request.method == 'POST':
			emailbody = request.form["emailbody"]
	features = []
	data = emailbody.split()
	#print data
	for word in d:
		features.append(data.count(word[0]))
	res = clf.predict([features])
	
	return render_template("predict.html",emailbody=emailbody,predicted=["Not a Spam", "a Spam!!"][res[0]])

	
#Hosting the server with debugger configuration
if __name__ == '__main__':
	app.run(debug = True)
