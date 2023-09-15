#!/usr/bin/env python

#python imports
import requests
from requests.auth import HTTPBasicAuth
import json
import logging
import sys

#local imports
import ProofpointSIEM2Humio_Config as config
from Send2HumioHEC import send_to_HEC

def get_last_query_time(filename=config.last_successful_time_File):
    with open(filename) as file:
        return file.read().strip()

def set_last_query_time(time):
    with open(config.last_successful_time_File, "w") as file:
        file.write(time)

def main():

    #get version from config file and configure logging
    version = config.pfpt_version
    log_level = config.pfpt_log_level
    logging.basicConfig(filename=config.log_file, filemode='a+', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=log_level)

    logging.info('PFPTSIEM2Humio v' + version + ' : Starting data collection process')
    
    #construct API call
    logging.info('PFPTSIEM2Humio v' + version + ' : Constructing API call')
    basicAuth = HTTPBasicAuth(config.SIEM_API_user_name, config.SIEM_API_password)

    #attempt to contact PFPT SIEM API
    logging.info('PFPTSIEM2Humio v' + version + ' : Making API call to Proofpoint SIEM API')

    SIEM_API_params = {
        "format": "json", # should return 'queryEndTime'
        "sinceTime": get_last_query_time() 
    }
    try: 
        response = requests.get(config.SIEM_API_url, auth=basicAuth, params=SIEM_API_params)
        response_code = str(response.status_code)
        pfpt_response = response.json()
        logging.info('PFPTSIEM2Humio v' + version + ' : Call to the Proofpoint SIEM API response code was = ' + response_code)
    
    except Exception as e:
        logging.info('PFPTSIEM2Humio v' + version + ' : Call to the Proofpoint SIEM API response code was = ' + response_code)
        logging.error('PFPTSIEM2Humio v' + version + ' : Error contacting the Proofpoint SIEM API = ' + e.message + '  ' + e.args)
        sys.exit('PFPTSIEM2Humio v' + version + ' : Unable to collect Proofpoint data, please correct any issues and try again')

    for event_type in ['clicksPermitted', 'clicksBlocked', 'messagesDelivered', 'messagesBlocked']:
        events = pfpt_response[event_type]
        num_events = str(len(events))

        if not events:
            logging.info('PFPTSIEM2Humio v' + version + ' : No events of type ' + str(event_type) + ' to send...')    
            continue

        logging.info('PFPTSIEM2Humio v' + version + ' : Preparing to send ' + num_events + ' ' + str(event_type) + ' Events to Humio')

        # Humio/Crowdstrike LogScale can accept a newline delimited list of json objects. 
        # Therefore you can send all events at once instead of 1 at a time.
        to_send = "\n".join(json.dumps(event) for event in events)
        
        logging.info('PFPTSIEM2Humio v' + version + ' ' +event_type +' HEC: Sending data to Humio HEC')

        HECToken = config.HumioHECTokens[event_type]
        try:
            r = send_to_HEC(to_send, HECToken)
            transmit_result = r.status_code
            logging.debug('PFPTSIEM2Humio v' + version + ' ' +event_type +' HEC: Transmission status code for data push to HEC= '+ str(transmit_result))

        except requests.exceptions.RequestException as e:
            error=str(e)
            logging.info('PFPTSIEM2Humio v' + version + ' ' +event_type +' HEC: Unable to evaluate and transmit sensor_data event: Error: ' + error)
            sys.exit('PFPTSIEM2Humio v' + version + ' ' +event_type +' HEC: This is fatal error, please review and correct the issue - CrowdStrike Intel Indicators to Humio is shutting down')

        logging.info('PFPTSIEM2Humio v' + version + ' ' +event_type +' HEC: Sent ' + num_events + ' ' + event_type + ' events to Humio for processing')

    # Set last query time after everything is sent
    set_last_query_time(pfpt_response['queryEndTime'])


if __name__ == "__main__":
    main()