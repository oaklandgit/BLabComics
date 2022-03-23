import os, json, markdown
from flask import Flask, render_template, redirect, url_for
from random import sample 

app = Flask('app')

@app.template_filter('md')
def md(text):
    return markdown.markdown(text)

def getItems(path):
    file = open(path)
    data = file.read()
    items = json.loads(data)
    return items
    
CONTENT = 'comics.json'
JSON_PATH = os.path.join(app.static_folder, CONTENT)
ITEMS = getItems(JSON_PATH)

# HOME
@app.route('/')
def home():
    bestList = [item for item in ITEMS if 'bestof' in item]
    return render_template('home.jinja', items=bestList[0:12])

# ALL COMICS SHUFFLED
@app.route('/comics/')
def archives():
    return render_template('archives.jinja', items=sample(ITEMS, len(ITEMS)) )

# RANDOMIZER URL
@app.route('/random/')
def random():
    item=sample(ITEMS,1)[0]
    return redirect('/comics/' + item['slug'] + '/')

# DETAIL PAGE
@app.route('/comics/<slug>/')
def detail(slug):
    idx, item = [(index, row) for index, row in enumerate(ITEMS) if row['slug'] == slug][0]
    
    if idx < len(ITEMS) - 1:
        next = ITEMS[idx + 1]
    else:
        next = ITEMS[0]

    return render_template('detail.jinja', item=item, next=next)

# ABOUT
@app.route('/about/')
def about():
  return render_template('about.jinja')

# @app.route('/game/')
# def game():
#   return render_template('game.jinja')
    
app.run(host='0.0.0.0', port=8080)