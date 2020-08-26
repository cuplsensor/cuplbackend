from datetime import timedelta
import pytz
from ...wsapiwrapper.admin.capture import CaptureWrapper
from ...wsapiwrapper.consumer.capture import CaptureWrapper as ConsumerCaptureWrapper

tz = pytz.timezone("Europe/London")


class CaptureHelper:
    def makesamples(self, starttime, timeintmins, nsamples):
        temp = 0
        smpltime = starttime
        samplelist = []
        for x in range(0, nsamples):
            samplelist.append({
                "temp": temp,
                "timestamp": smpltime.astimezone(tz).isoformat()
            })
            temp += 1
            smpltime += timedelta(minutes=timeintmins)
        return samplelist

    def makecapture(self, samples, timeintmins, tag_id):
        capture = {
            "batvoltagemv": 3000,
            "tag_id": tag_id,
            "cursorpos": 10,
            "loopcount": 20,
            "md5": "abcdefgh",
            "samples": samples,
            "status": {
                "brownout": False,
                "clockfail": False,
                "lpm5wakeup": False,
                "misc": False,
                "resetsalltime": 120,
                "supervisor": False,
                "watchdog": False
            },
            "timeintmins": timeintmins,
            "timestamp": samples[-1]['timestamp'],
            "version": 1
        }
        return capture



    def make_capture_with_samples(self, starttime, tag_id, timeintmins=12, nsamples=4):
        samples = self.makesamples(starttime, timeintmins, nsamples)
        return self.makecapture(samples, timeintmins, tag_id)

    def __init__(self):
        super().__init__()


class CaptureListHelper(CaptureHelper):
    def __init__(self, baseurl, adminapi_token, capturespeclist, tagid, timeintmins=12):
        super().__init__()
        self.capturelist = []
        self.writtencaptures = []
        alltimestamps = []
        capturewrapper = CaptureWrapper(baseurl, adminapi_token)
        consumercapturewrapper = ConsumerCaptureWrapper(baseurl)


        for capturespec in capturespeclist:
            capture = self.make_capture_with_samples(starttime=capturespec['starttime'],
                                                     tag_id=tagid,
                                                     timeintmins=timeintmins,
                                                     nsamples=capturespec['nsamples'])

            writtencapture = capturewrapper.post(capture)

            samples = consumercapturewrapper.get_samples(capture_id=writtencapture['id'])

            # Make a list of all timestamps to find the maximum and minimum
            timestamps = [sample['timestamp'] for sample in samples]
            alltimestamps.extend(timestamps)

            self.capturelist.append(capture)
            self.writtencaptures.append(writtencapture)

        self.mints = min(alltimestamps)
        self.maxts = max(alltimestamps)

