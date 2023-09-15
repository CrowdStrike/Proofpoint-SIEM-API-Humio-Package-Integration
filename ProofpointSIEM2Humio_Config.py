import logging


#Set Logging Level and file name
pfpt_log_level = logging.DEBUG
log_file = 'PFPT_SIEMapi2Humio.log'
last_successful_time_File = 'last_success_time'

#Code version - do not alter
pfpt_version = '1.0'

#####Proofpoint API Config Information
SIEM_API_url = 'https://tap-api-v2.proofpoint.com/v2/siem/all'
SIEM_API_user_name = ''
SIEM_API_password = ''


#####Humio HEC configuration
Humio_base = ''
HumioHECurl = Humio_base+'/api/v1/ingest/hec/raw'
#sample full HEC URL = http://192.168.1.229:8080/api/v1/ingest/hec/raw

HumioHECContent_pfpt  = "{'Content-Type': 'application/json', 'Accept':'application/json'}"
HumioHECverify = False

# Token Mapping
HumioHECTokens = {
    #Humio HEC Token for Clicks Permitted events
    'clicksPermitted': '',

    #Humio HEC Token for Clicks Blocked events
    'clicksBlocked': '',

    #Humio HEC Token for Messages Delivered events
    'messagesDelivered': '',
    
    #Humio HEC Token for Messages Blocked events
    'messagesBlocked': ''
}
