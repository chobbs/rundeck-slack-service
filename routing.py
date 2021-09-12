#!/usr/bin/python

from flask import Flask, request, redirect, url_for, send_from_directory, jsonify, Response
import json, os, logging
import cfworker
import psutil
import requests

#---------------------------------------------------------------
#
# app routes: end points for the app's web interfaces
#
#---------------------------------------------------------------
worker = cfworker.cfworker( port=int(os.getenv('PORT')) )
worker.app = Flask(__name__, static_url_path='')

@worker.app.route('/')
def keen_chart():
        return worker.app.send_static_file('index.html')

@worker.app.route('/webhook', methods=['POST'])
def service_slack_handler():
        # TODO: Validate the Slack token
        token = request.form.get('token', None)

        # Parse the Slack request payload (Assumes format: var1=somevalue, var2=somvalue)
        text = request.form.get('text', None)
        username = request.form.get('user_name', None)
        teamid = request.form.get('team_id', None)
        print (teamid)
        text = text.replace('starlark','')
        text = text.strip()
        print (text)
        data = {i.split('=')[0]: i.split('=')[1] for i in text.split(', ') }
        # Save the associated Rundeck Webhook URL
        url = os.getenv('RUNDECK_WEBHOOK_URL')

        # Save the slash command variable values
        value1 = data.get('var1')
        #value2 = data.get('var2')
        value2 = teamid

        # Save the associated key names for the Rundeck job parameters
        key1 = os.getenv('SLACK_VAR1')
        key2 = os.getenv('SLACK_VAR2')

        # Build the transformed Rundeck Webhook request
        headers = {'content-type': 'application/json'}
        json_data = {"url":url, key1:value1, key2:value2}
        json_data = {"url":url, key1:value1, key2:value2}
        print (json_data)

        # Forward transformed Slack request to Rundeck as POST
        r = requests.post(url=url, headers=headers, data=json.dumps(json_data))
        return data


#---------------------------------------------------------------
#
# logging: suppresses some of the annoying Flask output
#
#---------------------------------------------------------------
log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)

