from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
db = SQLAlchemy(app)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)  # New field

with app.app_context():
    db.create_all()

# API: Get all appointments
@app.route('/api/appointments')
def get_appointments():
    appointments = Appointment.query.all()
    events = []
    for appt in appointments:
        events.append({
            'id': appt.id,
            'title': appt.title,
            'start': appt.time.isoformat(),
            'description': appt.description  # Include description
        })
    return jsonify(events)

# API: Add appointment
@app.route('/api/appointments', methods=['POST'])
def add_appointment():
    data = request.get_json()
    try:
        new_appt = Appointment(
            title=data['title'],
            time=datetime.fromisoformat(data['time']),
            description=data.get('description', '')  # Optional field
        )
        db.session.add(new_appt)
        db.session.commit()
        return jsonify({'message': 'Added!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API: Delete (unchanged)
@app.route('/api/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    appt = Appointment.query.get_or_404(id)
    db.session.delete(appt)
    db.session.commit()
    return jsonify({'message': 'Deleted!'})

@app.route('/')
def index():
    return render_template('calendar.html')

if __name__ == '__main__':
    app.run(debug=True)