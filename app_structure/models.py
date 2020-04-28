from .extensions import db

class Message(db.Model):
    id = db.Column(db.String(), primary_key = True)
    content = db.Column(db.String(500))

    send_message = db.relationship('Send_message', backref = 'message', lazy=True)

class Session(db.Model):
    id = db.Column(db.String(50), primary_key = True)

    send_message = db.relationship('Send_message', backref = 'session', lazy=True)

class Participant(db.Model):
    id = db.Column(db.String(50), primary_key = True)

send_to_participant = db.Table('send_to_participant',
    db.Column('send_message_id', db.Integer, db.ForeignKey('send_message.id'), primary_key=True),
    db.Column('participant_id', db.String(50), db.ForeignKey('participant.id'), primary_key=True)
)

class Send_message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer)
    session_id = db.Column(db.ForeignKey('session.id'))
    message_id = db.Column(db.ForeignKey('message.id'))

    participants = db.relationship(
        'Participant',
        secondary=send_to_participant,
        lazy=True,
        backref=db.backref('send_message',lazy=True)
    )

    def to_json(self):
        participants = []
        for participant in self.participants:
            participants.append(participant.id)

        message = Message.query.get(self.message_id)
        
        json = {
            'application_id' : self.application_id,
            'session_id' : self.session_id,
            'message_id' : self.message_id,
            'participants' : participants,
            'content' : message.content
        }

        return json



