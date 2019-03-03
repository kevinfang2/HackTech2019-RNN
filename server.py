from collections import Counter, defaultdict
from six.moves import cPickle
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import os
import tensorflow as tf
import shutil
import urllib.request
import requests
import re
import json
import time
import wikipediaComparer as wc
from model import Model
import sample


def sample(queries):
    with open(os.path.join('save', 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join('save', 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = cPickle.load(f)
    #Use most frequent char if no prime is given
    model = Model(saved_args, training=False)
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state('save')
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            data = []
            for query in queries:
                predict = model.sample(sess, chars, vocab, 250, query + " ",
                               2).encode('utf-8')
                data.append(predict.decode("utf-8"))
            return data

def getImages(query):
    url = "https://www.google.com/search?q=" + query + "&tbm=isch"
    response = requests.get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    images = html_soup.find_all('img')
    links = []
    for x in images:
        image_link = x.attrs['src']
        links.append(image_link)
    return links

baseUrl = 'https://en.wikipedia.org/wiki/'

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return 'hello'

@app.route("/search", methods=["POST"])
def search():
    # return "the fuck"
    likeCat = request.form.get('interest')
    learnCat = request.form.get('learn')
    likeUrl = baseUrl+likeCat
    learnUrl = baseUrl + learnCat

    resultingKeywords = wc.keyWords(wc.getParagraph(wc.getBestSection(wc.getBestSpan(\
        wc.findBestSpan(wc.subCatDict(learnUrl), wc.allConnections(likeUrl))), learnUrl), learnUrl)).split(' ')
    queries = resultingKeywords[:10]
    paragraphs = []
    common_words = []
    images_links = []
    paragraphs = sample(queries)

    full_dict = defaultdict(dict)
    for x in range(0,len(queries)):
        paragraph = paragraphs[x]
        removed_paragraph = wc.keyWords(paragraph)
        query = queries[x]

        counter = Counter(removed_paragraph.split(' '))
        most_common = counter.most_common(10)
        most_common = {x[0]:x[1] for x in most_common}
        images = getImages(query)

        full_dict[x]['query'] = query
        full_dict[x]['paragraph'] = paragraph
        full_dict[x]['common_words'] = most_common
        full_dict[x]['images'] = images

    return jsonify(dict(full_dict))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)
