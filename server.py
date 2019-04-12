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

    search_word = question.split()
    indexes = []
    for t in questions['Title']:
        c = smart_suggestion(search_word, t)
        indexes.append(c)
        arr = np.array(indexes)
    replace = arr.argsort()[-5:][::-1]
    toReturn = {}
    mylist = ['first', 'second', 'third', 'fourth', 'fifth']
    for i, o in enumerate(mylist):
        toReturn[o] = {'title': questions['Title'][replace[i]], 'questions': questions['questions'][replace[i]], 'answers':questions['answers'][replace[i]]}
    return jsonify(toReturn)

def smart_suggestion(list1, string2):
    return len(set(list1)&set(string2.split()))


if __name__ == "__main__" : 
    app.run()


