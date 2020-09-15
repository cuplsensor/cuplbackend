# utils.py
from unittest.mock import Mock
from requests.models import Response
import json
from wscodec.encoder.pyencoder.instrumented import InstrumentedSampleTRH


def create_capture_for_tag(response, baseurl, tagserial=None, tagsecretkey=None, nsamples=10):
    if tagserial is None:
        tagserial = response.json()["serial"]
    if tagsecretkey is None:
        tagsecretkey = response.json()["secretkey"]
    capturetrh = InstrumentedSampleTRH(baseurl=baseurl,
                                       serial=tagserial,
                                       secretkey=tagsecretkey,
                                       smplintervalmins=10)
    samplesin = capturetrh.pushsamples(nsamples)
    queries = capturetrh.geturlqs()
    serial = queries['s'][0]
    statusb64 = queries['x'][0]
    timeintb64 = queries['t'][0]
    circbufb64 = queries['q'][0]
    vfmtb64 = queries['v'][0]
    outlist = {
            'serial': serial,
            'statusb64': statusb64,
            'timeintb64': timeintb64,
            'circbufb64': circbufb64,
            'vfmtb64': vfmtb64,
            'samplesin': samplesin
            }
    print(outlist)
    return outlist
