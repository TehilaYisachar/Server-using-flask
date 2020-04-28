from flask import Blueprint, jsonify, request, make_response
from .extensions import db
from .models import Message, Send_message, Session, Participant, send_to_participant

main = Blueprint('main',__name__)


@main.route('/')
def main_index():
    return 'hello'

@main.route('/AddMessage', methods=['POST'])
def add_message():
    req_data = request.get_json()
    print(req_data)
    if not (req_data.get('application_id') and req_data.get('session_id') and req_data.get('message_id') and req_data.get('participants') and req_data.get('content')):
        return make_response(jsonify({"Error": "Invalid request"}), 400)

    session = Session.query.filter_by(id=req_data.get('session_id')).first()
    if not session:
        session = Session(id = req_data.get('session_id'))
        db.session.add(session) 

    message = Message.query.filter_by(id=req_data.get('message_id')).first()
    if message:
        return make_response(jsonify({"Error": "Message id already exists"}), 400)
         
    message = Message(id = req_data.get('message_id'), content = req_data.get('content'))
    db.session.add(message)

    participants = []

    for participant in req_data.get('participants'):
        new_participant = Participant.query.filter_by(id=participant).first()
        if not new_participant:
            new_participant = Participant(id = participant)
            db.session.add(new_participant)
        participants.append(new_participant)

    send_message = Send_message(
        application_id = req_data.get('application_id'),
        session = session,
        message = message,
        participants = participants
    )
    
    db.session.add(send_message)
    db.session.commit()

    return make_response(jsonify({"Success": "Message added"}), 201)
    

@main.route('/GetMessage', methods=['GET'])
def get_message():
    messageId = request.args.get('messageId')
    applicationId = request.args.get('applicationId')
    sessionId = request.args.get('sessionId')

    print(applicationId)

    if not (messageId or applicationId or sessionId):
        return make_response(jsonify({"Error": "Invalid request"}), 400)

    if messageId:
        message = Send_message.query.filter_by(message_id=str(messageId)).first()
        if message:
            return make_response(jsonify(message.to_json()),200)

    messages_lst = []
    if applicationId:
        messages_lst = Send_message.query.filter_by(application_id=applicationId)
    
    if sessionId:
        messages_lst = Send_message.query.filter_by(session_id=str(sessionId))

    if messages_lst.count() != 0:
        return jsonify({'messages' : [message.to_json() for message in messages_lst]})
    
    return make_response(jsonify({"error": "The Message / Messages do not exist"}), 404)


@main.route('/DeleteMessage', methods=['DELETE'])
def delete_message():
    applicationId = request.args.get('applicationId')
    sessionId = request.args.get('sessionId')
    messageId = request.args.get('messageId')

    if not (messageId or applicationId or sessionId):
        return make_response(jsonify({"Error": "invalid request"}), 400)

    if applicationId:
        messages = Send_message.query.filter_by(application_id=applicationId).all()
    
    if sessionId:
        messages = Send_message.query.filter_by(session_id=str(sessionId)).all()

    if messageId:
        messages = Send_message.query.filter_by(message_id=str(messageId)).all()

    if len(messages) == 0:
        return make_response(jsonify({"Error": "The Message / Messages do not exist"}), 404)
        
    for send_message in messages:
        message = Message.query.filter_by(id=send_message.message_id).first()
        db.session.delete(message)
        db.session.delete(send_message)
        
    participants_lst = []

    for send_message in Send_message.query.all():
        participants_lst[0:0] = send_message.participants
    
    for participant in Participant.query.all():
        if not participant in participants_lst:
            db.session.delete(participant)

    for session in Session.query.all():
        s = Send_message.query.filter_by(session_id=session.id).first()
        if Send_message.query.filter_by(session_id=session.id).first() is None:
            db.session.delete(session)

    db.session.commit()   

    return make_response(jsonify({"Success": "The Message / Messages deleted"}), 200)




