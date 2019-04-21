from flask import Flask
import pandas as pd
import re, math
from collections import Counter
import numpy as np
from flask import jsonify


WORD = re.compile(r'\w+')

questions = pd.read_csv('stackoverflow_25000.csv', encoding='latin-1')
questions = questions.ix[:1000, :]
# questions = questions.ix[0:10000, 1]
# # questions.to_csv("Questions_100000.csv")
print("sucessfully load the data")

app = Flask(__name__)

@app.route('/smart_solution/<question>')
def smart_solution(question):

    search_word = question.split('-')
    indexes = []
    for t in questions['Title']:
        c = smart_suggestion(search_word, t)
        indexes.append(c)
        arr = np.array(indexes)
    replace = arr.argsort()[-5:][::-1]
    toReturn = {}
    mylist = ['first', 'second', 'third', 'fourth', 'fifth']
    for i, o in enumerate(mylist):
        toReturn[o] = {'title': questions['Title'][replace[i]], 'id': str(replace[i])}
    return jsonify(toReturn)

def smart_suggestion(list1, string2):
    return len(set(list1)&set(string2.split()))

@app.route('/get_detail/<id>')
def get_detail(id):
    id = int(id)
    toReturn = {'question': questions['questions'][id], 'answer': questions['answers'][id]}
    return jsonify(toReturn)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/robots.txt")
def robots_txt():
    Disallow = lambda string: 'Disallow: {0}'.format(string)
    return Response("User-agent: *\n{0}\n".format("\n".join([
        Disallow('/bin/*'),
        Disallow('/thank-you'),
    ])))

if __name__ == "__main__" : 
    app.run()


