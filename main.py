from flask import Flask
from flask import render_template
from flask import request

from schema import Item
from db import Session

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('root.html')


@app.route('/item_form', methods=['GET', 'POST'])
def item_form():
    if request.method == 'POST':
        session = Session()
        name = request.form['name']
        description = request.form['description']
        item = Item(name=name, description=description)
        session.add(item)
        session.commit()
        return str(item.id)
    else:
        return render_template('item_form.html')


@app.route('/items')
def items():
    session = Session()
    items = session.query(Item).all()
    return render_template('items.html', items=items)
