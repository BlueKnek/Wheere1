from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from flask import redirect
from werkzeug.utils import secure_filename
import os

from schema import Item
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
        name = request.form['name']
        description = request.form['description']
        image_filename = save_image_if_exists()

        item = Item(name=name, description=description, image_filename=image_filename)

        session = Session()
        session.add(item)
        session.commit()

        return redirect(url_for('items'))
    else:
        return render_template('item_form.html')


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
