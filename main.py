import os, json, markdown, wikipedia
from flask import Flask, render_template, redirect, url_for
from random import sample 

app = Flask('app')

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# JINJA FUNCTIONS
@app.template_filter('md')
def md(text):
    return markdown.markdown(text)

@app.template_filter('wiki2keywords')
def wiki(text):
    return ", ".join(wikipedia.search(text))

# FETCH DATA

def getItems(path):
    file = open(path)
    data = file.read()
    items = json.loads(data)
    return items
    
CONTENT = 'comics.json'
JSON_PATH = os.path.join(app.static_folder, CONTENT)
ITEMS = getItems(JSON_PATH)

# 404
@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.jinja'), 404

# CONFIRM GOOGLE
@app.route('/' + os.environ['google'] + '.html')
def goog():
    return render_template(os.environ['google'] + '.html')
    
# HOME
@app.route('/')
def home():
    # GET ANY 13 BEST-OFS. HERO WILL BE THE FIRST
    items = sample([item for item in ITEMS if 'bestof' in item], 13)
    return render_template('home.jinja', hero=items[0], items=items[1:13])

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

    matches = [(index, row) for index, row in enumerate(ITEMS) if row['slug'] == slug]

    if len(matches) == 0:
        return render_template('404.jinja'), 404
    
    idx, item = matches[0]

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