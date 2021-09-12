#!/usr/bin/python

from flask import Flask, request
import os, sys, logging, json, requests
import cfworker

#---------------------------------------------------------------
#
# app routes: end points for the app's web interfaces
#
#---------------------------------------------------------------
service = cfworker.cfworker( port=int(os.getenv('PORT')) )
service.app = Flask(__name__)

@service.app.route('/')
def service_home():
        return ('HELLO RUNDECK')

@service.app.route('/webhook', methods=['POST'])
def service_slack_handler():

        # TODO: Validate the Slack token
        token = request.form.get('token', None)

        # Parse the Slack request payload (Assumes format: var1=somevalue, var2=somvalue)
        text = request.form.get('text', None)
        print $text
        data = {i.split('=')[0]: i.split('=')[1] for i in text.split(', ') }
        print $data

        # Save the associated Rundeck Webhook URL
        url = os.getenv('RUNDECK_WEBHOOK_URL')

        # Save the slash command variable values
        value1 = data.get('var1')
        value2 = data.get('var2')

        # Save the associated key names for the Rundeck job parameters
        key1 = os.getenv('SLACK_KEY1')
        key2 = os.getenv('SLACK_KEY2')

        # Build the transformed Rundeck Webhook request
        headers = {'content-type': 'application/json'}
        json_data = {"url":url, key1:value1, key2:value2}

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


#---------------------------------------------------------------
#
# Main Application
#
#---------------------------------------------------------------

def restartService():
        python = sys.executable
        os.execl(python, python, * sys.argv)

if __name__=='__main__':
        try:
                service.start()

        except Exception as e:
                print('Service error, main exception: %s' % e)
                service.stop()
                restartService()

        print('Service stopping')
        service.stop()

