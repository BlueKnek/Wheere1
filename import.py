import json
from datetime import datetime

from db import Session
from schema import Item, Position


def str_to_datetime(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")


def datetime_from_json(json, name, default):
    if name in json:
        return str_to_datetime(json[name])
    else:
        return default


def get(json, name, default):
    if name in json:
        return json[name]
    else:
        return default


def import_json(json):
    session = Session()
    for item_json in json['items']:
        positions = []

        for p in item_json['positions']:
            dt = datetime_from_json(p, 'datetime', datetime.now())
            positions.append(Position(
                name=p['name'],
                description=p['description'],
                datetime=dt,
                created=datetime_from_json(p, 'created', dt),
                updated=datetime_from_json(p, 'updated', dt),
                ))

        now = datetime.now()

        item = Item(
            name=item_json['name'],
            description=item_json['description'],
            tags=get(item_json, 'tags', ''),
            image_filename=item_json['image_filename'],
            created=datetime_from_json(item_json, 'created', now),
            updated=datetime_from_json(item_json, 'updated', now),
            positions=positions,
        )
        session.add(item)

    session.commit()


def import_filename(filename):
    data = json.load(open(filename))
    return import_json(data)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input json file from where items will be added')
    args = parser.parse_args()

    import_filename(args.input)
