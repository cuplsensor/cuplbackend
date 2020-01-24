# utils.py
from unittest.mock import Mock
from requests.models import Response
import json
import sys
sys.path.append("../../PSCodec")

from encodertb.pyencoder.instrumented import InstrumentedSampleTRH

def create_capture_for_box(response):
    boxserial = response.json()["serial"]
    boxsecretkey = response.json()["secretkey"]
    capturetrh = InstrumentedSampleTRH(serial=boxserial, secretkey=boxsecretkey, smplintervalmins=10)
    samplesin = capturetrh.pushsamples(10)
    queries = capturetrh.geturlqs()
    serial = queries['s'][0]
    statusb64 = queries['x'][0]
    timeintb64 = queries['t'][0]
    circbufb64 = queries['q'][0]
    ver = queries['v'][0]
    outlist = {
            'serial': serial,
            'statusb64': statusb64,
            'timeintb64': timeintb64,
            'circbufb64': circbufb64,
            'ver': ver,
            'samplesin': samplesin
            }
    print(outlist)
    return outlist


def check_samples(response):
    print(response)

if __name__ == "__main__":
    boxresponse = Mock(spec=Response)
    boxresponse.json.return_value = {'serial': 'ABCDEFGH'}
    boxresponse.status_code = 200
    test = create_capture_for_box(boxresponse)
    print(test)