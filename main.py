from flask import Flask, render_template, request, send_from_directory, url_for, redirect, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from schema import Item, Position
from db import Session

app = Flask(__name__)

UPLOADED_IMAGES = 'uploaded_images'


def new_uploaded_filename(folder, filename):
    filename = secure_filename(filename)
    if not os.path.exists(os.path.join(folder, filename)):
        return filename
    else:
        name, extension = os.path.splitext(filename)
        for i in range(999):
            filename_num = name + '_' + i.zfill(3) + extension
            if not os.path.exists(os.path.join(folder, filename_num)):
                return filename_num
        raise EnvironmentError('Problem with finding free filename for '+filename)


def new_uploaded_image_filename(filename):
    return new_uploaded_filename(UPLOADED_IMAGES, filename)


def save_image_if_exists():
    print('image' in request.files)
    if 'image' in request.files:
        file = request.files['image']
        print(file)
        if file and file.filename:
            print(file.filename)
            filename = new_uploaded_image_filename(file.filename)
            file.save(os.path.join(UPLOADED_IMAGES, filename))
            return filename
    return ''


@app.route('/img/<string:filename>')
def uploaded_image(filename):
    return send_from_directory(UPLOADED_IMAGES, filename)


@app.route('/')
def root():
    return render_template('root.html')


@app.route('/new_item', methods=['GET', 'POST'])
def new_item():
    if request.method == 'POST':
        created = datetime.now()

        name = request.form['name']
        description = request.form['description']
        image_filename = save_image_if_exists()

        item = Item(name=name, description=description, image_filename=image_filename, created=created, updated=created)

        session = Session()
        session.add(item)
        session.commit()

        return redirect(url_for('items'))
    else:
        return render_template('item_form.html')


@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    session = Session()
    item = session.query(Item).get(item_id)
    if request.method == 'POST':
        updated = datetime.now()

        name = request.form['name']
        description = request.form['description']
        image_filename = save_image_if_exists()

        if name: item.name = name
        if description: item.description = description
        if image_filename: item.image_filename = image_filename
        item.updated = updated

        session.commit()
        return redirect(url_for('items'))
    else:
        return render_template('item_form.html', item=item)


@app.route('/item/<int:item_id>/new_position', methods=['POST'])
def new_position(item_id):
    if request.method == 'POST':
        created = datetime.now()

        session = Session()
        item = session.query(Item).get(item_id)

        print(item)

        name = request.form['name']
        if 'description' in request.form:
            description = request.form['description']
        else:
            description = ''
        datetime_ = datetime.now()

        item.positions.append(Position(item=item, name=name, description=description, datetime=datetime_,
            created=created, updated=created))

        session.commit()
        return redirect(url_for('items'))



@app.route('/item/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    session = Session()
    item = session.query(Item).get(item_id)
    session.delete(item)
    session.commit()
    return redirect(url_for('items'))


@app.route('/items')
def items():
    session = Session()
    items = session.query(Item).all()
    return render_template('items.html', items=items)


@app.route('/export.json')
def export_json():
    session = Session()
    items = session.query(Item).all()
    json = {}
    json_items = []
    json['items'] = json_items
    for item in items:
        json_items.append({
            'name': item.name,
            'description': item.description,
            'image_filename': item.image_filename,

            'created': str(item.created),
            'updated': str(item.updated),

            'positions': [{
                'name': position.name,
                'description': position.description,
                'datetime': str(position.datetime),

                'created': str(position.created),
                'updated': str(position.updated),
            } for position in reversed(item.positions)]
        })
    return jsonify(json)
