from flask import Flask, request, jsonify
from datetime import datetime
import logging
import json
import mysql.connector
import os

from flask import Blueprint
from flask import Response
from flask import request
from flask import redirect

from data.event import Event
from data.event_mysql import EventMySql
from data.event_service import EventService
from icalendar import Calendar

app_events = Blueprint('app_events', __name__)

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "password"),
        database=os.environ.get("DB_NAME", "mydatabase")
    )

def get_event_service():
    event_dao = EventMySql(get_connection())  
    return EventService(event_dao)

@app_events.route('/events', methods=['GET'])
def get_events():
    dao = get_event_service()
    events = dao.get_all_events()
    response = []
    for event in events:
        response.append(event.__dict__)
    return jsonify(response)

@app_events.route('/events/<string:event_uid>', methods=['GET'])
def get_event(event_uid):
    dao = get_event_service()
    event = dao.read_event(event_uid)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    else:
        return jsonify(event.__dict__)

@app_events.route('/events', methods=['POST'])
def create_event():
    dao = get_event_service()
    data = request.json
    if 'uid' not in data:
        return jsonify({'error': 'UID is required'}), 400
    if 'summary' not in data:
        return jsonify({'error': 'Summary is required'}), 400
    if 'start_time' not in data:
        return jsonify({'error': 'Start time is required'}), 400
    start_time = datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M')
    end_time = datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M') if 'end_time' in data else start_time
    event = Event(uid=data['uid'], summary=data['summary'], description=data.get('description'), location=data.get('location'), start_time=start_time, end_time=end_time)
    dao.create_event(event)
    return jsonify(event.__dict__), 201

@app_events.route('/events/<string:event_uid>', methods=['PUT'])
def update_event(event_uid):
    dao = get_event_service()
    event = dao.read_event(event_uid)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    else:
        data = request.json
        if 'summary' in data:
            event.summary = data['summary']
        if 'description' in data:
            event.description = data['description']
        if 'location' in data:
            event.location = data['location']
        if 'start_time' in data:
            event.start_time = datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M')
        if 'end_time' in data:
            event.end_time = datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M')
        dao.update_event(event)
        return jsonify(event.__dict__)

@app_events.route('/events/<string:event_uid>', methods=['DELETE'])
def delete_event(event_uid):
    dao = get_event_service()
    event = dao.read_event(event_uid)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    else:
        dao.delete_event(event_uid)
        return '', 204

@app_events.route('/events/ics', methods=['POST'])
def import_ics():
    try:
        # Parse the ICS file
        logging.info(request.files)
        ics_files = request.files.getlist('file[]')
        logging.info(ics_files)
        for ics_file in ics_files:
            logging.info(ics_file)
            calendar = Calendar.from_ical(ics_file.read().decode())

            # Import each event from the ICS file into the database
            dao = get_event_service()
            for component in calendar.walk('VEVENT'):
                event = Event(
                    uid=component['UID'],
                    summary=component['SUMMARY'],
                    description=component.get('DESCRIPTION', ''),
                    location=component.get('LOCATION', ''),
                    start_time=datetime.fromisoformat(component['DTSTART'].dt.isoformat()),
                    end_time=datetime.fromisoformat(component['DTEND'].dt.isoformat())
                )
                dao.create_event(event)
        return jsonify({'message': 'ICS files imported successfully'}), 200
    except:
        return jsonify({'error': 'Error importing ICS files'}), 500