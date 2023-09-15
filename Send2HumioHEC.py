#!/usr/bin/env python

import requests

#local imports
import ProofpointSIEM2Humio_Config as config

def send_to_HEC(event_data, HumioHECToken):

    HumioHECurl = config.HumioHECurl
    HumioHECcontent = config.HumioHECContent_pfpt
    HumioHECverify = config.HumioHECverify

    header = {"Authorization": "Bearer " + HumioHECToken, "Content-Type": HumioHECcontent} 
    return requests.post(url=HumioHECurl, headers=header, data=event_data, verify=HumioHECverify, timeout=300)
