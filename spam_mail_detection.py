from flask import Flask, render_template, request
import os
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import accuracy_score

def make_dict():
    direc = "emails/"
    files = os.listdir(direc)
    emails = [direc + email for email in files]
    words = []
    c = len(emails)
    for email in emails:
        f = open(email)
        blob = f.read()
        words += blob.split(" ")
        print c
        c -= 1

    for i in range(len(words)):
        if not words[i].isalpha():
            words[i] = ""

    dictionary = Counter(words)
    del dictionary[""]
    return dictionary.most_common(3000)


def make_dataset(dictionary):
    direc = "emails/"
    files = os.listdir(direc)
    emails = [direc + email for email in files]
    feature_set = []
    labels = []
    c = len(emails)

    for email in emails:
        data = []
        f = open(email)
        words = f.read().split(' ')
        for entry in dictionary:
            data.append(words.count(entry[0]))
        feature_set.append(data)

        if "ham" in email:
            labels.append(0)
        if "spam" in email:
            labels.append(1)
        print c
        c = c - 1

    return feature_set, labels


d = make_dict()
features, labels = make_dataset(d)
#print features
#print labels
x_train, x_test, y_train, y_test = tts(features, labels, test_size=0.2)

clf = MultinomialNB()
clf.fit(x_train, y_train)

preds = clf.predict(x_test)
print accuracy_score(y_test, preds)

print "....................READY FOR USE.................................."
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
	print data
	for word in d:
		features.append(data.count(word[0]))
	res = clf.predict([features])
	
	return render_template("predict.html",emailbody=emailbody,predicted=["Not a Spam", "a Spam!!"][res[0]])

	
#Hosting the server with debugger configuration
if __name__ == '__main__':
	app.run(debug = True,host='0.0.0.0',port=5000)
