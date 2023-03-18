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

from data.webhook import Webhook
from data.webhook_mysql import WebhookMySql
from data.webhook_service import WebhookService

app_webhooks = Blueprint('app_webhooks', __name__)

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "password"),
        database=os.environ.get("DB_NAME", "mydatabase")
    )

def get_webhook_service():
    webhook_dao = WebhookMySql(get_connection())    
    return WebhookService(event_dao)

@app_webhooks.route('/webhooks/<string:event_type>', methods=['POST'])
def handle_webhook(event_type):
    # Retrieve the webhook associated with the event type
    service = get_webhook_service()
    webhook = service.get_webhook_by_event_type(event_type)
    if webhook is None or not webhook.enabled:
        return jsonify({'error': 'Invalid webhook'}), 400

    # Verify the signature using the secret key (if provided)
    if webhook.secret_key is not None:
        signature = request.headers.get('X-Signature')
        if signature is None:
            return jsonify({'error': 'Missing signature'}), 400
        expected_signature = hmac.new(
            webhook.secret_key.encode(), request.data, hashlib.sha256).hexdigest()
        if signature != expected_signature:
            return jsonify({'error': 'Invalid signature'}), 400

    # Process the webhook payload
    payload = request.json
    # TODO: Add your webhook processing logic here

    return jsonify({'message': 'Webhook received and processed successfully'}), 200
