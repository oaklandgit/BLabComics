import os, json, markdown
from flask import Flask, render_template
# import flask_resize

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

# app.config['RESIZE_URL'] = 'https://blabcomics.larrystone.repl.com/'
# app.config['RESIZE_ROOT'] = '//static/images'
# resize = flask_resize.Resize(app)

@app.route('/')
def home():
    featured = ITEMS[1:9]
    return render_template('home.jinja', items=ITEMS, featured=featured)
    
@app.route('/comics/')
def archives():
    return render_template('archives.jinja', items=ITEMS)

@app.route('/comics/series/<seriesId>/')
def category(seriesId):
    items = [row for row in ITEMS if row['series'] == seriesId]
    return render_template('series.jinja', items=items, seriesId=seriesId)

@app.route('/comics/<slug>/')
def detail(slug):
    idx, item = [(index, row) for index, row in enumerate(ITEMS) if row['slug'] == slug][0]
    
    if idx < len(ITEMS) - 1:
        next = ITEMS[idx + 1]
    else:
        next = ITEMS[0]

    if idx > 0:
        prev = ITEMS[idx - 1]
    else:
        prev = ITEMS[len(ITEMS) - 1]
    
    return render_template('detail.jinja', item=item, prev=prev, next=next)



@app.route('/game/')
def game():
  return render_template('game.jinja')

@app.route('/about/')
def about():
  return render_template('about.jinja')

app.run(host='0.0.0.0', port=8080)