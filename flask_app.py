from flask import Flask, make_response, request, jsonify

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
import requests
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


app = Flask(__name__)



def get_all_data():
    root = "/home/shubhamiiest/mysite/Datasets/"

    with open(root + "imdb_labelled.txt", "r") as text_file:
        data = text_file.read().split('\n')

    with open(root + "amazon_cells_labelled.txt", "r") as text_file:
        data += text_file.read().split('\n')

    with open(root + "yelp_labelled.txt", "r") as text_file:
        data += text_file.read().split('\n')

    with open(root + "random.txt", "r", encoding='utf-8') as text_file:
        data += text_file.read().split('\n')

    with open(root + "data_python.txt", "r") as text_file:
        data += text_file.read().split('\n')

    return data

def preprocessing_data(data):
    processing_data = []
    for single_data in data:
        if len(single_data.split("\t")) == 2 and single_data.split("\t")[1] != "":
            processing_data.append(single_data.split("\t"))

    return processing_data

#all_data = get_all_data()
#values = preprocessing_data(all_data)

#print(values[0])

def split_data(data):
    total = len(data)
    training_ratio = 0.95
    training_data = []
    evaluation_data = []

    for indice in range(0, total):
        if indice < total * training_ratio:
            training_data.append(data[indice])
        else:
            evaluation_data.append(data[indice])

    return training_data, evaluation_data


def preprocessing_step():
    data = get_all_data()
    processing_data = preprocessing_data(data)

    return split_data(processing_data)
def training_step(data, vectorizer):
    training_text = [data[0] for data in data]
    training_result = [data[1] for data in data]

    training_text = vectorizer.fit_transform(training_text)

    return BernoulliNB().fit(training_text, training_result)

#result = classifier.predict(vectorizer.transform(["I love this movie!"]))

#print(result[0])

def analyse_text(classifier, vectorizer, text):
    return text, classifier.predict(vectorizer.transform([text]))


'''training_data, evaluation_data = preprocessing_step()
vectorizer = CountVectorizer(binary = 'true')
classifier = training_step(training_data, vectorizer)

new_result = analyse_text(classifier, vectorizer, "Best product ever")'''

#print(new_result)

def print_result(result):
    text, analysis_result = result
    print_text = "Positive" if analysis_result[0] == '1' else "Negative"
    print(text, ":", print_text)
    return print_text

#print_result(new_result)

def results1():
    message = request.args.get('text')
    #print(req)
    training_data = preprocessing_step()
    vectorizer = CountVectorizer(binary = 'true')
    classifier = training_step(training_data[0], vectorizer)
    new_result = analyse_text(classifier, vectorizer, message)

    result = print_result(new_result)
    print(result)
    resp = {}
    resp["key"] = ""+str(result)
    resp = jsonify(resp)
    resp = make_response(resp)
    resp.mimetype='application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def results():
    #req = request.form.get.(force=True)
    #print(req)
    training_data = preprocessing_step()
    vectorizer = CountVectorizer(binary = 'true')
    classifier = training_step(training_data[0], vectorizer)
    new_result = analyse_text(classifier, vectorizer, "Best Book Ever")

    result = print_result(new_result)
    return result
def results2():
    URL = "https://covid-193.p.rapidapi.com/statistics?country=india"
    r = requests.get(url = URL,headers= {"x-rapidapi-host":"covid-193.p.rapidapi.com", "x-rapidapi-key":"862526ff37mshcc3afad62a13163p1b40d5jsnfa409a262195"})

    data = r.json()
    #print(data)
    ac = data['response'][0]['cases']['active']
    nc = data['response'][0]['cases']['new']
    nc = nc[1:]
    nc = int(nc)
    ac = ac + nc
    result = str(ac)
    resp = {}
    resp["key"] = ""+result
    resp = jsonify(resp)
    resp = make_response(resp)
    resp.mimetype='application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def sendmail():

    message = Mail(
        from_email='from_email@example.com',
        to_emails='shubhamiiest14@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')

    try:

        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        result = "success"
    except Exception as e:
        print(e)

    resp = {}
    resp["key"] = ""+result
    resp = jsonify(resp)
    resp = make_response(resp)
    resp.mimetype='application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/corona', methods=['GET', 'POST'])
def temp():
    return results2()

@app.route('/', methods=['GET', 'POST'])
def home():
	return "Welcome to Evee's Webhook home page"

@app.route('/ok', methods=['GET', 'POST'])
def index():
    return results1()

@app.route('/send', methods=['GET', 'POST'])
def form():
    return sendmail()


if __name__ == '__main__':
   app.run(debug=True)