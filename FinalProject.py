from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://MarroquinDB:Adml1168@marroquincis3368db.ctgtbyie81ca.us-east-1.rds.amazonaws.com/MarroquinCIS3368DB'
db = SQLAlchemy(app)


class Floor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)
    name = db.Column(db.String(255))

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer)
    number = db.Column(db.Integer)
    floor_id = db.Column(db.Integer, db.ForeignKey('floor.id'))
    floor = db.relationship('Floor', backref='rooms')

class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    age = db.Column(db.Integer)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', backref='residents')

# API endpoints for managing floors, rooms, and residents

@app.route('/floors', methods=['GET', 'POST'])
def manage_floors():
    if request.method == 'GET':
        floors = Floor.query.all()
        floor_data = [{'id': floor.id, 'level': floor.level, 'name': floor.name} for floor in floors]
        return jsonify({'floors': floor_data})

    elif request.method == 'POST':
        data = request.get_json()
        if 'level' in data and 'name' in data:
            level = data['level']
            name = data['name']
            new_floor = Floor(level=level, name=name)
            db.session.add(new_floor)
            db.session.commit()
            return jsonify({'message': 'Floor added successfully'}), 201
        else:
            return jsonify({'error': 'Invalid data format for adding a floor'}), 400

# Similar endpoints for managing rooms and residents can be added.

if __name__ == '__main__':
    app.run(debug=True)
